import pytesseract
import pdf2image

class DataExtractor:
    extractedText = ''
    def __init__(self,filePath) -> None:
        self.filePath = filePath
    
    def extractTextFromPdf(self):
        images = pdf2image.convert_from_path(self.filePath)
        text = ''
        pageFirstText = pytesseract.image_to_string(images[0])
        for page in images:
            text += pytesseract.image_to_string(page)
        self.extractedText = text
        self.pageFirstText = pageFirstText
        return text, pageFirstText        #TODO: remove the return not needed
    

    def __str__(self) -> str:
        return self.extractedText

    # extract images from pdf
    '''def extractImagesColumns(self):
        reader = PdfReader(self.filePath)
        for page in reader.pages:
            extracted_images = page.extract_images()
            for img in extracted_images:
                # Preprocessing the image starts
                img_cropped_horizontal = img[:, 150:img.shape[1]-150]
                #cv2.imshow('img_cropped_horizontal', img_cropped_horizontal)
                #cv2.waitKey(0)
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
                    #cv2.imshow('cropped', cv2.resize(cropped, (cropped.shape[1]//2, cropped.shape[0]//2)))
                    #cv2.waitKey(0)

        pass
        '''
    def __str__(self) -> str:
        return self.extractedText
    
#TODO: remove imshow

'''test = DataExtractor('../Research papers/Echantillons Articles-20240101T062528Z-001/Echantillons Articles/Article_10.pdf')
res,PageFirst, PageLast = test.extractTextFromPdf()
with open('output.txt', 'a') as f:
    f.write(res)
with open('outputPageFirst.txt', 'a') as f:
    f.write(PageFirst)
with open('outputPageLast.txt', 'a') as f:
    f.write(PageLast)
    print(res) 
    '''
