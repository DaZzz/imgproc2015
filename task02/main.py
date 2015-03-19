import numpy as np
import cv2

def holeRing(size):
  c = np.zeros((size,size),np.uint8)
  center = size / 2
  cv2.circle(c, (center, center), center, (255, 255, 255))
  return c

def holeMask(size):
  c = np.zeros((size,size),np.uint8)
  center = size / 2
  cv2.circle(c, (center, center), center, (255, 255, 255))
  return c

def closing(b, s):
  return cv2.erode(cv2.dilate(b, s), s)

def opening(b, s):
  return cv2.dilate(cv2.erode(b, s), s)

###
# Main program
###
original = cv2.imread('gears.png')
height, width = original.shape[:2]

# A
for h in range(height):
  for w in range(width):
    original[h][w] = [(0 if c < 128 else 255) for c in original[h][w]]


# B
step1 = cv2.erode(original, holeRing(85), iterations=1)

# C
step2 = cv2.dilate(step1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(80,80)), iterations=1)

# D
step3 = original + step2

# E
gearBody = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(100,100))
samplingRingSpacer = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
samplingRingWidth  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
step41 = cv2.dilate(opening(step3, gearBody), samplingRingSpacer)
step4 = cv2.dilate(step41, samplingRingWidth) - step41

# F
step5 = cv2.bitwise_and(step3, step4)

# G
step6 = cv2.dilate(step5, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))

# H
defectCue = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(30,30))
result = cv2.bitwise_or(cv2.dilate(step4 - step6, defectCue), step6)

cv2.imshow('original', original)
cv2.imshow('step-1', step1)
cv2.imshow('step-2', step2)
cv2.imshow('step-3', step3)
cv2.imshow('step-4-1', step41)
cv2.imshow('step-4-2', step4)
cv2.imshow('step-5', step5)
cv2.imshow('step-6', step6)
cv2.imshow('result', result)

cv2.waitKey(0)
cv2.destroyAllWindows()