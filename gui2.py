import threading
#----------------------------------------------------------------------------------------
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
#----------------------------------------------------------------------------------------
from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics
import datetime
import time
#----------------------------------------------------------------------------------------
file = ""
#----------------------------------------------------------------------------------------

def speak(str):
   from win32com.client import Dispatch
   d = Dispatch("SAPI.SpVoice")
   d.Speak(str)
#----------------------------------------------------------------------------------------
class screenrecorder(QDialog):
   def __init__(self):
      super(screenrecorder, self).__init__()
      loadUi("sr.ui", self)

      self.start.clicked.connect(self.startfunction)
#      self.stop.clicked.connect(self.stopfunction)

   # ----------------------------------------------------------------------------------------
   def startfunction(self):

      global file
      print("Clicked on start!!")
      speak("Recording Started!!")


      time_stamp = datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")
      file_name = f'{time_stamp}.mp4'
      file = file_name
#      webcam = cv2.VideoCapture(0)
      self.stoprecording.setText("To Stop Recording Press \"q\"")
      print(file_name)

      four_cc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
      captured_video = cv2.VideoWriter(file_name, four_cc, 20.0, (1920, 1080))

      while True:
         img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
         img_np = np.array(img)
         img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

         cv2.imshow("Screen Recorder", img_final)

         captured_video.write(img_final)

         if cv2.waitKey(10) == ord("q"):
            cv2.destroyWindow("Screen Recorder")
            self.stopfunction()
            break

   # ----------------------------------------------------------------------------------------
   def stopfunction(self):
      global file
      print("Clicked on stop!!")
      speak("Recording Stopped, Saving File!!")
      self.stoprecording.setText("")
      f = "Recording Saved at " + file
      QMessageBox.about(self, "File Saved Successfully", f)



#----------------------------------------------------------------------------------------
app = QApplication(sys.argv)

mainwindow = screenrecorder()

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(800)
widget.setFixedWidth(800)
widget.show()

app.exec_()