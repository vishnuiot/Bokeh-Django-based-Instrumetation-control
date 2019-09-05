# Bokeh Libraries
from bokeh.io import output_notebook
from bokeh.plotting import figure, show

import datetime
import os
import sys
import time


# Open first found instrument
handle = bodj.openS("ANY", "ANY", "ANY")  # Any device, Any connection, Any identifier
#handle = bodj.openS("Hamamatsu", "ANY", "ANY")  # pyt1 device, Any connection, Any identifier
#handle = bodj.openS("Toshiba", "ANY", "ANY")  # pyt2 device, Any connection, Any identifier
#handle = bodj.open(bodj.constants.dtANY, bodj.constants.ctANY, "ANY")  # Any device, Any connection, Any identifier

info = bodj.getHandleInfo(handle)
print("\nOpened a Bodj with Device type: %i, Connection type: %i,\n"
      "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
      (info[0], info[1], info[2], bodj.numberToIP(info[3]), info[4], info[5]))

# Setup and call eReadName to read from AIN0 on the Bodj.
name = "AIN0"
numIterations = 10
rate = 100 # in ms
rateUS = rate*1000


# Get the current time to build a time-stamp.
appStartTime = datetime.datetime.now()
# startTimeStr = appStartTime.isoformat(timespec='milliseconds')
startTimeStr = appStartTime.strftime("%Y/%m/%d %I:%M:%S%p")
timeStr = appStartTime.strftime("%Y_%m_%d-%I_%M_%S%p")

# Get the current working directory
cwd = os.getcwd()

# Build a file-name and the file path.
fileName = timeStr + "-%s-Example.csv"%(name)
filePath = os.path.join(cwd, fileName)

# Open the file & write a header-line
f = open(filePath, 'w')
f.write("Time Stamp, Duration/Jitter (ms), %s" %(name))

# Print some program-initialization information
print("The time is: %s" %(startTimeStr))
print("Reading %s %i times and saving data to the file:\n - %s\n" %(name, numIterations, filePath))

# Prepare final variables for program execution
intervalHandle = 0
bodj.startInterval(intervalHandle, rateUS)
curIteration = 0
numSkippedIntervals = 0

lastTick = bodj.getHostTick()
duration = 0

while curIteration < numIterations:
	try:
		numSkippedIntervals = bodj.waitForNextInterval(intervalHandle)
		curTick = bodj.getHostTick()
		duration = (curTick-lastTick)/1000
		curTime = datetime.datetime.now()
		curTimeStr = curTime.strftime("%Y/%m/%d %I:%M:%S%p")

		# Read AIN0
		result = bodj.eReadName(handle, name)

		# Print results
		print("%s reading: %f V, duration: %0.1f ms, skipped intervals: %i" % (name, result, duration, numSkippedIntervals))
		f.write("%s, %0.1f, %0.3f\r\n" %(curTimeStr, duration, result))
		lastTick = curTick
		curIteration = curIteration + 1
	except KeyboardInterrupt:
		break
	except Exception:
		import sys
		print(sys.exc_info()[1])
		break

print("\nFinished!")

#Get the final time
appEndTime = datetime.datetime.now()
# endTimeStr = appEndTime.isoformat(timespec='milliseconds')
endTimeStr = appStartTime.strftime("%Y/%m/%d %I:%M:%S%p")
print("The final time is: %s" %(endTimeStr))

# Close file
f.close()

# Close handles
bodj.cleanInterval(intervalHandle)
bodj.close(handle)

# Bokeh visualization
fig = figure(background_fill_color='gray',
             background_fill_alpha=0.5,
             border_fill_color='blue',
             border_fill_alpha=0.25,
             plot_height=300,
             plot_width=500,
             h_symmetry=True,
             x_axis_label='X Label',
             x_axis_type='datetime',
             x_axis_location='above',
             x_range=('2018-01-01', '2018-06-30'),
             y_axis_label='Y Label',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(0, 100),
             title=' Figure',
             title_location='right',
             toolbar_location='below',
             tools='save')

# plot - local host - html
show(fig)
