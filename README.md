# klip

![](https://img.shields.io/badge/python-3-blue)

A tiny Python CLI program that reads your book highlights from a connected Kindle device, sorts through the mess and organizes all clippings into per-book markdown files and saves them into author folders at a given destination folder.

## Usage

The script just needs the input file and an output folder:

```
$ python klip.py "~/Documents/kindle_highlights"

Sync complete.
Successfuly synced 22 new highlights to ~/Documents/kindle_highlights
Skipped 901 highlights already existing at ~/Documents/kindle_highlights
```

This will sort everything into this folder structure:

```
Clippings
└─── Author A
|   |   Book A1.md
|   |   Book A2.md
...
└─── Author Z
    |   Book Z1.md
```

With the markdown files being formatted as follows:

```
# What I Talk About When I Talk About Running (Haruki Murakami)

## Page 2 | Location 26-27 | 28 January 2018 22:26:17
No matter how mundane some action might appear, keep at it long enough and it becomes a contemplative, even meditative act.

...
```

The program automatically checks if highlights already exist at the destination and only appends new ones to their respective files.

## Installation

First clone this repository using git:

```
$ git clone https://github.com/alex-schaaf/klip.git
```

Then install the dependencies using either the provided `Pipfile` or manually:

### Pipenv

```
$ pip install pipenv
$ cd klip
$ pipenv install
```

And run the program

```
$ pipenv run klip.py <destination>
```

### Manual

```
$ pip install typer
```

And run the program:

```
$ python klip.py <destination>
```
