from PyPDF2 import PdfReader, PdfWriter
from core.decrypt import decrypt
from utils.guard import is_valid_pdf, PdfFormatException
from utils.slice import split_path_slice, parse_slice

def get_sliced_pdf_by_reader_slice(reader: PdfReader, page_range: slice) -> PdfWriter:
    '''
    Generate sliced `PDFwriter` by given reader and range slice
    '''
    write = PdfWriter()

    for page_num in range(len(reader.pages))[page_range]:
        write.add_page(reader.pages[page_num])
    
    return write

def get_sliced_pdf_raw(path_with_slice: str) -> PdfWriter:
    '''
    Generate sliced `PDFwriter` by given raw string
    '''
    (path, slice_str) = split_path_slice(path_with_slice)
    
    if not is_valid_pdf(path):
        raise PdfFormatException('Given file is not formatted as PDF correctly')
    
    return get_sliced_pdf_by_reader_slice(decrypt(path), parse_slice(slice_str))
