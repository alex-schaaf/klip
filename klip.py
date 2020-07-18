import typer
import os
from sys import platform
from pathlib import Path
import klip


app = typer.Typer()

username = os.path.expanduser('~').split('/')[-1]
kindle_path = Path(f'/media/{username}/Kindle/')


def main(destination: str, verbose: bool = False) -> None:
    """Syncronize your highlights from a connected Kindle device."""
    if not kindle_is_connected():
        return

    clippings_file = kindle_path / 'documents/My Clippings.txt'
    if not os.path.isfile(clippings_file):
        typer.echo('No clippings found on connected Kindle.')
        return

    klipings_lines = klip.read_clippings(clippings_file)
    clippings = klip.sort_clippings(klipings_lines)
    klip.write_clippings(
        clippings,
        destination,
        verbose=verbose
    )


def kindle_is_connected() -> bool:
    """Checks if Kindle device is connected. Also checks for OS, as
    app only works on Linux as of now."""
    if platform != 'linux':
        typer.echo(f"{platform} not supported. Current support is linux only.")
        return False
    return os.path.exists(kindle_path)


if __name__ == "__main__":
    typer.run(main)