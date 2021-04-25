import subprocess
import json
from typing import Optional, TypedDict

Drive = TypedDict("Drive", letter=str, label=str)


def list_drives() -> list[Drive]:
    """Get a list of all mounted drives on Windows.

    Thanks to https://abdus.dev/posts/python-monitor-usb/

    Returns
    -------
    list[Drive]
        List of Drives
    """
    proc = subprocess.run(
        args=[
            "powershell",
            "-noprofile",
            "-command",
            "Get-WmiObject -Class Win32_LogicalDisk | Select-Object deviceid,volumename,drivetype | ConvertTo-Json",
        ],
        text=True,
        stdout=subprocess.PIPE,
    )

    if proc.returncode != 0 or not proc.stdout.strip():
        print("Failed to enumerate drives")
        return []
    devices = json.loads(proc.stdout)

    return [
        Drive(
            letter=d["deviceid"],
            label=d["volumename"],
        )
        for d in devices
    ]


def get_kindle_drive_letter(drives: list[Drive]) -> Optional[Drive]:
    """Return Kindle drive if exists in list of drives."""
    for drive in drives:
        if drive.get("label") == "Kindle":
            return drive.get("letter")
