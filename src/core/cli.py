import click
from commands.meta import meta
from commands.copy import copy
from commands.merge import merge
from commands.split import split
# from commands.ping import ping

@click.group()
def cli():
    pass

cli.add_command(meta)
cli.add_command(copy)
cli.add_command(merge)
cli.add_command(split)

if __name__ == '__main__':
    cli()
