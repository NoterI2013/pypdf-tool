import click
from PyPDF2 import PdfReader, PdfWriter
from utils.guard import is_valid_pdf, is_valid_range, is_valid_path
from core.decrypt import decrypt_by_reader
from utils.format import FilenameRange, parse_filepath_range

@click.command()
@click.argument('filepath', callback=lambda ctx, param, value: parse_filepath_range(value))
@click.option('--output', '-o', 'opath', default="./output.pdf", show_default = True, help = "Specify the output path.")
@click.option('--encrypt', '-e', 'password', help="Encrypt with give password.")

def copy(filepath: FilenameRange, opath: str, password: str):

    '''
    Copy a pdf file
    '''

    # Guard
    if not is_valid_path(opath):
        click.echo('❌ Invalid output path')
        return

    path = filepath.path

    # Guard
    if not is_valid_pdf(path):
        click.echo('❌ Input is not a valid PDF')
        return
    
    # Main functionality
    reader = PdfReader(path)
    if not decrypt_by_reader(reader):
        return
    
    start_page = filepath.start - 1 if filepath.start else 0
    jump_const = filepath.step if filepath.step else 1
    if jump_const > 0:
        end_page = filepath.stop if filepath.stop else len(reader.pages)
    elif jump_const < 0:
        end_page = filepath.stop - 2 if filepath.stop else -1
        
    # Guard
    valid_range_judge, msg = is_valid_range(reader, start_page, end_page, jump_const)
    if not valid_range_judge:
        click.echo(f'❌ {msg}')
        return

    click.echo(f'processing: {path}, rangefrom[{filepath.start}:{filepath.stop}:{filepath.step}]')
    # click.echo(f'start = {start_page}, end = {end_page}, step = {jump_const}')
    writer = PdfWriter()
    for i in range(start_page, end_page, jump_const):
        writer.add_page(reader.pages[i])

    if password:
        writer.encrypt(password)

    with open(opath, "wb") as f:
        writer.write(f)