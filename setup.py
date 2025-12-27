from setuptools import setup, find_packages

setup(
    name= "document_portal",
    author= "Chris",
    version= "0.1",
    description = "document management portal built with FASTAPI",
    long_description= open("README.md").read(),
    long_description_content_type="text/markdown",
    url= "",
    packages= find_packages(),

)