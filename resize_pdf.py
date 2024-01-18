from PyPDF2 import PdfReader, PdfWriter

def main():
	#fileName = raw_input("Type your file name: ")

	pdfFile = PdfReader(open('input.pdf', 'rb'))
	# Getting only first page!
	newPage = pdfFile.pages[0]

	newHeight = 1024
	newWidth = 841

	# Conversion to points
	newHeight = newHeight * 2.83464567
	newWidth = newWidth * 2.83464567

	newPage.scale_to(newWidth, newHeight)

	writer = PdfWriter()
	writer.add_page(newPage)

	with open('resize_.pdf' , "wb") as outfp:
		writer.write(outfp)

if __name__ == "__main__":
    main()
