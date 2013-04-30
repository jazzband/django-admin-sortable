VERSION = (1, 4, 5, 1)  # following PEP 386
DEV_N = None


def get_version():
    version = '{0}.{1}'.format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '{0}.{1}'.format(version, VERSION[2])
    if VERSION[3]:
        version = '{0}.{1}'.format(version, VERSION[3])
    return version


__version__ = get_version()
