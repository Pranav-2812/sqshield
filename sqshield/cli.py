import click
from .predict import predict, preprocess_query
from .__init__ import __version__
@click.command()
@click.argument("input", required=False)
@click.option("--version", "-v", is_flag=True, help="Show the version and exit.")
@click.option(
    "--report",
    "-r",
    is_flag=True,
    help="Show a complete DataFrame report for the query."
)
def main(input, version, report):
    if version:
        click.echo(f"sqshield version : {__version__}")
        return
    if report:
        df = preprocess_query(input)
        click.echo(df.to_string(index=False))
        return
    result = predict(input)
    if result[0] == 1:
        click.echo("Query is MALICIOUS")
    else:
        click.echo("Query is BENGIN")
        