import configparser
import copy
import os


conf_default = dict(
    DEFAULT=dict(
        editor=os.environ.get('EDITOR', 'vim'),
        pdf_viewer='xdg-open'
    ),
    pandoc=dict(
        pdf_engine='pdflatex',
        filters=[]
        )
    )

conf_fn = os.path.join(os.environ['HOME'], '.config/docwatch.conf')


def get_conf():
    if os.path.exists(conf_fn):
        cfp = configparser.ConfigParser()
        cfp.read(conf_fn)
        conf = copy.deepcopy(conf_default)
        # conf.update(cfp) is not recursive, it overwrites section dicts, need
        # to loop over sections. Also cfp.sections() excludes 'DEFAULT' b/c it
        # is "special"/"magic". Could also leave this out since all settings
        # from DEFAULT are mirrored in all other sections.
        for section in ['DEFAULT'] + cfp.sections():
            conf[section].update(cfp[section])
    else:
        conf = conf_default
    return conf

conf = get_conf()
