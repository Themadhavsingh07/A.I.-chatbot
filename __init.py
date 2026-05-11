# don't import any costly modules
import sys
import os


is_pypy = '__pypy__' in sys.builtin_module_names


def warn_distutils_present():
    if 'distutils' not in sys.modules:
        return
    if is_pypy and sys.version_info < (3, 7):
        # PyPy for 3.6 unconditionally imports distutils, so bypass the warning
        # https://foss.heptapod.net/pypy/pypy/-/blob/be829135bc0d758997b3566062999ee8b23872b4/lib-python/3/site.py#L250
        return
    import warnings

    warnings.warn(
        "Distutils was imported before Setuptools, but importing Setuptools "
        "also replaces the `distutils` module in `sys.modules`. This may lead "
        "to undesirable behaviors or errors. To avoid these issues, avoid "
        "using distutils directly, ensure that setuptools is installed in the "
        "traditional way (e.g. not an editable install), and/or make sure "
        "that setuptools is always imported before distutils."
    )


def clear_distutils():
    if 'distutils' not in sys.modules:
        return
    import warnings

    warnings.warn("Setuptools is replacing distutils.")
    mods = [
        name
        for name in sys.modules
        if name == "distutils" or name.startswith("distutils.")
    ]
    for name in mods:
        del sys.modules[name]


def enabled():
    """
    Allow selection of distutils by environment variable.
    """
    which = os.environ.get('SETUPTOOLS_USE_DISTUTILS', 'local')
    return which == 'local'


def ensure_local_distutils():
    import importlib
