from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="FEAPy",
    version="0.1.0",
    description="Tools to include FEAP into Python scripts",
    long_description=readme(),
    url="",
    author="L. Lamm",
    author_email="lamm@ifam.rwth-aachen.de",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
    ],
    license="GNU General Public License v2 or later (GPLv2+)",
    packages=["feapy"],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
