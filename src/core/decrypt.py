from click import echo, prompt
from PyPDF2 import PdfReader

class DecryptException(Exception):
    '''
    Indicate the password is incorrect
    '''
    pass

def decrypt_by_reader(reader: PdfReader) -> bool:
    '''
    Default decrypt check before any PDF processing
    '''
    if not reader.is_encrypted:
        return True
    echo('🔶 The PDF has been protected')
    MAX_DECRYPT_COUNT = 5
    def try_decrypt(count):
        if (count > MAX_DECRYPT_COUNT):
            echo('❌ Try too many times!')
            return False
        password = prompt('👉 Password', hide_input = True)
        if reader.decrypt(password):
            echo('✅ Dycrypted successfully')
            return True
        else:
            echo('❌ Erroreous password')
            return try_decrypt(count + 1)
    return try_decrypt(0)

def decrypt(safe_path: str) -> PdfReader:
    '''
    Open a PDF, decrypt if needed, then return the reader
    '''
    reader = PdfReader(safe_path)
    
    if not decrypt_by_reader(reader):
        raise DecryptException('Try too many times')
    
    return reader
