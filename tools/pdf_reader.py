
import pymupdf  # PyMuPDF


def extract_pdf_text(pdf_path):
    """
    Extract readable text from a supplier proposal PDF.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a string.
    """
    try:
        document_text = []

        with pymupdf.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                if text:
                    document_text.append(
                        f"\n--- Page {page_number} ---\n{text}"
                    )

        extracted_text = "\n".join(document_text).strip()

        if not extracted_text:
            raise ValueError(
                "No readable text found. The PDF may be scanned "
                "or contain images instead of selectable text."
            )

        return extracted_text

    except Exception as error:
        raise RuntimeError(
            f"Could not read PDF '{pdf_path}': {error}"
        ) from error
