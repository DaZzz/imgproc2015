import numpy as np
import cv2

###
# Step 1: Original image
###
img = cv2.imread('../pic.png')


###
# Step 2: Show
###
gs = cv2.cvtColor(img, cv2.CV_64FC1)
gs = np.float32(gs)
gs = gs / 255.0

imgDft = cv2.dft(gs)

# cv2.imshow('Step 1: Original message', img1)
cv2.imshow('Step 1: Original message', gs)
cv2.imshow('Step 1: Original message', imgDft)

cv2.waitKey(0)
cv2.destroyAllWindows()