import typer
import os
from sys import platform
from pathlib import Path
import src
from typing import Optional


app = typer.Typer()


def main(destination: str, verbose: bool = False, json: bool = False) -> None:
    """Syncronize your highlights from a connected Kindle device."""
    kindle_path = get_kindle_path()
    if kindle_path is None:
        typer.echo("Unable to detect a connected Kindle device.")

    clippings_file = kindle_path / "documents/My Clippings.txt"
    if not os.path.isfile(clippings_file):
        typer.echo("No clippings found on connected Kindle.")
        return

    clippings_lines = src.read_clippings(clippings_file)
    if json:
        highlights = src.parse_highlights(clippings_lines)
        src.write_highlights_json(highlights, destination)
    else:
        clippings = src.sort_clippings(clippings_lines)
        src.write_clippings(clippings, destination, verbose=verbose)


def get_kindle_path() -> Optional[Path]:
    """Checks if Kindle device is connected. Also checks for OS, as
    app only works on Linux as of now."""
    if platform == "win32":
        from src.win import list_drives, get_kindle_drive_letter

        drives = list_drives()
        kindle_drive_letter = get_kindle_drive_letter(drives)
        print(kindle_drive_letter)
        return Path(f"{kindle_drive_letter}")

    elif platform == "linux":
        username = os.path.expanduser("~").split("/")[-1]
        return Path(f"/media/{username}/Kindle/")
    else:
        typer.echo(f"{platform} not supported. Current support is linux only.")


if __name__ == "__main__":
    typer.run(main)