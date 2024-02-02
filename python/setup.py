from setuptools import setup
import sys
from typing import List
import platform
import sysconfig
import os

from setuptools._distutils.util import convert_path


def get_plat():
    if platform.system() == 'Linux':
        plat_form = "manylinux1_x86_64"
    else:
        plat_form = sysconfig.get_platform()
    return plat_form


def get_version():
    main_ns = {}
    ver_path = convert_path('./ionpy/version.py')
    with open(ver_path) as ver_file:
        exec(ver_file.read(), main_ns)
    if os.environ.get("GITHUB_REF_NAME") is not None:
        tag = os.environ.get("GITHUB_REF_NAME")
    else:
        tag = '1.6.0'
    return tag


def main():
    package_data: List[str] = []

    if platform.system() == 'Windows':
        package_data = ["module/windows/*"]
    elif platform.system() == 'Darwin':
        package_data = ["module/macos/*"]
    elif platform.system() == 'Linux':
        package_data = ["module/linux/*"]

    setup(
        name="ion-python",
        packages=["ionpy"],
        version=get_version(),
        package_data={"ionpy": package_data},
        ext_modules=EmptyListWithLength(),
        include_package_data=False,
        options={
            "bdist_wheel": {
                "plat_name": get_plat(),
            },
        },
    )


# This creates a list which is empty but returns a length of 1.
# Should make the wheel a binary distribution and platlib compliant.
class EmptyListWithLength(list):
    def __len__(self):
        return 1


if __name__ == "__main__":
    main()
