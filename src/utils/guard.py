class PdfFormatException(Exception):
    '''
    Indicate that the file underlined is not PDF format
    '''
    pass

def is_valid_pdf(path: str) -> bool:
    '''
    Return `True` if given destination is a valid PDF format file
    '''
    try:
        with open(path, 'rb') as f:
            header = f.read(4)
            return header == b'%PDF'
    except Exception:
        return False
