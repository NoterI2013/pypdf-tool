import os
import click
from PyPDF2 import PdfReader, PdfWriter
from utils.guard import is_valid_pdf, is_valid_range
from core.decrypt import decrypt_by_reader
from utils.format import FilenameRange, parse_filepath_range


@click.command()
@click.argument('path')
@click.argument('segmentranges', nargs=-1, callback=lambda ctx, param, value: [parse_filepath_range(f"dummy{v}") for v in value])
@click.option('--output', '-o', 'odir', default="./output", show_default=True, help="Specify the output directory.")
@click.option('--encrypt', '-e', 'password', help="Encrypt with the given password.")
def split(path: str, segmentranges: list[FilenameRange], odir: str, password: str):
    """
    Split a PDF into multiple segments based on specified ranges.
    """

    # Guard: Validate input PDF
    if not is_valid_pdf(path):
        click.echo(f"❌ Invalid PDF: {path}")
        return

    # Main functionality
    reader = PdfReader(path)
    if not decrypt_by_reader(reader):
        click.echo(f"❌ Failed to decrypt PDF: {path}")
        return

    # Process output directory
    final_dir = odir
    if os.path.exists(odir):
        # If `odir` exists, create a subdirectory named after the input file
        base_name = os.path.splitext(os.path.basename(path))[0]
        final_dir = os.path.join(odir, base_name)

        # Create the specified directory
        try:
            os.makedirs(final_dir)
            click.echo(f"mkdir: {final_dir}")
        except Exception as e:
            click.echo(f"❌ Failed to create directory {final_dir}: {e}")
            return
    else:
        # If `odir` does not exist, ensure its parent exists or raise an error
        parent_dir = os.path.dirname(odir)
        if parent_dir and not os.path.exists(parent_dir):
            click.echo(f"❌ Parent directory does not exist: {parent_dir}")
            return

        # Create the specified directory
        try:
            os.makedirs(final_dir)
            click.echo(f"mkdir: {final_dir}")
        except Exception as e:
            click.echo(f"❌ Failed to create directory {final_dir}: {e}")
            return

    click.echo(f"Output directory: {final_dir}")

    # Process each range
    for idx, segmentRange in enumerate(segmentranges):
        start_page = segmentRange.start - 1 if segmentRange.start else 0
        jump_const = segmentRange.step if segmentRange.step else 1
        if jump_const > 0:
            end_page = segmentRange.stop if segmentRange.stop else len(reader.pages)
        elif jump_const < 0:
            end_page = segmentRange.stop - 2 if segmentRange.stop else -1
        
        valid_range_judge, msg = is_valid_range(reader, start_page, end_page, jump_const)
        if not valid_range_judge:
            click.echo(f"❌ {msg} for range {segmentRange}")
            continue

        # Generate output file path
        output_file = os.path.join(final_dir, f"segment{idx + 1}.pdf")
        writer = PdfWriter()
        
        # Add pages to the writer
        for i in range(start_page, end_page, jump_const):
            writer.add_page(reader.pages[i])

        if password:
            writer.encrypt(password)
        
        # Write the output file
        try:
            with open(output_file, "wb") as f:
                writer.write(f)
            click.echo(f"✅ Segment {idx + 1} saved to: {output_file}")
        except Exception as e:
            click.echo(f"❌ Failed to save segment {idx + 1}: {e}")

