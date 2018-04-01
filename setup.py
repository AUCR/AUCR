"""The AUCR FLASK APP."""
# coding=utf-8
from setuptools import setup
from setuptools import find_packages
from pip.req import parse_requirements
from pip.download import PipSession
from yaml_info.yamlinfo import YamlInfo


project_data = YamlInfo("projectinfo.yml", "projectinfo", "LICENSE").get()
project_info_data = project_data["info"]
project_version_data = project_data["version"]
__version__ = "%(major)s.%(minor)s.%(revision)s.%(release)s" % project_version_data
install_requirements = parse_requirements("requirements.txt", session=PipSession())
requirements = [str(ir.req) for ir in install_requirements]


setup(
    name=project_data["info"]["name"],
    version=__version__,
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages(exclude=['docs', 'tests', 'tests.*', 'tools', 'utils']),
    url=project_data["info"]["url"],
    license=project_data["info"]["license"],
    author=project_data["info"]["authors"],
    author_email=project_data["info"]["authors_email"],
    description=project_data["info"]["description"],
    classifiers=project_data["info"]["classifiers"],
    package_dir={'aucr': 'aucr', },
    zip_safe=False,
)
