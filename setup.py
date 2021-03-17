import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydb",
    version="0.0.1",
    author="Michael Kerry",
    author_email="michael_kerry@harvard.edu",
    description="A package to facilitate connecting to an oracle DB from a python application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huit/pydb",
    project_urls={
        "Bug Tracker": "https://github.com/huit/pydb/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "cx-Oracle==8.1.0",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
