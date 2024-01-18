import cv2 as cv
img = cv.imread("bird.jpeg")
px = img[100,100]
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imwrite("grayimg.jpeg", gray_img)