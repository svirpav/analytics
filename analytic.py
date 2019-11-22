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


if __name__ == "__main__":
    main()
