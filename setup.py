import re

import setuptools

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

with open("requirements.txt", encoding="utf8") as f:
    dependencies = f.read()

with open("exaroton/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]


setuptools.setup(
    name="Exaroton",
    version=version,
    description="Exaroton API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ColinShark/Exaroton",
    author="ColinShark",
    author_email="colin@colinshark.de",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet",
        "Topic :: Games/Entertainment",
    ],
    keywords="exaroton minecraft api wrapper",
    project_urls={"Issue Tracker": "https://gitlab.com/ColinShark/exaroton/-/issues"},
    # package_dir={"": "exaroton"},
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=dependencies,
)
