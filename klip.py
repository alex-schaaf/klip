import os
from pathlib import Path
from sys import platform

import typer

import klip.main as klip
from klip.operating_systems import windows

app = typer.Typer()


def main(
    destination: str,
    verbose: bool = False,
    json: bool = typer.Option(
        False, help="Will parse highlights into single JSON file."
    ),
) -> None:
    """Syncronize your highlights from a connected Kindle device."""
    kindle_path = get_kindle_path()
    if kindle_path is None:
        typer.echo("Unable to detect a connected Kindle device.")
        return

    clippings_file = kindle_path / "documents/My Clippings.txt"
    if not os.path.isfile(clippings_file):
        typer.echo("No clippings found on connected Kindle.")
        return

    clippings_lines = klip.read_clippings(clippings_file)
    if json:
        highlights = klip.parse_highlights(clippings_lines)
        klip.write_highlights_json(highlights, destination)
    else:
        clippings = klip.sort_clippings(clippings_lines)
        klip.write_clippings(clippings, destination, verbose=verbose)


def get_kindle_path() -> Path | None:
    """Checks if Kindle device is connected."""
    if platform == "win32":
        drives = windows.list_drives()
        kindle_drive_letter = windows.get_kindle_drive_letter(drives)
        path = Path(f"{kindle_drive_letter}")

    elif platform == "linux":
        username = os.path.expanduser("~").split("/")[-1]
        path = Path(f"/media/{username}/Kindle/")

    elif platform == "darwin":  # macOS
        path = Path("/Volumes/Kindle/")

    else:
        typer.echo(f"{platform} not supported.")
        return

    if os.path.exists(path):
        return path


if __name__ == "__main__":
    typer.run(main)
