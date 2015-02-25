#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import math
from scaler import Scaler

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
    self.isNearestNeighbourButton = QRadioButton('Nearest neighbor')
    self.isBilinearButton = QRadioButton('Bilinear interpolation')
    self.isBicubicButton = QRadioButton('Bicubic interpolation')
    self.isNearestNeighbourButton.setChecked(True)

    vbox = QVBoxLayout()
    vbox.addWidget(self.isNearestNeighbourButton)
    vbox.addWidget(self.isBilinearButton)
    vbox.addWidget(self.isBicubicButton)

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
    scale = percent / 100.0
    scaledImage = None

    # Nearest neighbour interpolation
    if self.isNearestNeighbourButton.isChecked():
      scaledImage = Scaler.nearestNeighbourInterpolation(self.loadedImage, scale)

    # Bicubic interpolation
    if self.isBicubicButton.isChecked():
      pass

    # Bilinear interpolation
    if self.isBilinearButton.isChecked():
      pass

    imageLabel = QLabel()
    imageLabel.setPixmap(QPixmap.fromImage(scaledImage))
    self.scrollArea.setWidget(imageLabel)

  # Actions
  def open(self):
    filePath, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpeg *.jpg)')
    imageLabel = QLabel()
    self.loadedImage = QImage(filePath)
    imageLabel.setPixmap(QPixmap.fromImage(self.loadedImage))
    self.scrollArea.setWidget(imageLabel)

  def createActions(self):
    self.openAct = QAction('&Open', self, shortcut=QKeySequence.Open, triggered=self.open)

  # Menus
  def createMenus(self):
    self.fileMenu = self.menuBar().addMenu('&File')
    self.fileMenu.addAction(self.openAct)

# Run programm
if __name__ == '__main__':
  import sys

  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
