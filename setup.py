import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dlmf-scraping",
    version="0.1.0",
    mantainer="Dariush Ehsani, Matteo Petrera",
    maintainer_email="dariush@zbmath.org, matteo@zbmath.org",
    description="Scraping DLMF bibliography.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "dlmf-scrape=dlmf_scraping.dlmf_scraping_script:main"
        ],
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
