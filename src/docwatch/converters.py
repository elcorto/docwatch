import os

from .conf import conf
from .subproc import run_cmd


class PandocConverter:
    # For now pypandoc would be overkill here. Re-visit should we plan to
    # support arbitrary input and output formats. Then pypandoc's format
    # handling might come in handy.
    options = ''
    tgt_ext = None
    conf_section = 'pandoc'

    def __init__(self, src, tgt):
        self.src = src
        self.tgt = tgt
        if self.tgt_ext is not None:
            assert tgt.endswith(self.tgt_ext)
        self.conf_dct = conf[self.conf_section]

    def convert(self):
        _filters = [os.path.expanduser(p) for p in
                    self.conf_dct['filters'].strip().split()]
        filters = " ".join(f"-F {ff}" for ff in _filters)
        cmd = f"pandoc {filters} {self.options} -o {self.tgt} {self.src}"
        run_cmd(cmd)


class PandocToPDFConverter(PandocConverter):
    options = f"-V documentclass=scrartcl \
                -V pagesize=a4 \
                -V colorlinks=true \
                -V linkcolor=red \
                -V urlcolor=blue \
                -V citecolor=green \
                -V link-citations=true \
                "
    tgt_ext = ".pdf"

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.options += f"--pdf-engine={self.conf_dct['pdf_engine']} "
        _latex_options = self.conf_dct['latex_options'].strip().split()
        latex_options = " ".join(f"-V {opt}" for opt in _latex_options)
        self.options += latex_options
