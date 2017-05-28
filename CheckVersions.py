#!/usr/bin/python3
# coding: utf8
import os
import subprocess
import configparser


class CheckVersions(object):

    @staticmethod
    def convert_to_cpe(name, version):
        prefix = "cpe:/a:"
        delimiter = ":"
        print(name + delimiter + str(version))
        return prefix + name + delimiter + str(version)

    @staticmethod
    def ssh_connection(hostname, username, pkey_file, command):
        return subprocess.getoutput('ssh -i ' + pkey_file + ' ' + username + '@' + hostname + " '" + command + "'")

    def check_versions(self, username, private_key):
        config_name = "conf.ini"
        config_file = os.path.join(os.path.dirname(__file__), config_name)
        config = configparser.ConfigParser()
        config.read(config_file)
        cpe_list = []
        for key, value in config.__dict__['_sections'].items():
            command = value['command']
            if value['ssh'] == "True":
                version = self.ssh_connection(value['hostname'], username, private_key, command)
            else:
                version = subprocess.getoutput(command)
            cpe_list.append(self.convert_to_cpe(value['cpe'], version))
        return cpe_list
