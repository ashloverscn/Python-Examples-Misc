# pip install pymupdf
# pip install fitz
# pip install pypdf
# pip install fpdf2

import fitz

def overlay_stamp_with_invisible_link(input_pdf, output_pdf, stamp_text, position, width, height, link_url):
    pdf_document = fitz.open(input_pdf)
    
    x, y = position
    rect = fitz.Rect(x, y, x + width, y + height)
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        text_info = page.get_text("dict")
        text_width = 0
        
        for block in text_info["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span['text'] == stamp_text:
                            text_width = max(text_width, span['bbox'][2] - span['bbox'][0])
        
        text_x = x + (width - text_width) / 2
        text_y = y + (height / 2) - 6

        page.insert_text((text_x, text_y), stamp_text, fontsize=12, color=(0, 0, 0))

        page.insert_link({
            "kind": fitz.LINK_URI,
            "from": rect,
            "uri": link_url
        })

    pdf_document.save(output_pdf)

input_pdf = 'test_src.pdf'
output_pdf = 'test_out.pdf'
stamp_text = ''
position = (0, 0)
width, height = 1000, 500
link_url = 'tel:+918777246851'

overlay_stamp_with_invisible_link(input_pdf, output_pdf, stamp_text, position, width, height, link_url)
