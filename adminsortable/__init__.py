VERSION = (1, 7, 1)  # following PEP 386
DEV_N = None


def get_version():
    version = '{}.{}'.format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '{}.{}'.format(version, VERSION[2])
    try:
        if VERSION[3]:
            version = '{}.{}'.format(version, VERSION[3])
    except IndexError:
        pass
    return version


__version__ = get_version()
