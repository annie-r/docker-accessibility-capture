from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
#import com.android.provider.Settings
import time, sys, os.path, os
import subprocess #for running monkey command to start app with package name alone
print sys.path
sys.path.append(os.path.join('/usr/lib/python2.7/dist-packages/'))
import yaml


class Traversal:
	device = None
	package = ''
	traversalFile = ''
	logFile = ''
	apkPath = ''
	screenCount = 0
	def __init__(self,arg_package,arg_traversalFile,arg_apkPath):
		self.device = MonkeyRunner.waitForConnection()
		self.package = arg_package
		self.traversalFile = arg_traversalFile
		self.apkPath = arg_apkPath

	def bashCall(self, bashCommand):
		print "bash Call: "+bashCommand
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
		print "output "
		print output

	def yaml_loader(self, filepath):
		file_descriptor = open(filepath, "r")
		data = yaml.load(file_descriptor)
		return data

	def test_responsiveness(self):
		self.screenshot();
		crashBox = (23,227,200,100)
		screen = self.device.takeSnapshot()
		ref = "./data/crashScreen.png"
		crashScreen = MonkeyRunner.loadImageFromFile(ref).getSubImage(crashBox)
		crashScreen.writeToFile("crash.png","png")
		if crashScreen.sameAs(screen.getSubImage(crashBox),0.9):
			print "crashed"
			self.click([60,300])
		self.screenshot()

	def screenshot(self):
		filename = "/screen"+str(self.screenCount)+".png"
		self.screenCount += 1
		self.device.wake()
		screenShot = self.device.takeSnapshot()
		screenShot.writeToFile(filename,'png')
		print "writing to : " + filename
		print "retrieve with:"
		print "docker cp <id>:" + filename + " <path to copy to>"

	def install_app(self):
		bashCommand = "adb install "+self.apkPath
		self.bashCall(bashCommand)

	def uninstall_app(self):
		bashCommand = "adb uninstall "+self.package
		self.bashCall(bashCommand)

	def open_app(self):
		bashCommand = "adb shell monkey -p "+self.package+" -c android.intent.category.LAUNCHER 1"
		self.bashCall(bashCommand)

	def click(self, coords):
		self.device.wake()
		self.device.touch(int(coords[0]),int(coords[1]),'DOWN_AND_UP')

	def text_entry(self, text):
		self.device.type(text)

	def traverse(self):
		self.test_responsiveness()
		'''
		self.install_app()
		self.open_app()
		print(self.package+" trav: "+self.traversalFile+" apk: "+self.apkPath)
		
		traversal_file_data = self.yaml_loader(self.traversalFile)
		traversal_info = traversal_file_data['traversal']
		for traversal_info_key, traversal_info_value in traversal_info.iteritems():
			self.test_responsiveness()
			if traversal_info_key == "commands":
				for traversal_step in traversal_info_value:
					step = traversal_step['type']
					if step == "screenshot":
						self.screenshot()
					elif step == "click":
						coords = traversal_step['coords']
						self.click(coords)
					elif step == "text_entry":
						text = traversal_step['text']
						self.text_entry(text)
						'''
		

if __name__ == "__main__":
	usage = "monkeyrunner traverse-app.py -i <package> -t <traversal file path> -a <apk file path>"
	
	package = ''
	traversalFile = ''
	apkPath = ''
	arg_iter = 1
	while (arg_iter < len(sys.argv)):
		if sys.argv[1]=="-l":
			print usage 
		elif sys.argv[arg_iter] == "-i":
			arg_iter += 1
			package = sys.argv[arg_iter]
		elif sys.argv[arg_iter] == "-t":
			arg_iter += 1
			traversalFile = sys.argv[arg_iter]
		elif sys.argv[arg_iter] == "-a":
			arg_iter += 1
			apkPath = sys.argv[arg_iter]
		arg_iter += 1

	if package == '' or traversalFile == '' or apkPath == '':
		print usage
	else:
		traversal = Traversal(package,traversalFile,apkPath)
		traversal.traverse()
	'''
	command = sys.argv[1]
	if command == "-l":
		print "possible commands: "
		print "monkeyrunner command.py -l"
		print "monkeyrunner command.py click <x coord> <y coord>"
		print "monkeyrunner command.py install <path to APK>"
	elif command == "click":
		x = int(sys.argv[2])
		y = int(sys.argv[3])
		traversal.click(x,y)
	elif command=="install":
		path = sys.argv[2]
		traversal.install_app()
	elif command=="open":
		package = sys.argv[2]
		traversal.open_app(device, package)
	elif command == "screenshot":
		traversal.screenshot(device)
	elif command == "traverse":
		traversal_file = sys.argv[2]
		traverse(device, traversal_file)
	else :
		print "no such command"
	
	#device.wake()
	#device.touch(100,300,'DOWN_AND_UP')
	'''

