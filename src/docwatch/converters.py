import os
import re
from functools import cached_property

from .conf import conf
from .subproc import run_cmd


class PandocConverter:
    options = ""

    # pdf, rst, md, markdown, ..., w/o the leading "."
    tgt_ext = ""

    conf_section = "pandoc"

    def __init__(
        self, src: str, tgt: str, extra_opts: str = "", src_ext: str = ""
    ):
        self.src = src
        self.tgt = tgt
        self.extra_opts = extra_opts
        if src_ext != "":
            self.extra_opts += f" --from={src_ext}"
        if self.tgt_ext != "":
            assert tgt.endswith(self.tgt_ext)
        self.conf_dct = conf[self.conf_section]
        if self.conf_dct["citeproc"]:
            self.options += " --citeproc"

    @cached_property
    def cmd(self):
        _filters = [
            os.path.expanduser(p)
            for p in self.cv_conf["filters"].strip().split()
        ]
        filters = " ".join(f"-F {ff}" for ff in _filters)
        cmd = f"pandoc {filters} {self.options} {self.extra_opts} {self.src}"
        return re.sub(r"\s{2,}", " ", cmd.strip(), flags=re.M)

    def convert(self, onerror="log"):
        run_cmd(self.cmd, onerror=onerror)


class PandocToPDFConverter(PandocConverter):
    options = "-V documentclass=scrartcl \
               -V pagesize=a4 \
               -V colorlinks=true \
               -V linkcolor=red \
               -V urlcolor=blue \
               -V citecolor=green \
               -V link-citations=true \
               "
    tgt_ext = "pdf"

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.options += f" --pdf-engine={self.cv_conf['pdf_engine']}"
        _latex_options = self.cv_conf["latex_options"].strip().split()
        latex_options = " " + " ".join(f"-V {opt}" for opt in _latex_options)
        self.options += latex_options

        # We need to use a suffix self.tgt_ext = 'pdf' here in the PDF case
        # b/c of the quirky pandoc behavior that in order to produce a PDF by
        # running latex, we *have* to use
        #     pandoc -o foo.pdf
        # instead of the usual
        #     pandoc [-t <tgt format>] {self.src}
        self.options += f" -o {self.tgt}"
