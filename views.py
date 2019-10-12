
# /Django_instrument_project/views.py
from django.http import HttpResponse
import serial
ser = serial.Serial('/dev/ttyUSB0',9600)
ser = serial.Serial('/dev/ttyUSB0',15200)
 
def index(request):
    return HttpResponse("""<h1>Project Server</h1>
        <a href="./scan/">scan</a> | 
        <a href="./stopscan/">stopscan</a> | 
        <a href="./getmeasurement/">Agetmeasurement</a>""")
        <a href="./Stopmeasurement/">Stopmeasurement</a> | 
        <a href="./Startmeasurement/">Startmeasurement</a>|
        <a href="./calibrate/">calibrate</a>""")|
        <a href="./reset/">reset</a>""")|
 
def Scan(request):
    ser.write("scan")
    s = ser.readline()
    return HttpResponse(s)
 
def StopScan(request):
    ser.write("stopscan")
    s = ser.readline()
    return HttpResponse(s)
 
def getmeasurement(request):
    ser.write("getmeasurement")
    s = ser.readline()
    return HttpResponse(s)

def Stopmeasurement(request):
    ser.write("Stopmeasurement")
    s = ser.readline()
    return HttpResponse(s)
 
def Startmeasurement(request):
    ser.write("startmeasurement")
    s = ser.readline()
    return HttpResponse(s)
 
def calibrate(request):
    ser.write("calibrate")
    s = ser.readline()
    return HttpResponse(s)

def reset(request):
    ser.write("reset")
    s = ser.readline()
    return HttpResponse(s)
