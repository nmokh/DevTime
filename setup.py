from setuptools import setup, find_packages

setup(
    name="devtime",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "tabulate"
    ],
    entry_points={
        "console_scripts": [
            "devtime=devtime.cli:main"
        ]
    },
    include_package_data=True,
)