import configparser
import copy
import os


conf_default = configparser.ConfigParser()

# configparser magic: settings from the DEFAULT section are mirrored in all
# other sections, and can be overwritten there if needed. That's why
# conf_default.sections() only returns ['pandoc'] .
conf_default['DEFAULT'] = dict(
    editor=os.environ.get('EDITOR', 'vim'),
    pdf_viewer='xdg-open'
    )

conf_default['pandoc'] = dict(
        pdf_engine='pdflatex',
        filters=[]
        )

conf_fn = os.path.join(os.environ['HOME'], '.config/docwatch.conf')


def get_conf():
    if os.path.exists(conf_fn):
        cfp = configparser.ConfigParser()
        cfp.read(conf_fn)
        conf = copy.deepcopy(conf_default)
        for section in cfp.sections():
            conf[section].update(cfp[section])
    else:
        conf = conf_default
    return conf

conf = get_conf()
