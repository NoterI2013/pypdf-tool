import re

def parse_slice(slice_str: str) -> slice:
    '''
    Make a slice object via slice literal string
    '''
    parts = slice_str.split(':')

    def try_parse_pint(val: str):
        try:
            return int(val) if val else None
        except ValueError:
            return None

    start = try_parse_pint(parts[0]) if len(parts) > 0 else None
    stop  = try_parse_pint(parts[1]) if len(parts) > 1 else None
    step  = try_parse_pint(parts[2]) if len(parts) > 2 else None
    
    return slice(start, stop, step)

def split_path_slice(mixed: str) -> tuple[str, str]:
    # warning:
    #   the regex guard is not complete
    #   for `xxx[]xxx[]`, it will parse `]xxx[` out
    #   bruh but I don't want give a sec for that
    split = re.match(r'^(.*?)(?:\[(.*)\])?$', mixed)

    return (split.group(1), split.group(2) or '')

# test
# print(parse_slice(''))
# print(parse_slice(':'))
# print(parse_slice('::'))
# print(parse_slice('1::'))
# print(parse_slice(':-1:'))
# print(parse_slice('::2'))
# print(parse_slice('-1::-2'))
# print(parse_slice('1:-50:2'))
