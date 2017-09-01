
#import com.android.provider.Settings
import time, sys, os.path, os
import subprocess #for running monkey command to start app with package name alone
print sys.path
sys.path.append(os.path.join('/usr/lib/python2.7/dist-packages/'))
import yaml
from PIL import Image, ImageChops

class Traversal:
	package = ''
	traversalFile = ''
	logFile = ''
	apkPath = ''
	screenCount = 0
	failed = False

	def __init__(self,arg_package,arg_traversalFile,arg_apkPath):
		#self.test_responsiveness()
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
		print "testing responsiveness"
		crashBox = (30,250,290,330)
		crashImage = Image.open("/data/crashScreen.png").crop(crashBox)
		screenFile = self.screenshot()
		screenImage = Image.open(screenFile).crop(crashBox)
		diff = ImageChops.difference(crashImage,screenImage)
		if  not diff.getbbox():
			print "crashed"
			self.click([60,300])
		self.screenshot()
		'''
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
		'''

	def screenshot(self):
		filename = "screen"+str(self.screenCount)+".png"
		phoneDir = "/sdcard/"
		localDir ="./"
		self.screenCount += 1
		#self.device.wake()
		#screenShot = self.device.takeSnapshot()
		#screenShot.writeToFile(filename,'png')
		#get screenshot
		bashCommand = "adb shell screencap -p "+ phoneDir+filename
		self.bashCall(bashCommand)
		#pull off phone to computer
		bashCommand = "adb pull "+phoneDir+filename +" "+localDir+filename
		self.bashCall(bashCommand)
		print "writing to : "+localDir + filename
		print "retrieve with:"
		print "docker cp <id>: "+localDir + filename + " <path to copy to>"
		return localDir+filename

	def install_app(self):
		print "installing"
		bashCommand = "adb install "+self.apkPath
		self.bashCall(bashCommand)

	def uninstall_app(self):
		print "uninstalling"
		bashCommand = "adb uninstall "+self.package
		self.bashCall(bashCommand)

	def open_app(self):
		bashCommand = "adb shell monkey -p "+self.package+" -c android.intent.category.LAUNCHER 1"
		self.bashCall(bashCommand)

	def wait(self, duration):
		time.sleep(duration)				## WAIT ################

	def click(self, coords):
		bashCommand = "adb shell input tap "+str(coords[0])+" "+ str(coords[1])
		self.bashCall(bashCommand)
		#self.device.wake()
		#self.device.touch(int(coords[0]),int(coords[1]),'DOWN_AND_UP')

	def text_entry(self, text):
		bashCommand="adb shell input text \""+text+"\""
		self.bashCall(bashCommand)
		#self.device.type(text)

	def traverse(self):
		self.test_responsiveness()
		
		self.uninstall_app()
		self.test_responsiveness()
		self.install_app()
		self.test_responsiveness()
		self.open_app()
		self.test_responsiveness()
		print(self.package+" trav: "+self.traversalFile+" apk: "+self.apkPath)
		
		traversal_file_data = self.yaml_loader(self.traversalFile)
		traversal_info = traversal_file_data['traversal']
		for traversal_info_key, traversal_info_value in traversal_info.iteritems():
			self.test_responsiveness()
			if traversal_info_key == "commands":
				for traversal_step in traversal_info_value:
					step = traversal_step['type']
					print "step: "+step
					if step == "wait":
						duration = traversal_step['time']
						self.wait(duration) 
					elif step == "screenshot":
						self.screenshot()
					elif step == "click":
						coords = traversal_step['coords']
						self.click(coords)
					elif step == "text_entry":
						text = traversal_step['text']
						self.text_entry(text)
		
		


if __name__ == "__main__":
	usage = "python traverse-app.py -i <package> -t <traversal file path> -a <apk file path>"
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


