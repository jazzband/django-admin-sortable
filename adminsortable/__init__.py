VERSION = (1, 3, 9)  # following PEP 386
DEV_N = None


def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    return version


__version__ = get_version()
