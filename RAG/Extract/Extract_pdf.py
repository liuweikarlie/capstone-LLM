from langchain_text_splitters import CharacterTextSplitter
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Table, CompositeElement
import pytesseract
import os



def extract_pdf_elements(path, fname):
    """
    Extract images, tables, and chunk text from a PDF file.
    path: File path, which is used to dump images (.jpg)
    fname: File name
    """
    image_output_path = os.path.join(path, "images")
    
    # Create the directory if it does not exist
    if not os.path.exists(image_output_path):
        os.makedirs(image_output_path)
    pdf_filepath = os.path.join(path, fname)
    return partition_pdf(
        filename=pdf_filepath,
        extract_images_in_pdf=False,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=200,
        image_output_dir_path=image_output_path,
    )


def categorize_elements(raw_pdf_elements):
    """
    Categorize extracted elements from a PDF into tables and texts.
    raw_pdf_elements: List of unstructured.documents.elements
    """
    tables = []
    texts = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
                tables.append(element)
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
                texts.append(str(element))
    return texts, tables

