import fpdf  # pip install fpdf2
from fpdf.enums import XPos, YPos

import pypdf
from pypdf import PdfReader, PdfWriter


def generate_overlay(target_path: str, text: str, link: str) -> None:
    class PDF(fpdf.FPDF):
        def header(self) -> None:
            self.set_font("helvetica", "B", 12)
            self.set_text_color(0, 0, 255)  # Blue color for the link
            link_width = pdf.get_string_width(text)
            link_height = 10
            self.cell(
                link_width,
                link_height,
                text=text,
                new_x=XPos.RIGHT,
                new_y=YPos.TOP,
                align="C",
                link=link,
            )

    pdf = PDF()
    pdf.add_page()
    pdf.output(target_path)


def stamp(original_path: str, stamp_path: str, out_path: str) -> None:
    stamp = PdfReader(stamp_path).pages[0]
    writer = PdfWriter(clone_from=original_path)
    for page in writer.pages:
        page.merge_page(stamp, over=False)
    writer.write(out_path)



if __name__ == "__main__":
    print(f"pypdf=={pypdf.__version__}")
    print(f"fpdf2=={fpdf.__version__}")
    stamp_path = "stamp.pdf"
    generate_overlay(stamp_path, "py-pdf.github.io", "https://py-pdf.github.io")
    stamp(stamp_path, "GeoTopo.pdf", "out.pdf")
