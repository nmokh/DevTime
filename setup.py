from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dv",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "devtime=devtime.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    license_files=[],
    include_package_data=True,
    long_description=long_description,  
    long_description_content_type="text/markdown",
)
