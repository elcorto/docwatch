import os
from functools import cached_property
from typing import Sequence
import itertools

from .conf import conf
from .subproc import run_cmd


def insert_before_each(item, lst: Sequence):
    return list(
        itertools.chain.from_iterable(zip(itertools.repeat(item), lst))
    )


class PandocConverter:
    options = []

    # pdf, rst, md, markdown, ..., w/o the leading "."
    tgt_ext = ""

    conf_section = "pandoc"

    def __init__(
        self,
        src: str,
        tgt: str,
        extra_opts: Sequence | str = [],
        src_ext: str = "",
    ):
        self.src = src
        self.tgt = tgt

        if isinstance(extra_opts, str):
            extra_opts = extra_opts.strip().split()

        self.extra_opts = extra_opts
        if src_ext != "":
            self.extra_opts += ["--from", src_ext]
        if self.tgt_ext != "":
            assert tgt.endswith(self.tgt_ext)
        self.cv_conf = conf[self.conf_section]
        if self.cv_conf.getboolean("citeproc"):
            self.options.append("--citeproc")

    @cached_property
    def cmd(self):
        filters = insert_before_each(
            "-F",
            [
                os.path.expanduser(p)
                for p in self.cv_conf["filters"].strip().split()
            ],
        )
        return (
            ["pandoc"] + filters + self.options + self.extra_opts + [self.src]
        )

    def convert(self, onerror="log"):
        run_cmd(self.cmd, onerror=onerror)


class PandocToPDFConverter(PandocConverter):
    options = insert_before_each(
        "-V",
        [
            "documentclass=scrartcl",
            "pagesize=a4",
            "colorlinks=true",
            "linkcolor=red",
            "urlcolor=blue",
            "citecolor=green",
            "link-citations=true",
        ],
    )
    tgt_ext = "pdf"

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.options += ["--pdf-engine", self.cv_conf["pdf_engine"]]
        latex_options = insert_before_each(
            "-V", self.cv_conf["latex_options"].strip().split()
        )
        self.options += latex_options

        # We need to use a suffix self.tgt_ext = 'pdf' here in the PDF case
        # b/c of the quirky pandoc behavior that in order to produce a PDF by
        # running latex, we *have* to use
        #     pandoc -o foo.pdf
        # instead of the usual
        #     pandoc [-t <tgt format>] {self.src}
        self.options += ["-o", self.tgt]
