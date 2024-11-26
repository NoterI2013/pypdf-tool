import os
from PyPDF2 import PdfReader

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

def is_valid_range(instance: PdfReader, start: int, end: int, step: int) -> tuple[bool, str]:
    stop = end - 1
    if stop >= len(instance.pages):
        return (False, "Pdf end-page out of bound")
    elif start > stop and step > 0:
        return (False, "Invalid start-page, it shouldn't be greater than end-page for positive step number")
    elif start < stop and step < 0:
        return (False, "Invalid start-page, it shouldn't be less than end-page for negative step number")
    elif step == 0:
        return (False, "Invalid step number: it should be a non-zero integer")
    elif start < 0:
        return (False, "Invalid start-page: it should be a positive integer")
    elif stop < 0 and step > 0:
        return (False, "Invalid end-page: it should a positive integer for the increasing step")
    elif stop < -2 and step < 0:
        return (False, "Invalid end-page: it should a positive integer for the decreasing step")
    else:
        return (True, "")
    
def is_valid_path(path: str) -> bool:
    dir_belong = os.path.dirname(path)
    if os.path.exists(dir_belong):
        return True
    else:
        return False