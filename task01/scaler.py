from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import math

class Scaler(object):

  def __init__(self, arg):
    super(Scaler, self).__init__()
    self.arg = arg

  @classmethod
  def nearestNeighbourInterpolation(cls, image, scale):
    newW = int(round(image.width() * scale))
    newH = int(round(image.height() * scale))

    newImage = QImage(newW, newH, QImage.Format_RGB32)
    bitsPointer = newImage.bits()
    bitsPointer.setsize(newImage.byteCount())
    bitsArray = np.asarray(bitsPointer).reshape(newH, newW, 4)

    for i in range(newH):
      for j in range(newW):
        x = math.floor(j/scale)
        y = math.floor(i/scale)
        pixel = image.pixel(x, y)
        # BGR
        b = qBlue(pixel)
        g = qGreen(pixel)
        r = qRed(pixel)
        bitsArray[i][j] = [b,g,r,0]

    return newImage

  @classmethod
  def bicubicInterpolation(cls, image, scale):
    pass

  @classmethod
  def bilinearInterpolationz(cls, image, scale):
    pass
