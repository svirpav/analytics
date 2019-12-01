import click
from scripts import applications


@click.group()
def main():
    """ Analytics command line tool\n
        To see command specific options run python analytics.py command --help
    """
    pass


@main.command()
#   @click.option('--p', help='Command option')
@click.argument('file')
def analytics(file):
    """This command is to run alasys based on customer."""
    applications.Analytics().app(file)


@main.command()
#   @click.option('--p', help='Command option')
@click.argument('file')
def application(file):
    """This command is to run alasys based on customer."""
    applications.Application().app(file)


@main.command()
#   @click.option('--p', help='Command option')
@click.argument('file')
def supplier(file):
    """This command is to run alasys based on customer."""
    applications.Supplier().app(file)


if __name__ == "__main__":
    main()
