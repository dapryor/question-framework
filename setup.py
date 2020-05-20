import setuptools


setuptools.setup(
    name="question_framework", # Replace with your own username
    version="0.0.1",
    author="David Pryor",
    author_email="dapryor@cisco.com",
    description="Framework for asking questions",
    url="https://github.com/dapryor/question_framework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)