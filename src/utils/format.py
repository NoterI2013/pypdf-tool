import click
import re

"""
Use @click.argument('fileinfo', callback=lambda ctx, param, value: parse_filename_range(value)) to define file input pattern
Your'll obtain
path:  fileinfo.path
start: fileinfo.start
stop:  fileinfo.stop
step:  fileinfo.step

Example 1: ./test/testfile1[3:10:2]
path = ./test/testfile1
start= 3
stop = 10
end  = 2

Example 2: ./test/testfile2[3::2]
path = ./test/testfile2
start= 3
stop = None
end  = 2
"""

# Custom class to handle the format <filename>[<start>:<stop>:<step>]
class FilenameRange:
    def __init__(self, path, start=None, stop=None, step=None):
        self.path = path
        self.start = start
        self.stop = stop
        self.step = step

    def __repr__(self):
        return f"<FilenameRange filepath={self.path}, start={self.start}, stop={self.stop}, step={self.step}>"

# Function to parse the input
def parse_filepath_range(value):
    # Regular expression to match the pattern <filepath>[<start>:<stop>:<step>]
    pattern = r"(?P<path>[\w\.\-\\/]+)(?:\[(?P<start>-?\d*):?(?P<stop>-?\d*):?(?P<step>-?\d*)\])?"


    match = re.match(pattern, value)
    if match:
        # Extract the matched groups
        path = match.group("path")
        start = match.group("start")
        stop = match.group("stop")
        step = match.group("step")

        # Convert start, stop, step to integers if they exist, else None
        start = int(start) if start else None
        stop = int(stop) if stop else None
        step = int(step) if step else None

        return FilenameRange(path, start, stop, step)
    else:
        raise click.BadParameter(f"Invalid format: {value}. Expected <file>[<start>:<stop>:<step>]")
