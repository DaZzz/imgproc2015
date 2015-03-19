#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import math

class MainWindow(QMainWindow):
  ###
  # Init window:
  # Setup layout
  # Setup menu and actions
  # Setup outlets
  ###
  def __init__(self):
    super(MainWindow, self).__init__()

    # Init properties
    self.image = None
    self.texture = None

    # Basic window setup
    self.setWindowTitle('Texturer XD375')
    self.resize(640,420)

    self.setupLayout()
    self.createActions()
    self.createMenus()

  ###
  # Set main layout
  ###
  def setupLayout(self):
    # Setup layout
    hbox = QHBoxLayout()
    hbox.setContentsMargins(5, 5, 5, 5)

    # Setup main
    self.scrollArea = QScrollArea()
    self.scrollArea.setBackgroundRole(QPalette.Dark)
    hbox.addWidget(self.scrollArea)

    # Set layout
    centralWidget = QWidget()
    self.setCentralWidget(centralWidget)
    centralWidget.setLayout(hbox)

  ###
  # Actions
  ###
  def openImage(self, imageType):
    filePath, _ = QFileDialog.getOpenFileName(self, 'Open Image', './images', 'Image Files (*.png *.jpeg *.jpg)')
    self.image = QImage(filePath)
    imageLabel = QLabel()
    imageLabel.setPixmap(QPixmap.fromImage(self.image))
    self.scrollArea.setWidget(imageLabel)

  def openTexture(self, imageType):
    filePath, _ = QFileDialog.getOpenFileName(self, 'Open Image', './images', 'Image Files (*.png *.jpeg *.jpg)')
    self.applyTexture(QImage(filePath))

  def createActions(self):
    self.openImageAct = QAction('&Open image', self, shortcut=QKeySequence.Open, triggered=self.openImage)
    self.openTextureAct = QAction('&Open texture', self, shortcut=QKeySequence.AddTab, triggered=self.openTexture)

  ###
  # Menus
  ###
  def createMenus(self):
    self.fileMenu = self.menuBar().addMenu('&File')
    self.fileMenu.addAction(self.openImageAct)
    self.fileMenu.addAction(self.openTextureAct)

  ###
  # Methods
  ###
  def applyTexture(self, texture):
    if not self.image: return

    w = int(round(self.image.width()))
    h = int(round(self.image.height()))
    tw = int(round(texture.width()))
    th = int(round(texture.height()))

    imgBitsPointer = self.image.bits()
    imgBitsPointer.setsize(self.image.byteCount())
    imgBitsArray = np.asarray(imgBitsPointer).reshape(h, w, 4)

    txtrBitsPointer = texture.bits()
    txtrBitsPointer.setsize(texture.byteCount())
    txtrBitsArray = np.asarray(txtrBitsPointer).reshape(th, tw, 4)

    for i in range(h):
      for j in range(w):
        b, g, r, a = [c/255.0 for c in txtrBitsArray[i % th][j % tw]]
        m = r * 0.3 +  g * 0.58 + 0.12 * b

        imgBitsArray[i][j][0] = int(round( imgBitsArray[i][j][0] * m ))
        imgBitsArray[i][j][1] = int(round( imgBitsArray[i][j][1] * m ))
        imgBitsArray[i][j][2] = int(round( imgBitsArray[i][j][2] * m ))

    imageLabel = QLabel()
    imageLabel.setPixmap(QPixmap.fromImage(self.image))
    self.scrollArea.setWidget(imageLabel)

# Run programm
if __name__ == '__main__':
  import sys

  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())

