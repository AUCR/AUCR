"""The AUCR FLASK APP."""
# coding=utf-8
from setuptools import setup
from setuptools import find_packages
from pip.req import parse_requirements
from pip.download import PipSession

install_requirements = parse_requirements("requirements.txt", session=PipSession())
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='aucr',
    version='0.3.1.1',
    packages=find_packages(exclude=['docs', 'tests', 'tests.*', 'tools', 'utils']),
    url='aucr.io',
    license='GPL-3.0',
    include_package_data=True,
    author='Wyatt Roersma',
    author_email='wyattroersma@gmail.com',
    description='Analyst Unknown Cyber Range - a micro web service framework ',
    install_requires=requirements,
    package_dir={
        'aucr': 'aucr',
    },

    zip_safe=False,
)