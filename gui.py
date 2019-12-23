import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np
from auto_canny import auto_canny
# take live video feed from cv2
USE_CAMERA = 0 # change to 1 if using multiple sources
cap = cv2.VideoCapture(USE_CAMERA)

class Thread(QThread):
    # connect to a QThread
    changePixmap = pyqtSignal(QImage)

    def run(self):
        while (True):
            ret, frame = cap.read()
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # apply canny edge detector
            edge = auto_canny(cap.read()[1])

            # change b&w to 3 colored channel
            edge_3_channel = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

            # horizontally stack original side by side with edge detector
            rgbStack = np.hstack((rgbFrame, edge_3_channel))

            # convert to readable format for Qt
            convertToQtFormat = QImage(rgbStack.data, rgbStack.shape[1], rgbStack.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640*2, 480*2, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

class camera(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Camera'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.cameraUI()
        self.startCameraThread()
        # self.stopCameraThread()

    @pyqtSlot(QImage)

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def cameraUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1300, 600)
        # create a label
        self.label = QLabel(self)
        self.label.move(10, -150)
        self.label.resize(640*2, 480*2)

        camera_button = QPushButton("Capture", self)
        camera_button.clicked.connect(self.click_picture)

    def startCameraThread(self):
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        self.show()

    def click_picture(self):
        frame = cap.read()[1]
        edge = auto_canny(cap.read()[1])
        cv2.imwrite("original.png", frame)
        cv2.imwrite("edge.png", edge)
        print("*********")
        print("Images were captured!")
        print("Check out your images within this current directory.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = camera()
    ex.show()
    sys.exit(app.exec_())
    ex.stopCameraThread()
    cap.release()
    cv2.destroyAllWindows()