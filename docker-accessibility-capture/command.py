from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
#import com.android.provider.Settings
import time, sys, os.path, os
import subprocess #for running monkey command to start app with package name alone

def bashCall(bashCommand):
	print "bash Call: "+bashCommand
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print "output "
	print output

def click(device,x,y):
	device.wake()
	device.touch(x,y,'DOWN_AND_UP')

def screenshot(device):
	filename = "/screen.png"
	device.wake()
	screenShot = device.takeSnapshot()
	screenShot.writeToFile(filename,'png')
	print "writing to : " + filename
	print "retrieve with:"
	print "docker cp <id>:" + filename + " <path to copy to>"

def install_app(device, pathToAPK):
	bashCommand = "adb install "+pathToAPK
	bashCall(bashCommand)

def open_app(device,package):
	bashCommand = "adb shell monkey -p "+package+" -c android.intent.category.LAUNCHER 1"
	bashCall(bashCommand)

if __name__ == "__main__":
	device = MonkeyRunner.waitForConnection()
	command = sys.argv[1]
	if command == "-l":
		print "possible commands: "
		print "monkeyrunner command.py -l"
		print "monkeyrunner command.py click <x coord> <y coord>"
		print "monkeyrunner command.py install <path to APK>"
	elif command == "click":
		x = int(sys.argv[2])
		y = int(sys.argv[3])
		click(device, x,y)
	elif command=="install":
		path = sys.argv[2]
		install_app(device, path)
	elif command=="open":
		package = sys.argv[2]
		open_app(device, package)
	elif command == "screenshot":
		screenshot(device)
	else :
		print "no such command"
	
	#device.wake()
	#device.touch(100,300,'DOWN_AND_UP')

