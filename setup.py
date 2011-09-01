from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except:
    README = None

setup(
    name='django-admin-sortable',
    version=__import__('adminsortable').__version__,
    description='Drag and drop sorting for models and tabular inline models in Django admin',
    long_description=README,
    author='Brandon Taylor',
    author_email='btaylorweb@gmail.com',
    url='http://btaylorweb.com/',
    packages=find_packages(exclude=['sample_project']),
    zip_safe=False,
    include_package_data=True,
    classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)
