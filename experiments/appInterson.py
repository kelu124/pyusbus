# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2 	
import os
import time
import numpy as np 
import pyusbus



#probe.dopplerDta[0]
#np.sqrt(np.sqrt(np.abs(probe.loop[1])).T[7:]

class DopplerApp:
	
	def __init__(self):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event 
		self.probe = pyusbus.Interson()
		self.probe.StartRun() 
		self.frame = None
		self.thread = None
		self.stopEvent = None
		# initialize the root window and image panel
		self.root = tki.Tk()

		self.panel = None
		self.panelD = None
		self.panelS = None
		self.imgBW = None
		self.imgDoppler = None
		# create a button, that when pressed, will take the current
		# frame and save it to file

		btnFreeze = tki.Button(self.root, text="Freeze", command=self.Freeze)
		btnFreeze.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)


		btn = tki.Button(self.root, text="Capture", command=self.takeSnapshot)
		btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
		self.display_text = tki.StringVar()
		self.display = tki.Label(self.root, textvariable=self.display_text) 
		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.bwLoop, args=())
		self.thread.start()
		# set a callback to handle when the window is closed
		self.root.wm_title("Doppler")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


 
	def Freeze(self):
		if not self.stopEvent.is_set():
			self.stopEvent.set() 
			print("Freeze")
		else:
			self.stopEvent.clear() 
			print("Unfreeze")
			self.thread = threading.Thread(target=self.bwLoop, args=())
			self.thread.start()
		return 1			
	def takeSnapshot(self):
		# grab the current timestamp and use it to construct the
		# output path
		ts = datetime.datetime.now()
		filename = "{}.".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))

		#bw,doppler = self.imgBW, self.imgDoppler
		#np.savez("./data/20211030-npz/"+filename + "npz", bw, doppler)
		np.savez("./data/20211030-npz/bw"+filename + "npz", self.probe.loop)
		
		print("[INFO] saved {}".format(filename+ "npz"))

	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set() 
		self.root.quit()


	def bwLoop(self): 
			try:
				# keep looping over frames until we are instructed to stop
				while not self.stopEvent.is_set():
					# grab the frame from the video stream and resize it to
					# have a maximum width of 300 pixels
					self.probe.startMotor() 
					self.probe.startAcq()
					time.sleep(0.5)
					self.probe.getUSBImages(n=10)
					self.probe.stopAcq()
					self.probe.stopMotor()
					N = np.shape(self.probe.rawData)[0]*np.shape(self.probe.rawData)[1]
					img = np.array(self.probe.rawData).reshape(N//2048, 2048)[:2048].T
					img = 255*(img/np.max(img))
					self.frame = img

					self.frame = cv2.resize(self.frame, (400,400), interpolation = cv2.INTER_AREA)
					image = self.frame 
					image = Image.fromarray(image) 
					image = ImageTk.PhotoImage(image)
			
					# if the panel is not None, we sneed to initialize it
					if self.panel is None:
						print("None")
						self.panel = tki.Label(image=image)
						self.panel.image = image
						self.panel.pack(side="left", padx=10, pady=10)
			
					# otherwise, simply update the panel
					else:
						print("Update")
						self.panel.configure(image=image)
						self.panel.image = image
			except RuntimeError:
				print("[INFO] caught a RuntimeError")

pba = DopplerApp()
pba.root.mainloop()