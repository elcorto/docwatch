<p align="center">
    <img src="examples/pic.jpg" width="70%">
</p>

About
=====

Features:

* convert a source file to PDF using [pandoc] by default (which uses LaTeX)
* open rendered target (PDF temp file) in a viewer application
* open source file in an editor
* watch source for changes and re-build automatically

Optional config file `$HOME/.config/docwatch/docwatch.conf`.

The main use case of this tool is to be a previewer for text markup source
documents (e.g. markdown, rst, tex, .. any format that `pandoc` supports) that
contain some TeX math (in markdown: `pandoc`'s markdown math, or GitLab math
using a filter) in situations where you want to write text using your text
editor instead of the browser using GitHub/GitLab or [hackmd]/[hedgedoc]. Even though
the last two have pretty instant previews and key bindings for several
editors, it's still coding in the browser which is not fun, and you don't have
access to your editor's full config. Another use case is light technical
reports with text, code and simple math that don't justify setting up a TeX
project.

Usage
=====

```
usage: docwatch [-h] [-p] [-c [TARGET]] [-o EXTRA_OPTS] [-f SOURCE_FORMAT]
                [SOURCE_FILE]

positional arguments:
  SOURCE_FILE

options:
  -h, --help            show this help message and exit
  -p, --print-command   Print converter (e.g. pandoc) command that would be
                        executed and exit.
  -c [TARGET], --convert [TARGET]
                        Convert mode. Only run converter (see --print-command)
                        and produce TARGET (optional, temp file used if
                        omitted, use 'docwatch -c -- SOURCE_FILE' or 'docwatch
                        SOURCE_FILE -c' in that case).
  -o EXTRA_OPTS, --extra-opts EXTRA_OPTS
                        Additional options to pass to the converter, e.g. for
                        pandoc: docwatch -o '--bibliography=/path/to/lit.bib'
                        SOURCE_FILE. Mind the quoting. Some shells mess up
                        quoting, then use an equal sign: -o='...' or --extra-
                        opts='...'.
  -f SOURCE_FORMAT, --source-format SOURCE_FORMAT
                        Format of SOURCE_FILE (file type, typically file
                        extension). Same as docwatch --extra-opts='-f
                        SOURCE_FORMAT'. Passed to pandoc (-f/--from) if used.
                        Else (default) we use pandoc's automatic detection.
                        Use in combination with omitted SOURCE_FILE, e.g.
                        "docwatch -f rst" to edit a temp rst file.
```

This will open `foo.md` in your text editor (config file: `editor`), build a
PDF (temp file) and open that in a viewer application (config file: `pdf_viewer`).

```sh
$ docwatch foo.md
```

The document is rebuilt whenever it is saved. If the source file `foo.md`
doesn't exist, it will be created. Logs are written to `/tmp/docwatch.log`
(config file: `logfile`).

You can use many formats that `pandoc` understands automatically.

```sh
$ docwatch foo.md
$ docwatch foo.rst
$ docwatch foo.tex
...
```

Or specify the format explicitly (as in `pandoc -f markdown`).

```sh
$ docwatch -f markdown foo
```

If you just want to quickly create a text snippet *without specifying and
saving* the source file, use

```sh
$ docwatch
```

without arguments. This will use a temp source file (default: markdown). Use
`-f` to specify the format.

```sh
$ docwatch -f rst
```

Print the `pandoc` command that is executed, which includes all options defined
in the config file.

```sh
$ docwatch -p foo.md
pandoc -F pandoc-xnos -V documentclass=scrartcl -V pagesize=a4 -V
colorlinks=true -V linkcolor=red -V urlcolor=blue -V citecolor=green -V
link-citations=true --pdf-engine=xelatex -V geometry:margin=2cm,bottom=3cm
--citeproc -o TARGET.pdf foo.md
```

Less important options
----------------------

Although not the main use case, you can also just build the target w/o opening
the editor and viewer, which means all we do is use the `pandoc` command (see
`docwatch -p`) to built the target PDF.

```sh
$ docwatch -c foo.pdf foo.md
```

You may use `-c` without specifying a target file.

```sh
$ docwatch -c -- foo.md
$ docwatch foo.md -c
```

In this case a temp target file will be used (which you won't see). Use this to
check if the build works without opening the source in an editor and the target
in a pdf viewer.

A funny edge case:

```sh
$ docwatch -c
```

This again won't open editor and viewer and will not produce any file on disk.
It will use a temp source and target file, build the target file and then
delete both again (since they are temp files).


Example config file
===================

The config file is in [Python configparser / DOS ini][pyini] format. See
[examples/docwatch.conf] for all possible settings.

```dosini
[DEFAULT]

editor=vim
pdf_viewer=xdg-open

# File with text to be included at the start of a new file. Optional.
##template_file=/path/to/template.yml

[pandoc]

filters=
    pandoc-xnos

# default
##citeproc=true

latex_options=
    geometry:margin=1.5cm
    pagestyle=empty
```

Error handling
==============

When you start `docwatch`, build errors are dumped to the terminal and we exit.
Once the initial build passed and your editor is open, all further (`pandoc`
and LaTeX) errors are logged to `logfile`, else the terminal error log would
mess up editors such as `vim`.

Therefore, when you change something in `foo.md`, save the file, but the PDF is
not being rebuilt, then you probably made a (LaTeX) mistake, which made the
`pandoc` command fail. Then look into `logfile`. Check the time stamp in
`logfile` to make sure the error is related to the last change to the source
file.


Install
=======

```sh
$ git clone ...
$ pip install -e .
```

Also install all `pandoc-xnos` filters:

```sh
$ pip install -e ".[filters-xnos]"
```

Dependencies
------------

* Python
* `pandoc`
* a TeX distro (e.g. `texlive` in Debian)


Filters
=======

We support [pandoc filters] (`filters` config option), which are executables
that process text. From the `pandoc` docs:

A "filter" is a program that modifies the AST, between the reader and the writer.

```
INPUT --reader--> AST --filter--> AST --writer--> OUTPUT
```

pandocfilters package
---------------------

The [pandocfilters][pandocfilters-gh] package has a collection of example
filter scripts.

Use

```dosini
[pandoc]

filters=
    /path/to/pandocfilters/examples/gitlab_markdown.py
    other-filter-here
```

in `docwatch.conf` to activate them.

Especially the [GitLab markdown filter][pandocfilters-gh-gitlab] lets you
render [GitLab style math][gl-math].

See also [examples/docwatch.conf].

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

You can process this by setting the `pandoc.citeproc=true` option in the
config file, which will imply [`pandoc --citeproc`][citeproc].


Cross-references
----------------

There are at least two filters ([pandoc-crossref], [pandoc-xons]) for doing
cross-referencing.

```
Here be math

$$\alpha = \int\sin(x)\,\Gamma(\phi)\,d\phi$$ {#eq:foo}

which we can reference in @eq:foo.
```

Also works for figures `{#fig:foo}` and tables `{#tbl:foo}`.

Both filters have slightly different syntax, but the example here should work
in both. We recommend `pandoc-xons`, which has nice support for naming
references automatically, e.g. `+@eq:foo` becomes "eq. 1" instead of just "1".

Please see also [examples/md.md] for much more, such as customizations
settings in the metadata header (e.g. `xnos-capitalise`).

Install the complete `pandoc-xons` family of filters with `pip install
pandoc-eqnos pandoc-fignos pandoc-secnos pandoc-tablenos pandoc-xnos`. You can
leave out any package (e.g. `pandoc-secnos` if you don't want section labels)
and still use `pandoc-xnos` as a filter, which will use all installed
functionality.


Notes
=====

New / empty source files
------------------------

When `pandoc` is given an empty file, it just produces an empty file, no matter
what the target format is. Some tools such as LaTeX don't react too well to
empty files. For this reason we add a dummy line to the source file should it
not exist.

Missing filters
---------------

When the option `pandoc.citeproc=false` and the `pandoc-xnos` filters are
*not* used, then cite/ref syntax such as `[@knuth1997]` `+@eq:foo` is just
rendered as is without error.

`pandoc --citeproc` & bibliography
----------------------------------

When the bibliography file is specified by a relative path such as `lit.bib` or
`../other/dir/lit.bib`, then `docwatch` must be started from the source file's
directory such that `pandoc --citeproc` can resolve the path (at least when using
LaTeX under the hood). Alternatively use an absolute path. The same goes for
image paths, by the way.

Using many filters to replicate LaTeX functionality
---------------------------------------------------

While this works and is kind of fun, don't get too crazy in terms of using
filters. If you find yourself wanting to replace much of, say TeX Live, with a
pile of `pandoc` filters, then you should stop and write your document in TeX.

Converting LaTeX source files
-----------------------------

Is it possible to build LaTeX? Sure, since we support everything `pandoc` can,
for a single, self-contained TeX file just do

```sh
$ docwatch foo.tex
```

which will use `pandoc -o foo.pdf foo.tex`. However, TeX projects usually have
a `main.tex` and many source files included in main, so the `docwatch` model
(open and render one single file) doesn't apply here. In this case, it makes
sense to use something like [latexmk] with make-like behavior to watch all
`*.tex` files. Furthermore, [latexmk] has its own preview mode (`latexmk
-pvc`)!

You may need to define the pdf viewer:

```
# ~/.config/latexmk/latexmkrc
$pdf_previewer = 'okular %S'
```

Then the workflow is almost as with `docwatch`:

```sh
# watch main.tex and all dependencies, start pdf_previewer application
$ latexmk -pdf -pvc main.tex

# edit one of the project files
$ vim src/chapter_foo.tex
```

A short `Makefile` and a `.latexmkrc` can be handy as well, for instance when
using the [minted] source code highlighter.

`.latexmkrc`:

```perl
# run bibtex or biber, clean up .bbl files
$bibtex_use = 2;

# latexmk -pdf
$pdf_mode = 1;

# --shell-escape b/c of minted package
# xelatex b/c of font stuff
$pdflatex = "xelatex -interaction=errorstopmode -file-line-error -shell-escape %O %S";

push @generated_exts, "bak", "bbl", "run.xml", "nav", "snm", "vrb", "synctex.*"
```

`Makefile`:

```make
main=main.tex

# Default
all: $(main)
    latexmk $<

# Build, watch, rebuild and open target in PDF viewer.
preview: $(main)
    latexmk -pvc $<

# Cleanup
clean: _restclean
    latexmk -c

allclean: _restclean
    latexmk -C

# Seems like latexmk's "push @generated_exts" doesn't treat directories.
_restclean:
    rm -rf _minted-*
```

Related projects
================

html preview

* [hedgedoc]/[hackmd]
* <https://github.com/joeyespo/grip> (GitHub MD flavor)
* <https://github.com/crdx/docwatch>  (the name seems to be popular :))

vim plugins:

* <https://github.com/previm/previm>
* <https://github.com/suan/vim-instant-markdown>
* <https://github.com/iamcco/markdown-preview.nvim>
* ... etc

Why this package?
-----------------

* `docwatch` is independent of
    * the source file format: not only markdown, anything `pandoc` can digest
    * the editor: stand-alone tool, not yet another vim plugin, config file:
      `editor`
    * the viewer: config file: `pdf_viewer`
* PDF output
* support for pandoc filters

Extending
=========

* any output other than PDF that `pandoc` can produce can be added by adding
  more converters (see [converters.py])
* one can also define converters that *don't use pandoc at all* and thus make
  `docwatch` independent of `pandoc` ... but it is pretty powerful, so there is
  really no need to do that


[pandoc-crossref]: https://github.com/lierdakil/pandoc-crossref
[pandoc-xons]: https://github.com/tomduck/pandoc-xnos
[latexmk]: https://mg.readthedocs.io/latexmk.html
[converters.py]: https://github.com/elcorto/docwatch/blob/main/src/docwatch/converters.py
[pandoc]: https://pandoc.org
[examples/md.md]: https://github.com/elcorto/docwatch/blob/main/examples/md.md
[examples/docwatch.conf]: https://github.com/elcorto/docwatch/blob/main/examples/docwatch.conf
[pyini]: https://docs.python.org/3/library/configparser.html
[minted]: https://www.ctan.org/pkg/minted
[pandoc filters]: https://pandoc.org/filters.html
[pandocfilters-gh]: https://github.com/jgm/pandocfilters
[pandocfilters-gh-gitlab]: https://github.com/jgm/pandocfilters/blob/master/examples/gitlab_markdown.py
[gl-math]: https://docs.gitlab.com/ee/user/markdown.html#math
[hedgedoc]: https://hedgedoc.org
[hackmd]: https://hackmd.io
[citeproc]: https://pandoc.org/MANUAL.html#citations
