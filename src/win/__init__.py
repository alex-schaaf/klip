import subprocess
import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Drive:
    letter: str
    label: str
    drive_type: str

    @property
    def is_removable(self) -> bool:
        return self.drive_type == "Removable Disk"


drive_types = {
    0: "Unknown",
    1: "No Root Directory",
    2: "Removable Disk",
    3: "Local Disk",
    4: "Network Drive",
    5: "Compact Disc",
    6: "RAM Disk",
}


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
            drive_type=drive_types[d["drivetype"]],
        )
        for d in devices
    ]


def get_kindle_drive(drives: list[Drive]) -> Optional[Drive]:
    """Return Kindle drive if exists in list of drives."""
    for drive in drives:
        if drive.label == "Kindle":
            return drive


if __name__ == "__main__":
    drives = list_drives()
    kindle_drive = get_kindle_drive(drives)
    print(kindle_drive)