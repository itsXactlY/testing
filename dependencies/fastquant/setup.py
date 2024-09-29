import setuptools
import os

# Read the requirements from the requirements.txt file
with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

# Ensure README.md is read correctly for long description, if available
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name="fastquant",
    version="0.1.8.1",
    author="Lorenzo Ampil",
    author_email="lorenzo.ampil@gmail.com",
    description="Bringing data driven investments to the mainstream",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enzoampil/fastquant",
    packages=setuptools.find_packages(where="python", exclude=["docs", "tests"]),
    package_dir={"": "python"},
    package_data={"fastquant": ["data/*"]},
    include_package_data=True,
    scripts=[
        os.path.join("python", "scripts", "get_disclosures"),
        os.path.join("python", "scripts", "update_cache")
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    python_requires='>=3.6',  # Specify Python version requirement
)
