import fpdf  # pip install fpdf2
import pypdf
from pypdf import PdfReader, PdfWriter


def generate_overlay(target_path: str, link: str) -> None:
    class PDF(fpdf.FPDF):
        def header(self) -> None:
            # No font, no text to display; just the invisible clickable area
            link_width = 1800  # Width of the clickable region
            link_height = 1008  # Height of the clickable region
            x_position = 10  # X position of the top-left corner of the clickable area
            y_position = 10  # Y position of the top-left corner of the clickable area

            # Create an invisible link (no text displayed, just a clickable region)
            self.link(x_position, y_position, link_width, link_height, link)

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
    generate_overlay(stamp_path, "https://py-pdf.github.io")  # Invisible link
    stamp(stamp_path, "GeoTopo.pdf", "out.pdf")
