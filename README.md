# Firmware 4_0
# Madre : Firmware2_0
# Para  : solutions.fusepong.com (Comfamiliar)
# ----- No modificar las primeras 3 lineas -----
# (modificar solo para nuevos o cambios de firmware)
#-------------------------------------------------------------
# 0)preparacion para nuevos formatos QR (Mantener logica de los antiguos)
#
# 1) Mejoras de Librerias personales :
#
#   Lib_File               : Manejo de archivos como base de datos
#   Lib_Rout               : Rutas de todo el aplicativo
#   Lib_Encryp             : Para los tipos de incriptaciones del aplicativo
#   Lib_Regular_Expression : Expreciones regulares , para validaciones de string
#   Lib_Networks           : Estados de Redes (Wifi, Ethernet) ,
#   Lib_Requests_Server    : Peticiones al servidor
#   Lib_Generator_Pin      : Generador de pines (no se esta usando en la actualidad)
#
# 2) Mejoras de Actuadores del dispositivo :
#
#   Act_Boton_No_Touch     : manejo del boton no touch TH-040
#   Act_Buzzer             : manejo del buzzer 5v activo
#   Act_Led_RGB            : manejo del led rgb
#   Act_Power_IR           : manejo del sensor IR y led de potencia
#   Act_Rele               : manejo del rele
#   Act_Teclado            : manejo de la bisualizacion en la pantacha de 3.5 pulgadas
#   Sen_QR.py              : Por serial nuevas validaciones del QR
#
# 3)  Mejoras de lectura de sensores
#
#   Sen_QR                 : lectura y alistamiento basico del qr
# 4)  Mejoras de lectura de procesos
#
