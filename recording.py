import pyautogui
import cv2
import numpy as np
import os.path
import time

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer


class Recording:
    def __init__(self, main_window):
        self.main_window = main_window
        self.startTimer = 0
        self.timer = QTimer(self.main_window)
        self.timer.timeout.connect(self.updateTimer)
        self.out = None

    def folderLocation(self):
        text = self.main_window.ln_Location.text()

        record_folder = os.path.expanduser(text)
        path = os.path.join(record_folder)
        os.chdir(path)

    def createFolder(self):
        record_folder = os.path.expanduser("~\\Documents\\Records")
        if not os.path.exists(record_folder):
            os.mkdir(record_folder)

    def recordLocation(self):
        self.record_folder = os.path.expanduser("~\\Documents\\Records")
        path = os.path.join(self.record_folder)
        os.chdir(path)

    def initVideoWriter(self):
        prefRes = self.main_window.comboBox.currentText()
        self.width, self.height = map(int, prefRes.split('x'))
        self.prefName = self.main_window.lineEdit.text()

    def startRecording(self):
        self.startTimer = 0
        self.onLive = True

        self.main_window.pushButton.hide()
        self.main_window.pushButton_2.show()

        resolution = (self.width, self.height)
        codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        filename = f"{self.prefName}" + '.avi'

        self.out = cv2.VideoWriter(filename, codec, 20.0, resolution)
        self.timer.start(1000)
        while self.onLive:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.out.write(frame)
            cv2.imshow('Monitor', frame)
            if cv2.waitKey(1) == ord('p'):
                self.onLive = 0
                self.stopRecording()
                break

    def stopRecording(self):
        self.startTimer = 0
        self.onLive = False

        self.main_window.label_2.setText("00:00:00")
        self.timer.stop()
        self.out.release()
        cv2.destroyAllWindows()

        self.main_window.pushButton.show()
        self.main_window.pushButton_2.hide()

    def updateTimer(self):
        if self.onLive:
            self.startTimer += 1
            self.main_window.label_2.setText(time.strftime("%H:%M:%S", time.gmtime(self.startTimer)))

    def countdown(self):
        t = 5
        while t != -1:
            self.main_window.label_3.setText(str(t))
            QApplication.processEvents()
            time.sleep(1)
            t -= 1
        self.startRecording()
