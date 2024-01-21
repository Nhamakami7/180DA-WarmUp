import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

"""
References: https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
"""

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Create rectangle that will be used to get colors
    height, width, _ = frame.shape

    rect_width = 100
    rect_height = 100
    rect_x = int((width - rect_width) / 2)
    rect_y = int((height - rect_height) / 2)
    rect_bottom_x = rect_x + rect_width
    rect_bottom_y = rect_y + rect_height

    # Draw the rectangle on frame
    cv2.rectangle(frame, (rect_x, rect_y), (rect_bottom_x, rect_bottom_y), (0, 255, 0), 2)
    center_rect = frame[(rect_y + 5):(rect_bottom_y - 5), (rect_x + 5):(rect_bottom_x - 5)]  

    img = cv2.cvtColor(center_rect, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3))
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(img)

    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)

    bar_bgr = cv2.cvtColor(bar, cv2.COLOR_RGB2BGR)
    cv2.imshow('Color Histogram', bar_bgr)

    # Display the resulting frame
    cv2.imshow('Video feed', frame)
    # cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('breaking')
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

