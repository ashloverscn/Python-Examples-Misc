from PyPDF2 import PdfReader, PdfWriter
import random
import time
import os
def main():
	#fileName = raw_input("Type your file name: ")
    with open('input.pdf', 'rb') as pdf_file:
        pdfFile = PdfReader(pdf_file)
        # Getting only first page!
        newPage = pdfFile.pages[0]

        newHeight = 250
        newWidth = 250

        # Conversion to points
        newHeight = newHeight * random.uniform(1.83464567, 2.83464567)
        newWidth = newWidth * random.uniform(1.83464567, 2.83464567)

        newPage.scale_to(newWidth, newHeight)

        writer = PdfWriter()
        writer.add_page(newPage)

        with open('output.pdf' , "wb") as outfp:
                writer.write(outfp)
                file_size = os.path.getsize('output.pdf')
                print(file_size)

if __name__ == "__main__":
    for i in range(100):
        main()
        time.sleep(1)
