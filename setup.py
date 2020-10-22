import pathlib
import setuptools


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="question_framework",  # Replace with your own username
    version="0.1.3",
    author="David Pryor",
    author_email="dapryor@cisco.com",
    description="Framework for asking questions",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dapryor/question-framework",
    license="MIT",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
