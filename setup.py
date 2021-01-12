import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pkg_req = [
    'requests>=2.25.0'
]
test_req = pkg_req + [
    'pytest>=3.0.6'
]

setuptools.setup(
    name="midtransclient",
    version="1.2.0",
    author="Rizda Prasetya",
    author_email="rizda.prasetya@midtrans.com",
    license='MIT',
    description="Official Midtrans Payment API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/midtrans/midtrans-python-client/",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=2.7',
    install_requires=pkg_req,
    tests_requires=test_req
)