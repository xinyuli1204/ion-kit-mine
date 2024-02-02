import subprocess

from setuptools import setup, find_namespace_packages
import sys
from typing import List
import platform
import sysconfig
import os


def get_plat():
    if platform.system() == 'Linux':
        plat_form = "manylinux1_x86_64"
    else:
        plat_form = sysconfig.get_platform()
    return plat_form


def get_version() -> str:
    try:
        if platform.system() == 'Windows':
            cmd = "git for-each-ref refs/tags --sort=-taggerdate --format=%(refname:short) --count=1 --points-at=HEAD"
        else:
            cmd = "git describe --tags `git rev-list --tags --max-count=1`"
        ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        version = ret.stdout.decode('utf-8').replace('v', '').strip()
    except:
        from importlib.metadata import version
        bump_version = version("ion-python")
        version = bump_version
    return version


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
        package_data={"ionpy": package_data},
        version=get_version(),
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
