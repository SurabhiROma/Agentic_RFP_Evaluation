
from pathlib import Path

from tools.pdf_reader import extract_pdf_text

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

EXPECTED = {
    "apex_systems.pdf": "Apex Systems",
    "brightpath_tech.pdf": "BrightPath Tech",
    "nexaworks.pdf": "NexaWorks",
    "orbit_digital.pdf": "Orbit Digital",
}


def test_all_supplier_pdfs_exist_and_are_readable():
    for filename, supplier_name in EXPECTED.items():
        pdf_path = DATA_DIR / filename

        assert pdf_path.exists(), f"Missing PDF: {filename}"

        text = extract_pdf_text(str(pdf_path))

        assert supplier_name in text
        assert "COMMERCIAL PROPOSAL" in text
        assert "SECURITY AND COMPLIANCE" in text
