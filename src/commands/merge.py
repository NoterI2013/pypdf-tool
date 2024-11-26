import click
from PyPDF2 import PdfReader, PdfWriter
from utils.guard import is_valid_pdf, is_valid_range, is_valid_path
from core.decrypt import decrypt_by_reader
from utils.format import FilenameRange, parse_filepath_range

@click.command()
@click.argument('filepaths', nargs=-1, callback=lambda ctx, param, value: [parse_filepath_range(v) for v in value])
@click.option('--output', '-o', 'opath', default="./output.pdf", show_default=True, help="Specify the output path.")
@click.option('--encrypt', '-e', 'password', help="Encrypt with the given password.")
def merge(filepaths: list[FilenameRange], opath: str, password: str):
    """
    Merge multiple PDFs into one.
    """

    # Guard: Check if output directory exists
    if not is_valid_path(opath):
        click.echo(f"❌ Invalid output path: {opath}")
        return

    writer = PdfWriter()

    for filepath in filepaths:
        path = filepath.path

        # Guard: Check if the file is a valid PDF
        if not is_valid_pdf(path):
            click.echo(f"❌ Invalid PDF: {path}")
            return

        # Load the PDF and decrypt it if necessary
        reader = PdfReader(path)
        if not decrypt_by_reader(reader):
            click.echo(f"❌ Failed to decrypt PDF: {path}")
            return

        # Determine range for pages to merge
        start_page = filepath.start - 1 if filepath.start else 0
        jump_const = filepath.step if filepath.step else 1
        if jump_const > 0:
            end_page = filepath.stop if filepath.stop else len(reader.pages)
        elif jump_const < 0:
            end_page = filepath.stop - 2 if filepath.stop else -1

        valid_range_judge, msg = is_valid_range(reader, start_page, end_page, jump_const)
        if not valid_range_judge:
            click.echo(f"❌ {msg} for {path}")
            return

        click.echo(f"Processing: {path}, range [{filepath.start}:{filepath.stop}:{filepath.step}]")

        # Add pages to the writer
        for i in range(start_page, end_page, jump_const):
            writer.add_page(reader.pages[i])

    # Save the merged PDF
    with open(opath, "wb") as f:
        if password:
            writer.encrypt(password)
        writer.write(f)

    click.echo(f"✅ Merged PDF saved to: {opath}")
