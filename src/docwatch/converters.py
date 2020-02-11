import shlex
import subprocess


class PandocConverter:
    # For now pypandoc would be overkill here. Re-visit should we plan to
    # support arbitrary input and output formats. Then pypandoc's format
    # handling might come in handy.
    options = ''
    tgt_ext = None

    def __init__(self, src, tgt, filters=[]):
        self.src = src
        self.tgt = tgt
        self.filters = filters
        if self.tgt_ext is not None:
            assert tgt.endswith(self.tgt_ext)

    def convert(self):
        filters = " ".join(f"-F {ff}" for ff in self.filters)
        cmd = f"pandoc {filters} {self.options} -o {self.tgt} {self.src}"
        subprocess.run(shlex.split(cmd), check=True)


# XXX link-citations and citecolor doesn't work
class PandocToPDFConverter(PandocConverter):
    options = '-V documentclass=scrartcl \
               -V pagesize=a4 \
               -V colorliks \
               -V linkcolor=red \
               -V urlcolor=blue \
               -V citecolor=green \
               -V link-citations=true \
               '
    tgt_ext = 'pdf'
