import socket
import select
import threading
import re
import hashlib
import base64
import struct
import weakref
import time
import gc


class Websocket(threading.Thread):

    SERVER_AWAIT_TIME = 0.08
    LAST_MESSAGE_TIME = int(time.time())
    DESCONECTION_MAX_TIME = 2

    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    # 0x3-7 reserved
    CLOSE = 0x8
    PING = 0x9
    PONG = 0xA

    CONNECTING, OPEN, CLOSING, CLOSED = range(4)

    GUID_STR = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    HANDSHAKE_STR = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: WebSocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: %(acceptstr)s\r\n\r\n"
    )

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        if 'connections' not in cls.__dict__:
            cls.connections = weakref.WeakSet()
        cls.connections.add(instance)
        return instance

    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.state = self.CONNECTING

    def onMessage(self):
        raise NotImplementedError

    def onLoop(self):
        raise NotImplementedError

    def onConnect(self):
        raise NotImplementedError

    def onDisconnect(self):
        raise NotImplementedError

    def onError(self):
        raise NotImplementedError

    def open_handshake(self):
        data = self.conn.recv(262144)

        if data:
            data = data.decode('utf-8')

        key = re.search("Sec-WebSocket-Key: (.+)\r\n", data).group(1)
        key += self.GUID_STR
        key = hashlib.sha1(key.encode('utf-8')).digest()
        acceptstr = base64.b64encode(key).decode('utf-8')
        response = self.HANDSHAKE_STR % {'acceptstr': acceptstr}
        self.conn.sendall(response.encode('utf-8'))
        self.state = self.OPEN

    def data_transfer(self):
        OPCODE, PAYLOAD_DATA = self.parse_frame()
        try:
            if OPCODE == self.TEXT:
                self.onMessage(PAYLOAD_DATA.decode('utf-8'))
            elif OPCODE == self.BINARY:
                self.onMessage(PAYLOAD_DATA)
            elif OPCODE == self.CLOSE:
                self.state = self.CLOSING
                self.close_handshake()
            elif OPCODE == self.PING:
                pass
            elif OPCODE == self.PONG:
                pass
            else:
                self.close_handshake(1002)
        except:
            self.onError()
    def parse_frame(self):
        try:
            data = self.conn.recv(2)

            FIN = (data[0] >> 7) & 1
            RSV1 = (data[0] >> 6) & 1
            RSV2 = (data[0] >> 5) & 1
            RSV3 = (data[0] >> 4) & 1

            OPCODE = data[0] & 0xf
            MASK = (data[1] >> 7) & 1

            if not MASK:
                self.close_handshake(1002)

            PAYLOAD_LENGTH = data[1] & 0x7f

            if PAYLOAD_LENGTH == 126:
                data = self.conn.recv(2)
                PAYLOAD_LENGTH = struct.unpack('H', data)[0]
            elif PAYLOAD_LENGTH == 127:
                data = self.conn.recv(8)
                PAYLOAD_LENGTH = struct.unpack('Q', data)[0]

            MASKING_KEY = self.conn.recv(4)

            PAYLOAD_DATA = self.conn.recv(PAYLOAD_LENGTH)

            PAYLOAD_DATA = self.unmask(PAYLOAD_DATA, MASKING_KEY)

            return OPCODE, PAYLOAD_DATA
        except:
            self.onError()

    def unmask(self, data, key):
        unmasked = bytearray(data)
        for i in range(len(data)):
            j = i % 4
            unmasked[i] = data[i] ^ key[j]
        return unmasked

    def build_frame(self, payload_data, opcode):
        header = struct.pack(
            '!B', ((1 << 7) | (0 << 6) | (0 << 5) | (0 << 4) | opcode)
        )
        mask_bit = 0
        length = len(payload_data)

        if length <= 125:
            header += struct.pack('!B', (mask_bit | length))
        elif length <= (2**16):
            header += struct.pack('!B', (mask_bit | 126)) + \
                struct.pack('!H', length)
        elif length <= (2**64):
            header += struct.pack('!B', (mask_bit | 127)) + \
                struct.pack('!Q', length)

        return header + payload_data

    def close_handshake(self, status_code=1000):
        body = struct.pack('H', status_code)
        frame = self.build_frame(body, self.CLOSE)
        self.conn.sendall(frame)

        if self.state == self.OPEN:
            self.state = self.CLOSING

            while True:
                OPCODE, PAYLOAD_DATA = self.parse_frame()
                if OPCODE == self.CLOSE:
                    break

        self.close()

    def broadcast(self, message):
        try:
            if type(message) == str:
                opcode = self.TEXT
                payload_data = message.encode('utf-8')
            elif type(message) == bytes:
                opcode = self.BINARY
                payload_data = message
            else:
                raise Exception("Message has to be string or bytes")

            frame = self.build_frame(payload_data, opcode)

            for t in self.connections:
                if t.conn and self.state != self.CLOSED:
                    t.conn.sendall(frame)
        except:
            self.onError()
    def close(self):
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()
        self.state = self.CLOSED

    def run(self):
        while True:
            gc.collect()
            if self.state == self.CONNECTING:
                self.open_handshake()
                self.onConnect()
            elif self.state == self.OPEN:
                readable, _, _ = select.select(
                    [self.conn], [], [], self.SERVER_AWAIT_TIME)
                if(readable):
                    self.data_transfer()
                else:
                    self.onLoop()
            elif self.state == self.CLOSED:
                conn = self.conn
                del conn
                gc.collect()
                self.onDisconnect()
                break


class WebsocketServer:

    def __init__(self, host, port, queues,
                 print_msg, ws_cls):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.queues = queues
        self.ws_cls = ws_cls
        self.print_msg = print_msg

    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.queues)
        loop = self
        while True:
            if self.print_msg:
                print('[SERVER]= Waiting connection at ' +
                      str(self.host)+":"+str(self.port))
            conn, addr = self.socket.accept()
            if self.print_msg:
                print('[SERVER]= Connected from '+str(addr))
            ws = self.ws_cls(conn, addr)
            ws.start()
