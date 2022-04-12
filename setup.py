import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dfdata", 
    version="0.0.6",
    author="dfdata",
    author_email="dfdata@outlook.com",
    description="下载金融数据",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfdata/dfdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
