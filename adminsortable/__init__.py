VERSION = (2, 0, 20)
DEV_N = None


def get_version():
    version = '{0}.{1}'.format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '{0}.{1}'.format(version, VERSION[2])
    try:
        if VERSION[3]:
            version = '{0}.{1}'.format(version, VERSION[3])
    except IndexError:
        pass
    return version


__version__ = get_version()
