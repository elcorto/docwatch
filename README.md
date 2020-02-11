# About

Convert source file (e.g. a markdown file) to PDF using `pandoc`, open in viewer
program, watch source for changes and re-build automatically. Optional config
file `$HOME/.config/docwatch.conf`.

# Usage

This will open the built PDF in a viewer.

```sh
$ docwatch foo.md
```

Open `foo.md` in your text editor (see config file below) as well.

```sh
$ docwatch -e foo.md
```

# Example config file

```
[DEFAULT]

# some text editor that opens a GUI window
editor=xvim

pdf_viewer=xdg-open

# pandoc filters, one per line, will be passed as
#   pandoc -F filter1 -F filter2 ...
# Each one is expected to be an executable. If no path is given, the executable
# is assumed to be on $PATH.
filters=
    /path/to/pandocfilters/examples/gitlab_markdown.py
    pandoc-citeproc
```

# File formats

Currently we only do conversion to PDF. Source file can be anything `pandoc`
can handle. We don't do source file format detection at all, the file is passed
diectly to pandoc, as in

```sh
$ pandoc [options] -o foo.pdf foo.md
```

# Install

```sh
$ git clone ...
$ pip install -e .
```
