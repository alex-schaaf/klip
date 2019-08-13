# klip

![](https://img.shields.io/badge/python-3-blue)

A simple Python script that reads in a Kindle clippings text file, sorts through the mess and organizes all clippings into per-book markdown files and saves them into author folders. 

## Usage

The script just needs the input file and an output folder:

```
$ python klip.py "./clippings.txt" "./Documents/Clippings"

100%|███████████████████████████████████████████████| 23/23
```

This will sort everything into the folder structure below:

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

The script automatically checks if clippings already exists and only appends new ones to their respective files.

## Dependencies

* `tqdm`
* `docopt`

```
$ pip install tqdm docopt
```