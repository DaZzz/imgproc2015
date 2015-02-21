#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np

class MainWindow(QMainWindow):
  ###
  # Init window:
  # Setup layout
  # Setup menu and actions
  # Setup outlets
  ###
  def __init__(self):
    super(MainWindow, self).__init__()

    # Loaded Image
    self.loadedImage = None

    # Basic window setup
    self.setWindowTitle('Scaler 3000')
    self.setMinimumSize(400,300)
    self.resize(480,320)

    # Setup layout
    hbox = QHBoxLayout()
    hbox.setContentsMargins(5, 5, 5, 5)

    # Setup main
    hbox.addWidget(self.createScrollArea())
    hbox.addWidget(self.createSideBar())

    # Set layout
    centralWidget = QWidget()
    self.setCentralWidget(centralWidget)
    centralWidget.setLayout(hbox)

    self.createActions()
    self.createMenus()
    self.setupOutlets()

  ###
  # Create scroll area
  ###
  def createScrollArea(self):
    self.scrollArea = QScrollArea()
    self.scrollArea.setBackgroundRole(QPalette.Dark)
    return self.scrollArea

  ###
  # Create side bar
  ###
  def createSideBar(self):
    sideBar = QWidget()
    sideBar.setFixedWidth(200)

    vbox = QVBoxLayout()
    vbox.setContentsMargins(5, 5, 5, 5)
    vbox.addWidget(self.createRadiobuttons())
    vbox.addWidget(self.createSlider())
    vbox.addStretch(1)

    sideBar.setLayout(vbox)
    return sideBar

  ###
  # Return GroupBox with all interpalation methods
  ###
  def createRadiobuttons(self):
    self.radioButtons = QGroupBox('Method')
    r1 = QRadioButton('Nearest neighbor')
    r2 = QRadioButton('Biquad interpolation')
    r3 = QRadioButton('Bicubic interpolation')
    r1.setChecked(True)

    vbox = QVBoxLayout()
    vbox.addWidget(r1)
    vbox.addWidget(r2)
    vbox.addWidget(r3)

    self.radioButtons.setLayout(vbox)
    self.radioButtons.setFixedHeight(180)
    return self.radioButtons

  ###
  # Return GroupBox with slider
  ###
  def createSlider(self):
    sliderGroup = QGroupBox('Scale')
    self.scaleSlider = QSlider(Qt.Horizontal)
    self.scaleSlider.setTickInterval(10)
    self.scaleSlider.setMinimum(100)
    self.scaleSlider.setMaximum(400)
    self.scaleLabel = QLabel('100%')
    self.scaleLabel.setAlignment(Qt.AlignCenter)
    self.scaleSlider.valueChanged.connect(lambda x: self.scaleLabel.setText(str(x) + '%'))
    self.scaleSlider.valueChanged.connect(self.scaleImage)

    vbox = QVBoxLayout()
    vbox.addWidget(self.scaleLabel)
    vbox.addWidget(self.scaleSlider)
    sliderGroup.setLayout(vbox)
    sliderGroup.setFixedHeight(80)
    return sliderGroup

  def scaleImage(self, percent):
    if not self.loadedImage: return

    w = self.loadedImage.width()
    h = self.loadedImage.height()

    w = round(w * percent / 100)
    h = round(h * percent / 100)

    img = QImage(w, h, QImage.Format_RGB888)
    img.fill(Qt.black)

    imageLabel = QLabel()
    imageLabel.setPixmap(QPixmap.fromImage(img))
    self.scrollArea.setWidget(imageLabel)

  # Actions
  def open(self):
    filePath, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpeg *.jpg)')
    imageLabel = QLabel()
    self.loadedImage = QImage(filePath)
    self.loadedImage.convertToFormat(QImage.Format_RGB888)

    img = self.loadedImage
    ptr = img.bits()
    ptr.setsize(img.byteCount())
    buf = buffer(ptr, 0, img.byteCount())
    arr = np.asarray(ptr).reshape(img.height(), img.width(), 4)
    # print arr

    w = img.width()
    h = img.height()

    # print h, w, len(arr),len(arr[0])

    for i in range(10):
      for j in range(10):
        arr[i][j] = [0,0,0,255]


    imageLabel.setPixmap(QPixmap.fromImage(self.loadedImage))
    self.scrollArea.setWidget(imageLabel)

  def createActions(self):
    self.openAct = QAction('&Open', self, shortcut=QKeySequence.Open, triggered=self.open)

  # Menus
  def createMenus(self):
    self.fileMenu = self.menuBar().addMenu('&File')
    self.fileMenu.addAction(self.openAct)

  # Outlets
  def setupOutlets(self):
    pass

# Run programm
if __name__ == '__main__':
  import sys

  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
