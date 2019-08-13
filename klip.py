"""
Usage:
    klip.py <input> <output>
    klip.py -h | --help
    klip.py --version

Options:
    -h --help   Show this screen.
    --version   Show version.
"""
from docopt import docopt
import os
from tqdm import tqdm
import re
from pathlib import Path


def find(iterable, x) -> list:
    """Find all occurences of x in given iterable and return indices
    
    Args:
        iterable: List of tuple in which to search.
        x: Element for which so search in given iterable.
        
    Returns:
        (list) of indices.
    """
    seps = []
    for i, entry in enumerate(iterable):
        if entry == x:
            seps.append(i)
    return seps


def read_clippings(fp: str, encoding="utf-8-sig") -> list:
    """Read in Kindle clippings text file as bytes, convert to correct string
    format and strip formatting codes.
    
    Args:
        fp (str): Filepath of the clippings text file.
    
    Returns:
        (list) of lines as strings..
    
    """
    with open(fp, "rb") as file:
        bytes_ = file.readlines()
        lines = [str(b, encoding).rstrip("\r\n") for b in bytes_]
    return lines


def slicer(iterable) -> slice:
    """Iteratively creates slice object from the given iterable containing
    indices. 
    
    Args:
        iterable: List or tuple of indices.
    
    Yields:
        (slice)
    """
    for i, j  in zip(iterable[:-1], iterable[1:]):
        yield slice(i, j)
        
        
def sort_clippings(lines: list, seperator:str = '==========') -> dict:
    """Sort clippings in given list of lines clippings.
    
    Args:
        lines(list): List of lines read from Kindle clippings txt file.
        separator(str, optional): Separator of individual highlights.
            Default: '=========='
    
    Returns:
        (dict)    
    """
    lines.insert(0, seperator)
    sep = find(lines, seperator)
    clippings = {}

    for s in slicer(sep):
        entry = lines[s]

        if entry[1] not in clippings.keys():
            clip = {"highlights": [], "loc": [], "time": [], "page": []}
            clip["author"] = entry[1].split("(")[1][:-1]
            clip["title"] = entry[1].split("(")[0].rstrip()
            clippings[entry[1]] = clip

        clippings[entry[1]]["highlights"].append(entry[-1])
        string = entry[2]
        import re
        # page pattern
        pattern = re.compile(r"page \d{1,}")
        try:
            page = pattern.search(string).group().split()[1]
        except AttributeError:
            page = None
        # location pattern
        pattern = re.compile(r"location (\d{1,}-\d{1,}|\d{1,})")
        loc = pattern.search(string).group().split()[1]
        # datetime pattern
        pattern = re.compile(r"\d{1,2} \D{1,}\d{4} \d{2}\:\d{2}\:\d{2}")
        datetime = pattern.search(string).group()

        clippings[entry[1]]["loc"].append(loc)
        clippings[entry[1]]["page"].append(page)
        clippings[entry[1]]["time"].append(datetime)
        
    return clippings


def write_clippings(clippings: dict, path: str, encoding: str = "utf-8") -> None:
    """Write clippings to markdown files at given location.
    
    Args:
        clippings (dict): Dictionary containing clippings.
        path (str): Path of directory to write in.
        2
    Returns:
        None
    """
    path = Path(path)

    for key, value in tqdm(clippings.items()):
        authorpath = path / value["author"]

        # check if filepath exists, if not: mkdir
        if not os.path.isdir(authorpath):
            os.makedirs(authorpath)
        
        # clean filename of special characters
        # https://stackoverflow.com/questions/23996118/replace-special-characters-in-a-string-python#23996414
        filename = value["title"].translate(
            {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}) + ".md"
        filepath = authorpath / filename
        
        # if file does not exist, create and write book header
        if not os.path.isfile(filepath):
            with open(filepath, "wb") as file:
                title = "# " + key + "\n\n"
                file.write(title.encode(encoding))
        
        # read existing file to check for duplicate clippings later
        with open(filepath, "rb") as f:
            content = str(f.read())

        content = filepath.read_text()

        with open(filepath, "a+b") as file:  # append mode
            for page, loc, time, text in zip(value["page"], 
                                             value["loc"], 
                                             value["time"], 
                                             value["highlights"]):

                # check if clipping already in file
                if time in content:
                    continue
                
                if page:
                    header = "## Page %s | Location %s | %s \n" % (page, loc, time)
                else:
                    header = "## Location %s | %s \n" % (loc, time)

                file.write(header.encode(encoding))
                file.write(text.encode(encoding))
                file.write(b"\n \n")


if __name__ == "__main__":
    args = docopt(__doc__)  # parse docopt arguments into dict
    lines = read_clippings(args["<input>"])
    clippings = sort_clippings(lines)
    write_clippings(clippings, args["<output>"])