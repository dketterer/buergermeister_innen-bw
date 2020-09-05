from setuptools import setup, find_packages

setup(
    name="BBW",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "tqdm",
        "BeautifulSoup4",
        "dataclasses-json",
        "pandas",
        "matplotlib",
        "jupyter"
    ],

    # metadata to display on PyPI
    author="Daniel Ketterer",
    description="This is package allows to collect information about the mayors of all municipalities in Baden-Württemberg, Germany.",
    keywords="mayor baden-württemberg bürgermeisterinnen bürgermeister wahlergebnisse wahl crawler",
    url="https://github.com/dketterer/buergermeister_innen-bw",  # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/dketterer/buergermeister_innen-bw",
        "Documentation": "https://github.com/dketterer/buergermeister_innen-bw",
        "Source Code": "https://github.com/dketterer/buergermeister_innen-bw",
    },
    classifiers=[
        "License :: GPLv3"
    ],
    entry_points={
        "console_scripts": [
            "bbw = buergermeisterbw.main:main"
        ]
    }
)
