from pathlib import Path

import typer
from humanize import naturalsize
from rich import print
from rich.progress import track
from typing_extensions import Annotated

from podbucket.config import get_config
from podbucket.convert import marcxml_to_parquet
from podbucket.resourcesync import get_resources, get_streams

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
    org: Annotated[str, typer.Argument(help="The organization name")] = "",
    verbose: Annotated[bool, typer.Option(help="Print resources")] = False,
):
    """
    Prints out the number and total size of resources in the organization's
    stream.
    """
    get_config()
    streams = get_streams(org)

    items = size = 0
    for org, stream_url in track(streams.items(), description="Fetching streams..."):
        for resource in get_resources(stream_url):
            if verbose:
                print(resource)
            items += 1
            size += resource.length

    print(f"[bold]Total Items:[/bold] {items}")
    print(f"[bold]Total Size:[/bold] {naturalsize(size)}")


@app.command()
def convert(
    output_dir: Annotated[Path, typer.Option(exists=True, file_okay=False)],
    org: Annotated[str, typer.Option(help="Organization name")] = None,
):
    get_config()

    for org, stream_url in get_streams(org).items():
        for resource in track(get_resources(stream_url), description=org):
            if resource.mediatype == "application/gzip":
                marcxml_to_parquet(resource.url, output_dir)


if __name__ == "__main__":
    app()
