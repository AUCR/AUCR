"""Zip file parsing"""
# coding=utf-8
from zipfile import ZipFile


def decrypt_zip_file_map(encrypted_zip, encrypted_file_password) -> bytes:
    """Return a decrypted zip file map bytes object."""
    encrypted_zip_file = ZipFile(encrypted_zip)
    for file in encrypted_zip_file.namelist():
        if encrypted_zip_file.getinfo(file).file_size < 1024 * 1024:
            file_map = encrypted_zip_file.read(file, pwd=encrypted_file_password.encode('utf-8'))
            return file_map


def encrypt_zip_file_map(encrypted_zip, encrypted_file_password, file_hash) -> bytes:
    """Return a encrypted zip file map bytes object."""
    encrypted_zip_file = ZipFile(encrypted_zip)
    encrypted_zip_file.filename(file_hash)
    for file in encrypted_zip_file.namelist():
        if encrypted_zip_file.getinfo(file).file_size < 1024 * 1024:
            encrypted_zip_file.setpassword(encrypted_file_password)
            file_map = encrypted_zip_file.write(encrypted_zip)
            return file_map
