import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pkg_req = [
    'requests>=2.3.0'
]
test_req = pkg_req + [
    'pytest>=3.0.6'
]

setuptools.setup(
    name="midtransclient",
    version="1.0.2",
    author="Rizda Prasetya",
    author_email="rizda.prasetya@midtrans.com",
    license='MIT',
    description="Official Midtrans Payment API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/midtrans/midtrans-client-python",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=2.7',
    install_requires=pkg_req,
    tests_requires=test_req
)