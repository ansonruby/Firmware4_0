# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
"""

Autor: Anderson Amaya Pulido

Libreria personal para el manejo del serson lector qr por serial.




# ideas a implementar





"""
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

#-------------------------------------------------------
#----      importar complementos                    ----
#-------------------------------------------------------
import serial
import os, time
import commands

from serial import SerialException

#---------------------------------
#           Librerias personales
#---------------------------------

from Lib_File import *  # importar con los mismos nombres
from Lib_Rout import *  # importar con los mismos nombres

#-------------------------------------------------------------------------------------
#                                   CONSTANTES
#-------------------------------------------------------------------------------------


SMD_Mensajes = 1    # 0: NO print  1: Print

Puerto_Serial = '/dev/ttyS0'
port = serial.Serial(Puerto_Serial, baudrate=9600, timeout=1)


Contador_Dispotivos =   0
N_Dispositivos      =   0
ID_Dispositivos     =   ""





#--------------------------------------------------------------------------------------
def Tramas_TX():
    global port
    global SMD_Mensajes
    #-------------------------------
    #Para dispotitos CCCB
    #-------------------------------
    rele = Get_File(TX_MODBUS) # leer una linea e eliminar <0001:Access granted-E>
    if len(rele)>= 1:

        if SMD_Mensajes: print 'TX:' + rele

        port.write(rele)
        Clear_File(COM_TX_RELE)

#---------------------------------------------------------------------------------------

def Tramas_RX():
    global port
    global SMD_Mensajes
    global Puerto_Serial

    try :
        #Tx_datos()
        rcv = port.read(250)
        T_rcv = len(rcv)
        if T_rcv >= 1:
            if SMD_Mensajes: print 'Cuantos:' + str(T_rcv)
            print 'RX:' + rcv
            #Procesar_Datos(rcv)
        else:
            if SMD_Mensajes: print 'Nada'


    except SerialException:
        while True:
            port = serial.Serial(Puerto_Serial, baudrate=9600, timeout=1)
            break


#---------------------------------------------------------------------------------------
def Control_Canal_Serial():
    while True:
        Tramas_RX()
        Tramas_TX()





#---------------------------------------------------------------------------------------
def proceso_Escan_Dispositivos():
    global Contador_Dispotivos
    global N_Dispositivos
    global ID_Dispositivos

    Get_Dispositivos()
    print N_Dispositivos
    print ID_Dispositivos
    print Contador_Dispotivos






#---------------------------------------------------------------------------------------



#Control_Canal_Serial()
proceso_Escan_Dispositivos()
