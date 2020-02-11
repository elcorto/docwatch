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

Currently we only do conversion to PDF. The source file can be anything `pandoc`
can handle. We don't do source file format detection at all, the file is passed
directly to `pandoc`, as in

```sh
$ pandoc [options] -o foo.pdf foo.md
```

# Install

```sh
$ git clone ...
$ pip install -e .
```

# Tips & Tricks

## pandoc markdown + LaTeX + Bib(La)TeX

In `pandoc`'s markdown, you can add a yaml metadata header

```
---
bibliography: lit.bib
---

Normal *awesome* markdown content here. We cite a paper here using the BibTeX
key like so [@knuth1997], which is the same as `\cite{knuth1997}` in LaTeX.
```

You can process this by adding the
[pandoc-citeproc](https://github.com/jgm/pandoc-citeproc) filter to the config
file's filter list. When the filter is not used, the cite syntax will be just
rendered as is, there is no error produced.

Note: When the bibliography file is specified as a relative path such as
`lit.bib` or `../other/dir/lit.bib`, then `docwatch` must be started from the
source file's directory such that `pandoc-citeproc` can resolve the path.
Alternatively use an absolute path.

# Related projects

* https://github.com/previm/previm
* https://github.com/suan/vim-instant-markdown
* https://github.com/iamcco/markdown-preview.nvim
* ... etc

What's the difference? Why this package?

* not yet another vim plugin
* independent of the editor and the viewer, both of which can be freely configured
* we want PDF output instead of html (or any other output that `pandoc` can
  produce, that's a matter of adding more converters)
* only dependency is `pandoc`
