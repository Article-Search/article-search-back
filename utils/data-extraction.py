# this is a standard version of using opencv to extract data from pdf
# it will be changed to fit to our specific needs which is exteacting the columns in the research paper
from pdf2image import convert_from_path
import cv2
import pytesseract
import numpy as np

# Path to your PDF file
pdf_path = './test_docs/2303.05352.pdf'

# Convert PDF to images
pages = convert_from_path(pdf_path, 300)  # 300 is DPI, adjust as needed

# Loop through each page/image
for i, page in enumerate(pages):
    # Convert PIL image to OpenCV format
    img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

    # Convert the image to grayscale for processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply any necessary preprocessing techniques (like thresholding, blurring, etc.)
    # ...

    # Example: Apply Canny edge detection for column identification
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Find contours to identify column boundaries
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract columns based on contours (this is a simplified example)
    columns = []
    for idx, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        column = img[y:y+h, x:x+w]
        columns.append(column)

        # Save the extracted columns as images
        column_filename = f"./pics/page_{i + 1}_column_{idx + 1}.png"
        cv2.imwrite(column_filename, column)

        print(f"Saved {column_filename}")

        # Display the extracted column (for demonstration purposes)
        cv2.imshow(f"Page {i + 1}, Column {idx + 1}", column)
        cv2.destroyAllWindows()
'''
    # Process each extracted column further if needed
    for idx, column in enumerate(columns):
        # Apply OCR using Tesseract on the extracted columns
        extracted_text = pytesseract.image_to_string(column)  # Use OCR on column
        print(f"Page {i + 1}, Column {idx + 1} - Extracted Text:\n{extracted_text}")

        # You can save or manipulate the extracted text as needed
        # ...

        # Display the extracted column (for demonstration purposes)
        cv2.imshow(f"Page {i + 1}, Column {idx + 1}", column)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

'''

