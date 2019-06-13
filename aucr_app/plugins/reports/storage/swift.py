# Imports the Openstack client library
import os
import swiftclient


class SwiftConnection(object):
    def __init__(self):
        # Read configuration from environment variables (openstack.rc)
        auth_url = os.environ["OPENSTACK_AUTH_URL"]
        user_domain_name = os.environ["OPENSTACK_USER_DOMAIN_NAME"]
        username = os.environ["OPENSTACK_USERNAME"]
        password = os.environ["OPENSTACK_PASSWORD"]
        project_domain_name = os.environ["OPENSTACK_PROJECT_DOMAIN_NAME"]
        project_name = os.environ["OPENSTACK_PROJECT_NAME"]
        container_name = os.environ["OPENSTACK_CONTAINER_NAME"]
        ca_certificate = os.environ["OPENSTACK_CA_CERTIFICATE"] or ""
        self.file_folder = os.environ["FILE_FOLDER"]
        self.container_name = container_name
        options = {
            'user_domain_name': user_domain_name,
            'project_domain_name': project_domain_name,
            'project_name': project_name,
        }
        self.conn = swiftclient.Connection(
            user=username,
            key=password,
            authurl=auth_url,
            auth_version=3,
            cacert=ca_certificate,
            os_options=options
        )
        found = False
        for container in self.conn.get_account()[1]:
            cname = container['name']
            if cname == container_name:
                found = True
        if found is not True:
            # Create a new container
            container_name = container_name
            self.conn.put_container(container_name)

    def put(self, file_name, file_content):
        container_name = self.container_name
        self.conn.put_object(container_name, file_name, contents=file_content, )

    def get_file(self, file_name):
        for data in self.conn.get_container(self.container_name)[1]:
            full_path = file_name
            obj_tuple = self.conn.get_object(self.container_name, full_path)
            if obj_tuple:
                raw_data = obj_tuple[1]
                try:
                    with open(str(self.file_folder + file_name), 'wb') as out_file:
                        out_file.write(raw_data)
                except FileNotFoundError:
                    file_path = ""
                    for letter in file_name:
                        if letter == '/':
                            try:
                                os.mkdir(self.file_folder + file_path)
                            except FileExistsError as e:
                                pass
                        file_path = file_path + letter
                    with open(str(self.file_folder + file_name), 'wb') as out_file:
                        out_file.write(raw_data)
                return

