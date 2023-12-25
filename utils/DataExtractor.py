# Import required packages
import cv2
 

# Read image from which text needs to be extracted
img = cv2.imread('./test_docs/2303.05352-images-1.jpg')

# Preprocessing the image starts
img_cropped_horizontal = img[:, 150:img.shape[1]-150]
cv2.imshow('img_cropped_horizontal', img_cropped_horizontal)
cv2.waitKey(0)
# Convert the image to gray scale
gray = cv2.cvtColor(img_cropped_horizontal, cv2.COLOR_BGR2GRAY)
 
# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
 
# Specify structure shape and kernel size. 
# Kernel size increases or decreases the area 
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect 
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,25))
 
# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 3)
 
# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
                                                 cv2.CHAIN_APPROX_NONE)
 
# Creating a copy of image
im2 = img_cropped_horizontal.copy()

#write a resize func 


 
# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
     
    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]
    cv2.imshow('cropped', cv2.resize(cropped, (cropped.shape[1]//2, cropped.shape[0]//2)))
    cv2.waitKey(0)