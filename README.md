About
=====

Convert a source file (e.g. markdown) to PDF using `pandoc`, open in a viewer
application, watch source for changes and re-build automatically. Optional
config file `$HOME/.config/docwatch.conf`.

Usage
=====

This will open `foo.md` in your text editor, as well as the built PDF in a
viewer application.

```sh
$ docwatch foo.md
```

If the source file `foo.md` doesn't exist, it will be created. Logs are written
to `/tmp/docwatch.log`.

Example config file
===================

```dosini
[DEFAULT]

# When using terminal editors such as vim, we start that in the terminal where
# the docwatch command was used. Cool, eh? If you skip this setting, the default
# is $EDITOR.
editor=vim
##editor=gvim
##editor=emacs

pdf_viewer=xdg-open
##pdf_viewer=okular
##pdf_viewer=evince
##pdf_viewer=xpdf

[pandoc]

# slow, but can deal with weird font situations
##pdf_engine=xelatex
# pandoc default
pdf_engine=pdflatex

# pandoc filters, one per line, will be passed as
#   pandoc -F filter1 -F filter2 ...
# Each one is expected to be an executable. If no path is given, the executable
# is assumed to be on $PATH.
#
# pandoc-citeproc must be listed after pandoc-xnos
# https://github.com/tomduck/pandoc-eqnos#usage
filters=
    /path/to/pandocfilters/examples/gitlab_markdown.py
##    pandoc-xnos
    pandoc-citeproc

# pandoc -V option1 -V option2
latex_options=
    geometry:margin=1.5cm
    pagestyle=empty
```

File formats
============

Currently we only do conversion to PDF. The source file can be anything `pandoc`
can handle. We don't do source file format detection at all, the file is passed
directly to `pandoc`, as in

```sh
$ pandoc [options] -o foo.pdf foo.md
```

Install
=======

```sh
$ git clone ...
$ pip install [-e] .
```

Dependencies
------------

* Python
* `pandoc`
* a TeX distro (e.g. `texlive` in Debian)


Tips & Tricks
=============

Bib(La)TeX
----------

In `pandoc`'s markdown, you can add a yaml metadata header, where you can
specify a BibTeX database file (or use `--bibliography`).

```
---
bibliography: lit.bib
---

We cite a reference [@knuth1997] using the BibTeX key, which is the
same as `\cite{knuth1997}` in LaTeX.
```

You can process this by adding the [pandoc-citeproc] filter to the config
file's filter list.


Cross-references
----------------

There are at least two filters ([pandoc-crossref], [pandoc-xons]) for doing
cross-referencing.

```
Here be math
$$\alpha = \int\sin(x)\,\Gamma(\phi)\,d\phi$$ {#eq:alpha}

which we can reference in @eq:alpha.
```

Both filters have slightly different syntax, but the example here should work
in both.

See also `examples/md.md` for more.

Notes
=====

New / empty source files
------------------------

When `pandoc` is given an empty file, it just produces an empty file, no matter
what the target format is. Some tools such as LaTeX don't react too well to
empty files. For this reason we add a dummy line to the source file should it
not exist.

pandoc-citeproc & bibliography
------------------------------

When the filter `pandoc-citeproc` is not used, the cite syntax will be just
rendered as is without error.

When the bibliography file is specified by a relative path such as `lit.bib` or
`../other/dir/lit.bib`, then `docwatch` must be started from the source file's
directory such that `pandoc-citeproc` can resolve the path (at least when using
LaTeX under the hood). Alternatively use an absolute path. The same goes for
image paths, by the way.

Using many filters to replicate LaTeX functionality
---------------------------------------------------

While this works and is kind of fun, don't get too crazy in terms of using
filters. If you find yourself wanting to replace much of, say TeX Live, with a
pile of `pandoc` filters, then you should stop and write your document in TeX.

Related projects
================

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
    * the editor
    * the (pdf) viewer
* stand-alone tool, not yet another vim plugin
* PDF output
* any other output that `pandoc` can produce can be added by adding more
  converters
* one can also define converters that don't use pandoc at all (see
  `converters.py`)


[pandoc-citeproc]: https://github.com/jgm/pandoc-citeproc
[pandoc-crossref]: https://github.com/lierdakil/pandoc-crossref
[pandoc-xons]: https://github.com/tomduck/pandoc-xnos
