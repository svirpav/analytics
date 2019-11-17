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
def salespart(file):
    """This command is to run alasys based on sales parts numbers.\n
        Example : python analytics.py salespart ~/data/file_name\n
        At the moment only csv is suported
    """
    applications.Salespart().app(file)

@main.command()
#   @click.option('--p', help='Command option')
@click.argument('file')
def analytics(file):
    """This command is to run alasys based on customer."""
    applications.Analytics().app(file)

if __name__ == "__main__":
    main()