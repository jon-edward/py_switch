import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_switch_case",
    version="1.0",
    author="jon-edward",
    description="A switch-case implementation using decorators in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jon-edward/py_switch_case",
    packages=setuptools.find_packages(
        include=[
            "switch",
        ]
    ),
    python_requires=">=3.6",
)
