import cv2 
import pickle
import matplotlib.pyplot as plt

# Function to resize images
def imageResizeTrain(image):
    maxD = 1024
    height, width = image.shape
    aspectRatio = width / height
    if aspectRatio < 1:
        newSize = (int(maxD * aspectRatio), maxD)
    else:
        newSize = (maxD, int(maxD / aspectRatio))
    image = cv2.resize(image, newSize)
    return image

# Function to compute SIFT keypoints and descriptors
def computeSIFT(image):
    sift = cv2.SIFT_create()
    return sift.detectAndCompute(image, None)

# Function to calculate matches between descriptors
def calculateMatches(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
    return good_matches

# Function to visualize matches between images
def getPlot(image1, image2, keypoint1, keypoint2, matches):
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
    matchPlot = cv2.drawMatches(
        image1, keypoint1, image2, keypoint2, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    return matchPlot

# Function to calculate and display results for a pair of images
def calculateResultsFor(i, j):
    keypoint1, descriptor1 = computeSIFT(imagesBW[i])
    keypoint2, descriptor2 = computeSIFT(imagesBW[j])
    matches = calculateMatches(descriptor1, descriptor2)
    score = 100 * (len(matches) / min(len(keypoint1), len(keypoint2)))
    plot = getPlot(images[i], images[j], keypoint1, keypoint2, matches)
    print("Matches:", len(matches))
    print("Keypoints in image 1:", len(keypoint1))
    print("Keypoints in image 2:", len(keypoint2))
    print("Score:", score)
    plt.imshow(plot)
    plt.show()

# Load images (replace with your actual image paths)
imageList = ["ABC", "abc1", "DEF", "def1", "GHI", "ghi1", "JKL", "jkl1", "MNO", "mno1"]
imagesBW = []
images = []
for imageName in imageList:
    imagePath = "data/images/" + str(imageName) + ".jpg"  # Assuming images are in JPEG format
    image = cv2.imread(imagePath)
    images.append(image)
    imagesBW.append(imageResizeTrain(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)))
# Run sample calculation for the first pair of images
calculateResultsFor(0,1)
