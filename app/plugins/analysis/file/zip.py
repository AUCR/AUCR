"""Zip file parsing"""
# coding=utf-8
import hashlib
from zipfile import ZipFile


def decrypt_zip_file_map(encrypted_zip, encrypted_file_password) -> bytes:
    """Return a decrypted zip file map bytes object."""
    encrypted_zip_file = ZipFile(encrypted_zip)
    for file in encrypted_zip_file.namelist():
        if encrypted_zip_file.getinfo(file).file_size < 1024 * 1024:
            file_map = encrypted_zip_file.read(file, pwd=encrypted_file_password.encode('utf-8'))
            return file_map


def compress_zip_file_map(file_object, file_path):
    """Return md5 hash of a compressed file."""
    file_md5_hash = hashlib.md5()
    file_map = file_object.read()
    file_md5_hash.update(file_map)
    file_hash = file_md5_hash.hexdigest()
    full_file_path_and_name = str(file_path + "/" + file_hash + ".zip")
    with ZipFile(full_file_path_and_name, 'w') as compressed_zip_file:
        compressed_zip_file.writestr(file_hash, file_map)
        compressed_zip_file.close()

    return file_hash
