---
bibliography: lit.bib
reference-section-title: Refs
csl: ieee-with-url.csl
link-citation: true

xnos-capitalise: true
tablenos-plus-name: Tab.

header-includes:
- |
  ```{=latex}
  \usepackage{bm}
  \usepackage{xspace}
  \newcommand{\ve}[1]{\ensuremath{\bm{\mathit{#1}}}\xspace}
  ```
---

# Images

![image w/ caption, md syntax](pic.jpg){width=50% #fig:fry-md}


\begin{figure}
    \centering
    \includegraphics[width=0.3\textwidth]{pic.jpg}
    \caption{We can use plain TeX as welll!11!!!}
    \label{fig:fry-tex}
\end{figure}

# Code

## Indented blocks

text start 1

    code block
    newline before
        and after

text end 1


text start 2
    This is not a code block since it doesn't
    start with a newline
text end 2


text start 3

    code block
    newline
        before
text end 3


text start 4
    This is not a code block since it doesn't
    start with a newline.

text end 4


## Inline

`inline code`

## Fenced code blocks

```
# fenced code
for i in range(foo):
    print(i)
```

```py
# fenced code with highlighting
for i in range(foo):
    print(i)
```

```sh
for fn in foo bar; do
    tail $fn
done
```

# Bullet lists

* L1
  aaaaa
  bbbbb
    * L2
      ccccccc
      ddddddd
        * L3
          eeeee
          fffff
            * L4
              gggggg
              hhhhhh
    * iiiiii
      jjjjjj
      kkkkkkk
      lllll

# Tables

Table markup doesn't need to match column width as in rst. Nice!

| a | table |
|-|-|
|col 1| col 2    |

Table: caption 1 {#tbl:table_with_outer}


We can even leave the outer pipes off!!

a | table | w/o | outer | pipes
-|-|-|-|-
x | y | xxxxx | yyyyyyyyyyyyyyyyyyyyyyyy | zzzzzzz

Table: caption 2 {#tbl:table_no_outer}

Note however that since some `pandoc-xnos` version (checked 2023-07), tables
and figures *must* have a caption *and* a label, else the build fails.

# Math

We can do inline math $E = m\,c^2$ easily.

Display math with `$$...$$`:

$$E = m\,c^2$$

Also plain TeX works, awesome!

\begin{equation}
    E = m\,c^2
\end{equation}

Turn off numbering.

\begin{equation*}
    E = m\,c^2
\end{equation*}

GitLab style fenced math works when you use [the matching
filter](https://github.com/jgm/pandocfilters/blob/master/examples/gitlab_markdown.py).

```math
E = m\,c^2
```

If not then this will be a fenced code block.

```
E = m\,c^2
```

# Labels and references

We recommend `pandoc-xnos`.


## Equations

Using inline math `$...$` but with labels

$E = m\,c^2$ {#eq:some-math}

is treated like display style math `$$...$$`

$$E = m\,c^2$$ {#eq:foo}

`pandoc-xnos` labels like `{#eq:foo}` only work for `$$...$$` style math, not GitLab
style.


## Tables and figures

a|b
-|-
c|d

Table: table with label {#tbl:a_table}

![small image with label and citation [@focker_2019]](pic.jpg){width=20% #fig:fry-md-small}


## Ref syntax

The prefixes `eq:`, `fig:` and `tbl:` are mandatory.

ref syntax | result
-|-
`{@eq:foo}`             | {@eq:foo}
`@eq:foo`               | @eq:foo
`+@eq:foo`              | +@eq:foo
`*@eq:foo`              | *@eq:foo
|
`+@fig:fry-md`          | +@fig:fry-md
`+@fig:fry-tex`         | +@fig:fry-tex
`+@fig:fry-md-small`    | +@fig:fry-md-small
|
`+@tbl:a_table`         | +@tbl:a_table

Table: ref syntax xnos {#tbl:ref_syntax_xnos}

## "plus syntax"

Customizations set in metadata block:

* `xnos-capitalise: true`: "eq. 3" -> "Eq. 3"
* `tablenos-plus-name: Tab`: "Table 3" -> "Tab. 3"

The `+@eq:foo` syntax with `+` works only with `pandoc-xnos`. In
`pandoc-crossref`, you need to use an uppercase first letter `@Eq:foo`.


# BibTeX

Using `pandoc --citeproc`:

ref syntax | result
-|-
`[@focker_2019]`            | [@focker_2019]
|
`[@focker_2019;@doe_2021]`  | [@focker_2019;@doe_2021]
|
`[@focker_2019 23]`         | [@focker_2019 23]
`[@focker_2019 p. 23]`      | [@focker_2019 p. 23]
`[@focker_2019, 23]`        | [@focker_2019, 23]
`[@focker_2019, p. 23]`     | [@focker_2019, p. 23]
|
`[@focker_2019 Sec. 42]`    | [@focker_2019 Sec. 42]
`[@focker_2019 sec. 42]`    | [@focker_2019 sec. 42]
`[@focker_2019 s. 42]`      | [@focker_2019 s. 42]
|
`[@focker_2019 ch. 42]`     | [@focker_2019 ch. 42]
|
`[@focker_2019; Sec. 42]`   | [@focker_2019; Sec. 42]
`[@focker_2019; 23]`        | [@focker_2019; 23]
`[@focker_2019; arb. text]` | [@focker_2019; arb. text]

Table: ref syntax citeproc {#tbl:ref_syntax_citeproc}
