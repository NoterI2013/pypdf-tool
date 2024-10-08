import click
from PyPDF2 import PdfReader
from utils.guard import is_valid_pdf
from core.decrypt import decrypt_by_reader

@click.command()
@click.argument('path')
def meta(path):
    '''
    Get metadata from PDF file
    '''
    # Guard
    if not is_valid_pdf(path):
        click.echo('❌ Input is not a valid PDF')
        return
    # Main functionality
    reader = PdfReader(path)
    if not decrypt_by_reader(reader):
        return
    max_key_len = max(map(len, reader.metadata.keys()))
    max_val_len = max(map(len, reader.metadata.values()))
    indent, gap = '   ', '  '
    click.echo(f'{indent}{"Key":<{max_key_len}}  Value')
    click.echo(f'{indent}{"-" * max_key_len}{gap}{"-" * max_val_len}')
    for key, val in reader.metadata.items():
        formatted = gap.join([f'{key:<{max_key_len}}', val])
        click.echo(f'{indent}{formatted}')
