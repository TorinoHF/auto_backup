"""Script for synchronizing local folders with remote folders using SFTP."""
# import os
import argparse
import getpass
import logging
import sys
# import tarfile
import yaml
import paramiko


def ssh_connect(host, username, password):
    """
    Establish an SSH connection to the given host using password authentication.
    """
    logging.info("Connecting to %s as %s...", host, username)
    client = paramiko.SSHClient()
    # Automatically add the host key (be cautious in production!)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=username, password=password)
    except Exception as e:  # pylint: disable=broad-except
        logging.error("SSH connection failed: %s", e)
        sys.exit(1)
    return client


def upload_file(sftp, local_file, remote_file):
    """
    Upload a file to the remote server using an open SFTP connection.
    """
    logging.info("Uploading '%s' to remote location '%s'...", local_file, remote_file)
    try:
        sftp.put(local_file, remote_file)
    except Exception as e:  # pylint: disable=broad-except
        logging.error("SFTP upload failed: %s", e)
        sys.exit(1)


def sync(config_file_name):
    """
    Synchronize local folders with remote folders.
    Args:
        config_file_name (str): The path to the YAML configuration file.

    The function will prompt for the password if it is not provided in the configuration file.
    It will then establish an SSH connection to the remote host and use SFTP to upload the
    specified local folders to the corresponding remote folders.
    """
    with open(config_file_name, 'r', encoding='utf-8') as file:
        config = yaml.load(file, yaml.FullLoader)

    if config['connection']['psw'] is None:
        config['connection']['psw'] = getpass.getpass(
            prompt=f'Password for\
                {config["connection"]["username"]}@{config["connection"]["host"]}: '
        )

    client = ssh_connect(
        config['connection']['host'],
        config['connection']['username'],
        config['connection']['psw']
    )
    sftp = client.open_sftp()

    for file, remote_path in zip(config['folders_to_sync'], config['target_folders']):
        upload_file(sftp, file, remote_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('config_file_name', metavar='text', default='')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    sync(args.config_file_name)
