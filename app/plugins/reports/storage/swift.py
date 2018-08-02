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
        container_name =  os.environ["OPENSTACK_CONTAINER_NAME"]
        self.container_name = container_name
        options = {
            'user_domain_name': user_domain_name,
            'project_domain_name': project_domain_name,
            'project_name': project_name,
        }
        # Establish the connection with the object storage API cacert=ca_certificate,
        self.conn = swiftclient.Connection(
            user=username,
            key=password,
            authurl=auth_url,
            auth_version=3,
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
