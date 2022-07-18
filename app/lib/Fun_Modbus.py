#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
"""

Autor: Anderson Amaya Pulido

Libreria personal para el control de multiples dispositivos por rs485




# ideas a implementar





"""
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
#---------------------------------
#           Librerias personales
#---------------------------------

from Lib_File import *            # importar con los mismos nombres
from Lib_Rout import *            # importar con los mismos nombres



#-------------------------------------------------------
# inicio de variable	--------------------------------------

FM_Mensajes = 1     # 0: NO print  1: Print

#-------------------------------------------------------
#           definiciones tramas Modbus
#-------------------------------------------------------
TRAMA_INIT                      = "¿"
TRAMA_FIN                       = "?"
ID_DEFAULT                      = "0000"
ID_ALL                          = "0000"
ID_MASTER_DEFAULT               = "0001"

#-------------------------------------------------------
#           Ejemplos tramas Modulos relevos
#-------------------------------------------------------
"""
#  xxxx : ID del modulo al cual se quiere comunicar

#//---------------------  funciones que son para todos ojo si tienen todo el mismo ID responde al mismo tiempo

¿xxxx0000XXXX?    //devuelve el  id de los modulos  por la misma linea    // mejorar para enviar datos por rs485
¿xxxx0001XXXX?    //cambiar el ID del Modulo por lo que se coloque en las XXXX

#//---------------------  funciones que son esclusivas del modulo

¿xxxx00020000?    // ¿123400020000? le responde al maaestro con su id,  funcion 2 y dato 0
¿xxxx00030000?    // ¿123400030000? le responde al maaestro OK
¿xxxx00040001?    // ¿123400040001? activar rele iz por 1 seg, requiere el ID del moodulo xxxx


"""

#-------------------------------------------------------
#           Ejemplos tramas Modulos Usuarios
#-------------------------------------------------------
"""
#  xxxx : ID del modulo al cual se quiere comunicar


#//---------------------  funciones que son esclusivas del modulo Usuarios

¿xxxx00020000?    // ¿123400020000? le responde al maaestro con su id,  funcion 2 y dato 0
¿xxxx00030000?    // ¿123400030000? le responde al maaestro OK   comos su fuero un ping
¿xxxx10020000?    // ¿123410020000? pericion de dato para procesar respuesta el ¿dato? o ¿NO?


#//---------------------  funciones que son para todos ojo si tienen todo el mismo ID responde al mismo tiempo

¿xxxx0000XXXX?    //devuelve el  id de los modulos  por la misma linea    // mejorar para enviar datos por rs485
¿xxxx0001XXXX?    //cambiar el ID del Modulo por lo que se coloque en las XXXX


"""


"""
RX_MODBUS                 = FIRM + COMMA + 'Serial_Modbus/RX_Modbus.txt'                        # Datos leidos del Nfc
TX_MODBUS                 = FIRM + COMMA + 'Serial_Modbus/TX_Modbus.txt'                        # Datos leidos del Nfc
PILA_MODBUS               = FIRM + COMMA + 'Serial_Modbus/PILA_Modbus.txt'                      # Datos leidos del Nfc

ID_MOD_USUARIOS           = FIRM + COMMA + 'Serial_Modbus/ID_MOD_Usuarios.txt'                      # Datos leidos del Nfc
ID_MOD_RELES               = FIRM + COMMA + 'Serial_Modbus/ID_MOD_Reles.txt'                      # Datos leidos del Nfc

"""





#---------------------------------------------------------
#----       funciones de uso comun para peticiones al servidor
#---------------------------------------------------------


if FM_Mensajes: print 'Modbus'
