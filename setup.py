from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="FEAPy",
    version="0.2.1",
    description="Tools to include FEAP into Python scripts",
    long_description=readme(),
    url="",
    author="L. Lamm",
    author_email="lamm@ifam.rwth-aachen.de",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
    ],
    license="MIT",
    packages=["feapy"],
    install_requires=["pandas", "jinja2", "numpy", "meshio", "matplotlib"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "fplot=scripts.cmd_plot:main",
            "setup_feap=scripts.cmd_feap_path:main",
        ]
    },
)
