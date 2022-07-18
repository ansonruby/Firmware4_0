#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
"""

Autor: Anderson Amaya Pulido

Libreria personal para procesar un qr.




# ideas a implementar





"""
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

import os
import commands
#---------------------------------
#           Librerias personales
#---------------------------------
from Lib_File import *            # importar con los mismos nombres
from Lib_Rout import *            # importar con los mismos nombres


#---------------------------------------------------------
#----       funciones de uso comun para el dispositivo
#---------------------------------------------------------
def Get_ID_Dispositivo():
    Caracte         = ((Get_Line(INF_DISPO, 1)).replace("\n","")).replace("\r","")
    Consecutivo     = ((Get_Line(INF_DISPO, 3)).replace("\n","")).replace("\r","")
    fech            = ((Get_Line(INF_DISPO, 2)).replace("\n","")).replace("\r","")
    ID = Caracte + fech + Get_MAC_addres() +Consecutivo

    #ID= 'CCCB25022021b827eb5f6c3b000003'   # fusepong
    #ID= 'CCCB23102020b827ebc30bd7000001'   # IF_CHI_01
    #ID= 'ABDD12102021b827eb110f29000007'    # CF_COL_07

    return ID
#---------------------------------------------------------
def Get_MAC_addres():
    MAC_DIRC        = 'cat /sys/class/net/wlan0/address'
    MAC             = commands.getoutput(MAC_DIRC)
    MAC             = MAC.replace(":","")
    return MAC

print Get_ID_Dispositivo()
