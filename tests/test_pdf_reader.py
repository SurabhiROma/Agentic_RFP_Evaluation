
import pymupdf
from tools.pdf_reader import extract_pdf_text


def test_extract_pdf_text(tmp_path):
    pdf_path = tmp_path / "sample_supplier.pdf"

    # Create a temporary PDF with sample supplier information.
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text(
            (72, 72),
            "Supplier: Apex Systems\n"
            "Implementation timeline: 12 weeks"
        )
        pdf.save(str(pdf_path))

    result = extract_pdf_text(str(pdf_path))

    assert "Apex Systems" in result
    assert "12 weeks" in result
    assert "Page 1" in result
