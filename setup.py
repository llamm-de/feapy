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
        "License :: OSI Approved :: MIT",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
    ],
    license="MIT",
    packages=["feapy"],
    install_requires=["pandas", "jinja2", "numpy", "meshio"],
    include_package_data=True,
    zip_safe=False,
)
