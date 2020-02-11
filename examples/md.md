---
bibliography: lit.bib
reference-section-title: Refs
---

# Images

![image w/ caption](pic.jpg){width=50%}

# Indented code blocks

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

# Fenced code blocks

```
fenced
    code
```

`inline code`

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

We can do inline math inline math $\pi\,\sin(x)$ easily.

Display math with `$$...$$`:

$$E = m\,c^2$$ {#eq:foo}

$$
    \Phi = \int_\infty^\Omega \sin x\,\text{d}x
$$ {#eq:bar}

GitLab style math here. Cannot use pandoc-xnos/pandoc-crossref `{#eq:foo}` labels here,
though. Works only for `$$...$$`.

```math
E = m\,c^2;\:
\Phi = \int_\infty^\Omega \sin x
```

## Equation labels and refs

pandoc-xnos: using

    $inline math but with labels$ {#eq:some-math}

is treated like

    $$display style math$$ {#eq:some-math}

Using references: {@eq:foo} or @eq:foo and {+@eq:bar} or +@eq:bar. Of course
the `{+@eq:bar}` syntax with `+` works only with pandoc-xnos. In
pandoc-crossref, you need to use an uppercase first letter `@Eq:bar` .. well
allright.

# BibTeX

Using pandoc-citeproc, we cite [@focker_2019].
