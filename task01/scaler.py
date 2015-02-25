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

    oldBitsPointer = image.bits()
    oldBitsPointer.setsize(image.byteCount())
    oldBitsArray = np.asarray(oldBitsPointer).reshape(image.height(), image.width(), 4)

    for i in range(newH):
      for j in range(newW):
        x = math.floor(j/scale)
        y = math.floor(i/scale)
        bitsArray[i][j] = oldBitsArray[y][x]

    return newImage

  @classmethod
  def bilinearInterpolation(cls, image, scale):
    oldW = image.width()
    oldH = image.height()
    newW = int(round(image.width() * scale))
    newH = int(round(image.height() * scale))

    newImage = QImage(newW, newH, QImage.Format_RGB32)
    bitsPointer = newImage.bits()
    bitsPointer.setsize(newImage.byteCount())
    bitsArray = np.asarray(bitsPointer).reshape(newH, newW, 4)

    oldBitsPointer = image.bits()
    oldBitsPointer.setsize(image.byteCount())
    oldBitsArray = np.asarray(oldBitsPointer).reshape(image.height(), image.width(), 4)

    print image.height(), image.width()

    for h in range(newH):
      for w in range(newW):
        # x, y - target point in old coords
        x = w * oldW/float(newW)
        y = h * oldH/float(newH)
        x1 = min(math.floor(x), image.width()-1)
        y1 = min(math.floor(y), image.height()-1)
        x2 = min(math.ceil(x), image.width()-1)
        y2 = min(math.ceil(y), image.height()-1)

        # resultColor = [0,0,0,0]

        # if x1 != x2 and y1 != y2:
        resultColor = cls.__calcColor__(oldBitsArray, x, y, x1, y1, x2, y2)

        bitsArray[h][w] = resultColor

    return newImage

  @classmethod
  def __calcColor__(cls, arr, x, y, x1, y1, x2, y2):
    b = cls.__calcChanel__(arr, 0, x, y, x1, y1, x2, y2)
    g = cls.__calcChanel__(arr, 1, x, y, x1, y1, x2, y2)
    r = cls.__calcChanel__(arr, 2, x, y, x1, y1, x2, y2)
    a = cls.__calcChanel__(arr, 3, x, y, x1, y1, x2, y2)
    return [b,g,r,a]

  @classmethod
  def __calcChanel__(cls, arr, c, x, y, x1, y1, x2, y2):
    delimeter = (x2 - x1) * (y2 - y1)
    val = None

    if x1 == x2 and y1 == y2:
      val = arr[y1][x1][c]
    elif x1 == x2:
      val = (y2 - y)/(y2 - y1)*arr[y1][x1][c] + (y - y1)/(y2 - y1)*arr[y2][x1][c]
    elif y1 == y2:
      val = (x2 - x)/(x2 - x1)*arr[y1][x1][c] + (x - x1)/(x2 - x1)*arr[y1][x2][c]
    else:
      val = (arr[y1][x1][c] / delimeter) * (x2 - x) * (y2 - y) \
                  + (arr[y1][x2][c] / delimeter) * (x - x1) * (y2 - y) \
                  + (arr[y2][x1][c] / delimeter) * (x2 - x) * (y - y1) \
                  + (arr[y2][x2][c] / delimeter) * (x - x1) * (y - y1)


    return min(max(int(round(val)), 0), 255)

  @classmethod
  def bicubicInterpolation(cls, image, scale):
    pass

