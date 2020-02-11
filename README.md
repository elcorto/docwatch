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

# When using terminal editors such as vim, we start that in the terminal where
# the docwatch command was used. Cool, eh? If you skip this setting, the default
# is $EDITOR.
editor=vim

# Use the system's default PDF viewer (called through xdg-open), or
# something like evince (Gnome), okular (KDE), xpdf (when you like the 90s)
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

## Dependecies

* Python
* `pandoc` and a TeX distro (e.g. `texlive` in Debian)

# Tips & Tricks

## pandoc markdown + LaTeX + Bib(La)TeX

In `pandoc`'s markdown, you can add a yaml metadata header.

```
---
bibliography: lit.bib
---

We cite a reference [@knuth1997] using the BibTeX key, which is the
same as `\cite{knuth1997}` in LaTeX.
```

You can process this by adding the
[pandoc-citeproc](https://github.com/jgm/pandoc-citeproc) filter to the config
file's filter list. When the filter is not used, the cite syntax will be just
rendered as is without error.

Note: When the bibliography file is specified by a relative path such as
`lit.bib` or `../other/dir/lit.bib`, then `docwatch` must be started from the
source file's directory such that `pandoc-citeproc` can resolve the path.
Alternatively use an absolute path.

# Related projects

Github markdown:

* https://github.com/joeyespo/grip

vim plugins:

* https://github.com/previm/previm
* https://github.com/suan/vim-instant-markdown
* https://github.com/iamcco/markdown-preview.nvim
* ... etc

What's the difference? Why this package?

* `docwatch` is independent of
    * the source file format (not only markdown, anything `pandoc` can digest)
    * the editor (vim, sublime, emacs .. whatever floats your boat)
    * the (pdf) viewer
* not yet another vim plugin (vim: good, vim bloated with a gazillion plugins: bad)
* we want PDF output instead of html (or any other output that `pandoc` can
  produce, that's a matter of adding more converters)
