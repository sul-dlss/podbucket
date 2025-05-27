import typer
from rich import print
from rich.progress import track

from typing_extensions import Annotated, Any
from humanize import naturalsize

from podbucket.config import get_config
from podbucket.resourcesync import get_streams, get_resources

app = typer.Typer()


@app.command()
def config():
    print("Configuring")


@app.command()
def streams():
    """
    Output a list of the POD organizations that are available and their
    resourcesync streams.
    """
    get_config()
    for name, url in get_streams().items():
        print(f"- [bold]{name}[/bold] {url}")


@app.command()
def resources(
    name: Annotated[str, typer.Argument(help="The short organization name")] = "",
    verbose: Annotated[bool, typer.Option(help="Print resources")] = False,
):
    """
    Prints out the number and total size of resources in the organization's
    stream.
    """
    get_config()
    streams = {}

    if name:
        url = get_streams().get(name)
        if not url:
            print("[bold red]No organization for {name}[/bold red]")
            raise typer.Exit(code=1)
        streams = {name: url}
    else:
        streams = get_streams()

    items = size = 0
    for name, stream_url in track(streams.items(), description="Fetching streams..."):
        for resource in get_resources(stream_url):
            if verbose:
                print(resource)
            items += 1
            size += resource.length

    print(f"[bold]Total Items:[/bold] {items}")
    print(f"[bold]Total Size:[/bold] {naturalsize(size)}")


@app.command()
def convert():
    print("Converting")


if __name__ == "__main__":
    app()
