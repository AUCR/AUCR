import ldap
from flask import current_app


def get_ldap_connection():
    connection = ldap.initialize(current_app.config['LDAP_PROVIDER_URL'])
    return connection


def get_ldap_user_email_address(user_name, password):
    user_email = None
    ldap_connection = get_ldap_connection()
    ldap_connection.protocol_version = current_app.config['LDAP_PROTOCOL_VERSION']
    ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
    try:
        ldap_connection.simple_bind_s(current_app.config['LDAP_CONNECTION_STRING'] % user_name, password)
    except ldap.INVALID_CREDENTIALS:
        return user_email
    scope = ldap.SCOPE_SUBTREE
    search_filter = "(&(objectClass=user)(sAMAccountName=" + user_name + "))"
    attribute_values = ["mail"]
    search_result = ldap_connection.search(current_app.config['LDAP_BASE'], scope, search_filter, attribute_values)
    data_type, user_result = ldap_connection.result(search_result, 60)

    name, attribute_values = user_result[0]
    if "mail" in attribute_values:
        user_email = attribute_values["mail"][0].decode('utf-8')
    return user_email
