"""A setuptools based setup module.
Based on: https://github.com/pypa/sampleproject/blob/90d44abe361688aba5a189e661423863b34f5208/setup.py
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

pkg_req = [
    'requests>=2.25.0'
]
test_req = pkg_req + [
    'pytest>=3.0.6'
]

setup(
    name="midtransclient",
    version="1.3.0",
    author="Midtrans - Integration Support Team",
    author_email="support@midtrans.com",
    license='MIT',
    description="Official Midtrans Payment API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/midtrans/midtrans-python-client/",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.5',
    install_requires=pkg_req,
    tests_requires=test_req
)
