
import serial,time,sys,datetime,serial,string,csv,os,os.path
from django import djangoClient
import matplotlib.pyplot as plt
#set absolute path for automated data saving into this directory
os.chdir("/home/bosch/Documents/pycon/1.pyspektr/")

#file to create date, time
# Dummy read line to remove spurious data
inst1= '/dev/ttyACM0'
ser=serial.Serial(isnt1,9600)
x= ser.readline()


# Actual data acquisition starts here
time.sleep (2)
inst1= '/dev/ttyACM0'
ser=serial.Serial(UNO,9600)
x=ser.readline()
# split the byte value and convert into comma seperated list
v=x.decode("utf-8").split(",")
yaxis=[]
for i in range (0,len(v)-1):
        yaxis.append(v[i])
xaxis=[410,435,460,485,510,535,560,585,610,645,680,705,730,760,810,860,900,940]
## prepare yaxis for plotting
print (xaxis)
print (yaxis)
#saves files with current date - CSV format
panelname="spectral_data_"
current_date=time.strftime("%Y%m%d")
current_time=time.strftime("%H:%M")
filename=panelname+current_date+".csv"
print (filename)
file_exists = os.path.isfile(filename)
with open (filename, 'a') as csvfile:
    headers = ['Date', 'Time','410','435','460','485','510','535','560','585','610','645','680','705','730','760','810','860','900','940']
    writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)
    if not file_exists:
        writer.writeheader()  # file doesn't exist yet, write a header
f=open(panelname+current_date+".csv","a+")
csv_f=csv.writer(f)

#modificatin to y axis data to convert it to integer
listToStr =' '.join(map(str,yaxis))
##convert space into ,
yaxis=listToStr.replace(" ",",")
##write data as csv file
f.write(current_date+","+current_time+","+yaxis)
f.write("\n")
f.flush()
ser.flushInput()
ser.flushOutput()

#print (yaxis)
#print (type(yaxis))
def Convert(string): 
    li = list(string.split(',')) 
    return li 
# Yxis converted to list
yaxis=(Convert(yaxis))
#print (yaxis[0]) 
## django 
#Set this variables, django should be localhost on Pi
host = "localhost"
#host="00.000.000.123"

json_body = [
               {
                 "measurement": "spectral_values",
                 "tags":{ "host": "triad"} ,# removed curly braces
                 "fields":{"channel1":yaxis[1],"channel2":yaxis[2],"channel3":yaxis[3],"channel4":yaxis[4],"channel5":yaxis[5],"channel6":yaxis[6],"channel7":yaxis[7],"channel8":yaxis[8],"channel9":yaxis[9],"channel10":yaxis[10],"channel11":yaxis[11],"channel12":yaxis[12],"channel13":yaxis[13],"channel14":yaxis[14],"channel15":yaxis[15],"channel16":yaxis[16],"channel17":yaxis[17]}
               }
             ]
## Write JSON to django
client.write_points(json_body)

## plotting
x = xaxis
y=yaxis
#print (xaxis)
#print (yaxis)
#print (len(xaxis))
#print (len(yaxis))
#print (type(y)) 
#Identify maximum y value to fix axis + add 100
import numpy as np
ylistconvert=np.array(y,dtype=float)
ymax=max(ylistconvert)+100
print ("Maximum y value = "+str(ymax-100))

# add a circle renderer with a size, color, and alpha
#from bokeh.plotting import figure, output_file, show
#from bokeh.plotting import figure,show
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row

# output to static HTML file
#output_file=("index.html") -- First plot
p1 = figure(x_axis_label='Wavelength',y_axis_label='Reflectivity W/m^2',plot_width=600, plot_height=600,x_range=(400,1000),y_range=(0,ymax),title="RAW Data  ")
p1.xaxis.axis_label_text_font_size = "14pt"
p1.yaxis.axis_label_text_font_size = "14pt"

p1.xaxis.axis_line_width=3
p1.yaxis.axis_line_width=3
p1.line(x,y,line_width=2)
p1.circle(x,y,size=10,color="red",alpha=0.5)
# show the results
show(row(p1))
