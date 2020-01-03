# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "Prototype OpenFisca USA Head Start",
    version = "0.0.1",
    author = "Alex Soble, 18F",
    author_email = "",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        ],
    description = "Sketchpad prototyping repo being used by 18F's Eligibility APIs Initiative",
    keywords = "",
    license = "http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url = "https://github.com/18f/prototype-openfisca-usa-headstart/",
    include_package_data = True,  # Will read MANIFEST.in
    data_files = [
        ("share/openfisca/openfisca-country-template", ["CHANGELOG.md", "LICENSE", "README.md"]),
        ],
    install_requires = [
        "OpenFisca-Core[web-api] >=27.0,<35.0",
        ],
    extras_require = {
        "dev": [
            "autopep8 ==1.4.4",
            "flake8 >=3.5.0,<3.8.0",
            "flake8-print",
            "pycodestyle >=2.3.0,<2.6.0",  # To avoid incompatibility with flake
            ]
        },
    packages=find_packages(),
    )
