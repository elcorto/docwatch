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
  % https://github.com/elcorto/docwatch/issues/2
  \usepackage{hyperref}
  % "capitalise" is what "xnos-capitalise: true" does. If you don't use this
  % setting, then just \usepackage{cleveref}.
  \usepackage[capitalise]{cleveref}

  \usepackage{xspace}

  % only with lualatex or xelatex
  %
  % May need mathtools before unicode-math to make things like \underbrace
  % render correctly in some cases.
  %%\usepackage{mathtools}
  \usepackage{unicode-math}
  % Restore classic computer modern roman font
  \usepackage[olddefault]{fontsetup}
  \DeclareMathAlphabet{\mathcal}{OMS}{cmsy}{m}{n}

  % For \IfInteger
  \usepackage{xstring}

  % vector: bold italic (latin, greek) or slanted (digits)
  %
  % unicode-math can't do bold slanted digits, so special-case
  % \ve <digit>
  %
  % Thanks: https://tex.stackexchange.com/a/590936
  \newcommand{\ve}[1]{%
    \IfInteger{#1}{%
      \textsl{\textbf{#1}}\xspace%
      }{%
      \ensuremath{\symbfit{#1}}\xspace%
    }
  }

  % matrix: bold upright
  \newcommand{\ma}[1]{\ensuremath{\symbfup{#1}}\xspace}
  ```
---

# Images

![image w/ caption, md syntax](pic.jpg){width=50% #fig:fry-md}


Image w/o caption

![](pic.jpg){width=20%}


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


We can even leave the outer pipes off!! Also we don't need captions and labels.

a | table | w/o | outer | pipes
-|-|-|-|-
x | y | xxxxx | yyyyyyyyyyyyyyyyyyyyyyyy | zzzzzzz


# Math

We can do inline math $E = m\,c^2$ easily.

Display math with `$$...$$`:

$$E = m\,c^2$$

Also plain TeX works, awesome!

\begin{equation}
    E = m\,c^2
\end{equation}

Turn off numbering with plain TeX: use `\begin{equation*} ... \end{equation*}`.

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

Using definitions from the header.

$$\ma A\,\ve x = \ve b$$

A vector of zeros as bold and slanted digit: $\ve 0$

## Check font stuff

This

$$\underbrace{\mathcal X \rightarrow \mathbb R}_{\psi}$$

should look like +@fig:tex-screen.

![Screenshot image of rendered math with correct fonts, generated with xelatex,
unicode-math and the \TeX\ header in this file](math_fonts.png){width=20%
#fig:tex-screen}


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
