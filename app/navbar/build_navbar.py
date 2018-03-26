# coding=utf-8
import glob
import yaml
from string import Template


class BuildNavBar(object):
    """Class to Build out a navigation bar based on the YAML
    file information presented by all imported plugins"""
    def __init__(self):
        self.yaml_dict = {}

    def get_yaml(self):
        """Parse Plugins for all navbar YAML files and build out a dictionary
        to user to build out links in navbar"""
        for filename in glob.iglob('app/plugins/**/navbar.yml', recursive=True):
            with open(filename, 'rb') as yaml_file:
                yaml_output = yaml.load(yaml_file)
                for link_type, link_content in yaml_output.items():
                    if link_type in self.yaml_dict:
                        self.yaml_dict[link_type].update(link_content)
                    else:
                        self.yaml_dict.update({link_type: link_content})

    @staticmethod
    def write_links(dict_to_write):
        """Write out the links to their respective files"""
        for file_to_write, links_to_write in dict_to_write.items():
            filename = 'app/plugins/main/templates/subtemplates/left_navbar/links/_{}.html'.format(file_to_write)
            with open(filename, 'w') as output_file:
                for links in links_to_write:
                    output_file.writelines(links + "\n")

    def create_links(self):
        """Use YAML dictionary to create links and send to write_links method for final output"""
        link_template = Template(
            '<a class="mdl-navigation__link" href="{{ url_for(\'$link_view\') }}">{{ _(\'$link_text\') }}</a>')
        for list_to_build, link_attributes in self.yaml_dict.items():
            temp_list = []
            for link_text, link_view in link_attributes.items():
                temp_list.append(link_template.substitute(link_view=link_view, link_text=link_text))
            self.write_links({list_to_build: temp_list})
