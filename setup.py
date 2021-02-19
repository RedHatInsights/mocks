from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()


setup(
    name="crcmocks",
    version="0.0.1",
    description=("Mock applications for testing cloud.redhat.com services"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Brandon Squizzato",
    author_email="bsquizza@redhat.com",
    url="https://www.github.com/RedHatInsights/mocks",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=["Topic :: Utilities", "Programming Language :: Python :: 3.6"],
    python_requires=">=3.6",
)
