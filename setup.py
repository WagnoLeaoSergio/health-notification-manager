"""Python setup.py for health_notification_manager package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("health_notification_manager", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="health_notification_manager",
    version=read("health_notification_manager", "VERSION"),
    description="Awesome health_notification_manager created by WagnoLeaoSergio",
    url="https://github.com/WagnoLeaoSergio/health-notification-manager/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="WagnoLeaoSergio",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["health_notification_manager = health_notification_manager.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
