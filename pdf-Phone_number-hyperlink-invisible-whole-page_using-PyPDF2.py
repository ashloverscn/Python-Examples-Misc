from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os

def create_link_pdf(page_width, page_height, link_url):
    packet = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    packet_path = packet.name
    c = canvas.Canvas(packet_path, pagesize=(page_width, page_height))
    
    c.setFillColorRGB(1, 1, 1, 0)
    c.linkURL(link_url, (0, 0, page_width, page_height), relative=0)
    c.save()

    packet.close()

    return packet_path

def patch_replica_over_original(input_pdf_path, output_pdf_path, link_url):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page_width = page.mediabox.width
        page_height = page.mediabox.height

        link_pdf_path = create_link_pdf(page_width, page_height, link_url)

        if not os.path.exists(link_pdf_path):
            print(f"Error: The link overlay PDF was not created: {link_pdf_path}")
            continue

        try:
            link_reader = PdfReader(link_pdf_path)

            if len(link_reader.pages) == 0:
                print(f"Error: The link overlay PDF is empty: {link_pdf_path}")
                continue

            original_page = reader.pages[page_num]
            link_page = link_reader.pages[0]

            original_page.merge_page(link_page)

            writer.add_page(original_page)

        except Exception as e:
            print(f"Error processing overlay PDF: {e}")
            continue

        os.remove(link_pdf_path)

    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

input_pdf = 'test_src.pdf'
output_pdf = 'test_out.pdf'
#link_url = 'https://google.com'
link_url = 'tel:+918777246851'
patch_replica_over_original(input_pdf, output_pdf, link_url)
