from setuptools import setup, find_packages

try:
    README = open('README').read()
except:
    README = None

setup(
    author='Brandon Taylor',
    author_email='alsoicode@gmail.com',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Topic :: Utilities'],
    description='Drag and drop sorting for models and inline models in Django admin.',
    include_package_data=True,
    install_requires=['django'],
    license='APL',
    long_description=README,
    name='django-admin-sortable',
    packages=find_packages(exclude=['sample_project']),
    url='https://github.com/iambrandontaylor/django-admin-sortable',
    version=__import__('adminsortable').__version__,
    zip_safe=False
)
