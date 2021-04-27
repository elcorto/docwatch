<p align="center">
    <img src="examples/pic.jpg" width="70%">
</p>

About
=====

Features:

* convert a source file to PDF using [pandoc] by default (which uses LaTeX)
* open rendered target (PDF) in a viewer application
* open source file in an editor
* watch source for changes and re-build automatically

Optional config file `$HOME/.config/docwatch.conf`.

The main use case of this tool is to be a previewer for text markup source
documents (e.g. markdown, rst, tex, but "any" format works, see below) that
contain some TeX math (in markdown: `pandoc`'s markdown math, or GitLab math
using a filter) in situations where you want to write text using your text
editor instead of the browser using GitHub/GitLab or hackmd/codimd. Even though
the latter two have pretty instant previews and key bindings for several
editors, it's still coding in the browser which is not fun, and you don't have
access to your editor's full config. Another use case is light technical
reports with text, code and simple math that doesn't require setting up a TeX
project.

Usage
=====

```
usage: docwatch [-h] [-p] [-c [TARGET]] [-o EXTRA_OPTS] SOURCE

positional arguments:
  SOURCE

optional arguments:
  -h, --help            show this help message and exit
  -p, --print-command   Print converter (e.g. pandoc) command that would be
                        executed and exit.
  -c [TARGET], --convert [TARGET]
                        Convert mode. Only run converter (see --print-command)
                        and produce TARGET (optional, temp file used if
                        omitted, use 'docwatch -c -- SOURCE' or 'docwatch
                        SOURCE -c' in that case).
  -o EXTRA_OPTS, --extra-opts EXTRA_OPTS
                        Additional options to pass to the converter, e.g. for
                        pandoc: docwatch -o '--bibliography=/path/to/lit.bib'
                        SOURCE. Mind the quoting.
```

This will open `foo.md` in your text editor (config file: `editor`), build a
PDF and open that in a viewer application (config file: `pdf_viewer`).

```sh
$ docwatch foo.md
```

The document is rebuilt whenever it is saved. If the source file `foo.md`
doesn't exist, it will be created. Logs are written to `/tmp/docwatch.log`
(config file: `logfile`).

You can use many formats that `pandoc` understands.

```sh
$ docwatch foo.rst
$ docwatch foo.tex
...
```

Options
-------

Print the `pandoc` command that is executed, using options from the config
file.

```sh
$ docwatch -p foo.md
pandoc -F pandoc-citeproc -V documentclass=scrartcl -V pagesize=a4 -V
colorlinks=true -V linkcolor=red -V urlcolor=blue -V citecolor=green -V
link-citations=true --pdf-engine=pdflatex -V geometry:margin=2cm,bottom=3cm -o
output.pdf foo.md
```

Although not the main use case, you can also just build the target w/o opening
the editor and viewer.

```sh
$ docwatch -c foo.pdf foo.md

# using a temp file instead of foo.pdf
$ docwatch -c -- foo.md
```

Example config file
===================

The config file is in [Python configparser / DOS ini][pyini] format. See
[examples/docwatch.conf] for all possible settings.

```dosini
[DEFAULT]

editor=vim
pdf_viewer=xdg-open

[pandoc]

filters=
    pandoc-xnos
    pandoc-citeproc

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

File formats
============

Source: We don't do source file format detection at all, the file is passed
directly to `pandoc`, as in

```sh
$ pandoc -o foo.pdf foo.md
```

Therefore, the source file can be anything `pandoc` can handle w/o specifying
`pandoc -f format`.

Target: We only do conversion to PDF.

See "Extending" below for more.

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


Filters
=======

We support [pandoc filters] (`filters` config option).

pandocfilters
-------------

The [pandocfilters][pandocfilters-gh] package has a collection of example
filter scripts. Especially the [GitLab markdown filter][pandocfilters-gh-gitlab]
lets you render [GitLab style math][gl-math]. See [examples/docwatch.conf] for how to
activate that filter. Use this to create equations on a new line (`$$...$$` in
`pandoc` markdown and LaTeX)

    ```math
    E = m\,c^2
    ```

or this quirky syntax (note the backticks in ``$`...`$``, `$...$` in `pandoc`
markdown and LaTeX) for inline.

    $`E= m\,c^2`$

GitHub does not support math in markdown at all, AFAIK.

Note that the Debian package `python3-pandocfilters` as well as the `pip`
package `pandocfilters` don't contain the GitLab filter for some reason
(packaging bug?), so make sure to grab the GitHub version.

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
$$\alpha = \int\sin(x)\,\Gamma(\phi)\,d\phi$$ {#eq:foo}

which we can reference in @eq:foo.
```

Also works for figures `{#fig:foo}` and tables `{#tbl:foo}`.

Both filters have slightly different syntax, but the example here should work
in both. We recommend `pandoc-xons`, which has nice support for naming
references automatically, e.g. `+@eq:foo` becomes "eq. 1" instead just "1".

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

When none of `pandoc-citeproc` or the `pandoc-xnos` filters are used, then
cite/ref syntax such as `[@knuth1997]` `+@eq:foo` is just rendered as is
without error.

pandoc-citeproc & bibliography
------------------------------

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

Converting LaTeX source files
-----------------------------

Is it possible to build LaTeX? Sure, since we support everything `pandoc` can,
for a single, self-contained TeX file just do

```sh
$ docwatch foo.tex
```

which will use `pandoc -o foo.pdf foo.tex`. However, TeX projects
usually have a `main.tex` and many source files included in main, so the
`docwatch` model (open and render one single file) doesn't apply here. In this
case, it makes sense use something like [latexmk] with make-like behavior to
watch all `*.tex` files. Furthermore, [latexmk] has its own preview mode
(`latexmk -pvc`)!

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

A short Makefile can be handy as well, for instance when using the [minted]
source code highlighter.

```make
all:
    # --shell-escape b/c of minted package
    latexmk -pdf -pvc -pdflatex="pdflatex --shell-escape %O %S" main.tex

clean: _restclean
    latexmk -c

allclean: _restclean
    latexmk -C

_restclean:
    rm -rf _minted-*
    rm -f *.bak
```

Related projects
================

Github markdown:

* <https://github.com/joeyespo/grip>

vim plugins:

* <https://github.com/previm/previm>
* <https://github.com/suan/vim-instant-markdown>
* <https://github.com/iamcco/markdown-preview.nvim>
* ... etc

Why this package?
-----------------

* `docwatch` is independent of
    * the source file format (not only markdown, anything `pandoc` can digest
      (w/o `-f format`))
    * the editor (stand-alone tool, not yet another vim plugin, config file:
      `editor`)
    * the viewer (config file: `pdf_viewer`)
* PDF output
* support for pandoc filters enables basic TeX features w/o writing TeX

Extending
=========

* any output other than PDF that `pandoc` can produce can be added by adding
  more converters (see [converters.py])
* one can also define converters that *don't use pandoc at all* and thus make
  `docwatch` independent of `pandoc` ... but it is pretty powerful, so there is
  really no ned to do that
* one can easily add a feature to pass `-f format` to `pandoc` but ATM we don't
  need that (using mainly md, tex (single file), rst)


[pandoc-citeproc]: https://github.com/jgm/pandoc-citeproc
[pandoc-crossref]: https://github.com/lierdakil/pandoc-crossref
[pandoc-xons]: https://github.com/tomduck/pandoc-xnos
[latexmk]: https://mg.readthedocs.io/latexmk.html
[converters.py]: https://github.com/elcorto/docwatch/blob/master/src/docwatch/converters.py
[pandoc]: https://pandoc.org
[examples/md.md]: https://github.com/elcorto/docwatch/blob/master/examples/md.md
[examples/docwatch.conf]: https://github.com/elcorto/docwatch/blob/master/examples/docwatch.conf
[pyini]: https://docs.python.org/3.8/library/configparser.html
[minted]: https://www.ctan.org/pkg/minted
[pandoc filters]: https://pandoc.org/filters.html
[pandocfilters-gh]: https://github.com/jgm/pandocfilters
[pandocfilters-gh-gitlab]: https://github.com/jgm/pandocfilters/blob/master/examples/gitlab_markdown.py
[gl-math]: https://docs.gitlab.com/ee/user/markdown.html#math
