import os
import re
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGES')).read()

with open(os.path.join(here, 'aio_forms/__init__.py')) as main_file:
    pattern = re.compile(r".*__version__ = '(.*?)'", re.S)
    VERSION = pattern.match(main_file.read()).group(1)


setup(
    name='AIO-Forms',
    version=VERSION,
    description='Async forms handling.',
    long_description=README,
    keywords='aio-forms',
    author='Vitalii Ponomar',
    author_email='vitalii.ponomar@gmail.com',
    url='https://github.com/ponomar/aio_forms',
    license='MIT',
    zip_safe=False,
    platforms='any',
    packages=find_packages(),
    py_modules=['aio_forms', 'tests'],
    install_requires=[],
    tests_require=[
        'pytest>=5.4.1',
        'pytest-asyncio>=0.11.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
)
