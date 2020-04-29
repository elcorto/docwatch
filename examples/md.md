---
bibliography: lit.bib
reference-section-title: Refs
---

# Images

![image w/ caption](pic.jpg){width=50%}

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

Table: caption 1


We can even leave the outer pipes off!!

a | table | w/o | outer | pipes
-|-|-|-|-
x | y | xxxxx | yyyyyyyyyyyyyyyyyyyyyyyy | zzzzzzz

Table: caption 2

# Math

We can do inline math $E = m\,c^2$ easily.

Display math with `$$...$$`:

$$E = m\,c^2$$

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

$$E = m\,c^2$$ {#eq:foo}

`pandoc-xnos` labels like `{#eq:foo}` only work for `$$...$$` style math, not GitLab
style.

We can reference equations using `{@eq:foo}` {@eq:foo} or `@eq:foo` @eq:foo or
`{+@eq:foo}` {+@eq:foo} or `+@eq:foo` +@eq:foo.

Using inline math but with labels

$E = m\,c^2$ {#eq:some-math}

is treated like display style math

$$E = m\,c^2$$ {#eq:some-math}

The `+@eq:foo` syntax with `+` works only with `pandoc-xnos`. In
`pandoc-crossref`, you need to use an uppercase first letter `@Eq:foo`.

a|b
-|-
c|d

Table: table with label {#tbl:table1}

![small image with label](pic.jpg){width=20% #fig:figure1}

We can also cite tables (see +@tbl:table1) and figures (+@fig:figure1).

# BibTeX

Using `pandoc-citeproc`, we cite [@focker_2019].
