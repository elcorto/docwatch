import subprocess

from .conf import conf


class PandocConverter:
    # For now pypandoc would be overkill here. Re-visit should we plan to
    # support arbitrary input and output formats. Then pypandoc's format
    # handling might come in handy.
    options = ''
    tgt_ext = None
    conf_section = 'pandoc'

    def __init__(self, src, tgt, filters=[]):
        self.src = src
        self.tgt = tgt
        self.filters = filters
        if self.tgt_ext is not None:
            assert tgt.endswith(self.tgt_ext)

    def convert(self):
        filters = " ".join(f"-F {ff}" for ff in self.filters)
        cmd = (f"pandoc {filters} {self.options} -o {self.tgt} {self.src} "
               f" > /tmp/docwatch.log 2>&1")
        subprocess.run(cmd, check=True, shell=True)


class PandocToPDFConverter(PandocConverter):
    options = f"-V documentclass=scrartcl \
                -V pagesize=a4 \
                -V colorlinks=true \
                -V linkcolor=red \
                -V urlcolor=blue \
                -V citecolor=green \
                -V link-citations=true \
                -V geometry:margin=1cm \
                "
    tgt_ext = ".pdf"

    def __init__(self, *args, **kwds):
        self.options += f"--pdf-engine={conf[self.conf_section]['pdf_engine']} "
        super().__init__(*args, **kwds)
