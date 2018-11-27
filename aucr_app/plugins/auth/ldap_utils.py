"""AUCR auth routes manages all basic flask app blueprints."""
# coding=utf-8
import ldap
import logging
from flask import current_app


def get_ldap_connection():
    connection = ldap.initialize(current_app.config['LDAP_PROVIDER_URL'])
    return connection


def get_ldap_user_email_address(user_name, password):
    """LDAP user authentication to return user email attribute."""
    user_email = None
    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, current_app.config['LDAP_CERTIFICATE'])
    ldap_connection = ldap.initialize(current_app.config['LDAP_PROVIDER_URL'])
    ldap_connection.protocol_version = current_app.config['LDAP_PROTOCOL_VERSION']
    ldap_connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
    ldap_connection.set_option(ldap.OPT_X_TLS_CACERTFILE, current_app.config['LDAP_CERTIFICATE'])
    ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
    ldap_connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)
    ldap_connection.set_option(ldap.OPT_X_TLS_PROTOCOL_MIN, 0x301)
    ldap_connection.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
    ldap_connection.set_option(ldap.OPT_X_TLS_DEMAND, True)
    logging.info("User attempting to login " + str(user_name))
    try:
        ldap_connection.simple_bind_s(current_app.config['LDAP_CONNECTION_STRING'] % user_name, password)
    except ldap.INVALID_CREDENTIALS:
        logging.error("User failed to login " + str(user_name))
        return user_email
    scope = ldap.SCOPE_SUBTREE
    search_filter = "(&(objectClass=user)(sAMAccountName=" + user_name + "))"
    attribute_values = ["mail"]
    search_result = ldap_connection.search(current_app.config['LDAP_BASE'], scope, search_filter, attribute_values)
    data_type, user_result = ldap_connection.result(search_result, 60)

    name, attribute_values = user_result[0]
    if "mail" in attribute_values:
        user_email = attribute_values["mail"][0].decode('utf-8')
    ldap_connection.unbind_s()
    logging.info("User auth was a success " + str(user_name))
    return user_email


def change_password(user_name, old_password, new_password):
    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, current_app.config['LDAP_CERTIFICATE'])
    ldap_connection = ldap.initialize(current_app.config['LDAP_PROVIDER_URL'])
    ldap_connection.protocol_version = current_app.config['LDAP_PROTOCOL_VERSION']
    ldap_connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
    ldap_connection.set_option(ldap.OPT_X_TLS_CACERTFILE, current_app.config['LDAP_CERTIFICATE'])
    ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
    ldap_connection.set_option(ldap.OPT_X_TLS_DEMAND, True)
    ldap_connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)
    test_dn = current_app.config['LDAP_CONNECTION_STRING'] % user_name
    try:
        ldap_connection.simple_bind_s(current_app.config['LDAP_CONNECTION_STRING'] % user_name, old_password)
    except ldap.INVALID_CREDENTIALS:
        return None
    old_password_utf16 = '"{0}"'.format(old_password).encode('utf-16-le')
    new_password_utf16 = '"{0}"'.format(new_password).encode('utf-16-le')
    mod_list = [
        (ldap.MOD_DELETE, "unicodePwd", old_password_utf16),
        (ldap.MOD_ADD, "unicodePwd", new_password_utf16),
    ]
    ldap_connection.modify_s(test_dn, mod_list)
    ldap_connection.unbind_s()

