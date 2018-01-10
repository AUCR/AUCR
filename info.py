"""Default Project information"""
import yaml


class ProjectInfo:
    project_info = {}

    def __init__(self) -> None:
        """init to load project information and license info"""
        with open("projectinfo.yml", 'rb') as project_info_file:
            project_info_strings = project_info_file.read()
        self.project_info = yaml.load(project_info_strings)
        with open("LICENSE", 'r') as license_file:
            license_strings = license_file.read()
        self.project_info["license"] = license_strings.strip('\n')

    def get(self) -> dict:
        return self.project_info


