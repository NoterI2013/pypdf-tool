import click
from commands.meta import meta
from commands.split import split
from commands.copy import copy
# from commands.ping import ping

@click.group()
def cli():
    pass

cli.add_command(meta)
cli.add_command(copy)
# cli.add_command(split)
# cli.add_command(ping)

if __name__ == '__main__':
    cli()
