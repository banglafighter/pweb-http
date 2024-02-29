from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "README.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = []

    if env and env == "dev":
        return dependency

    return dependency + []


setup(
    name='pweb-http',
    version='0.0.1',
    url='https://github.com/problemfighter/pweb-http',
    license='Apache 2.0',
    author='Bangla Fighter',
    author_email='banglafighter.com@gmail.com',
    description='PWebHTTP responsible for connect to PWeb Using HTTP, It can understand API call and response with authentication',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)
