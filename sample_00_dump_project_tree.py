#!/usr/bin/env python3
"""
__copyright__ = "Copyright 2023, Pomfort GmbH"
__license__ = "MIT"
__email__ = "opensource@pomfort.com"
"""
#
# ShotHub API sample script #0: Print the folder structure for one or more projects
#
# (c) 2022 - 2023 Pomfort GmbH, https://pomfort.com/
#
# To use, enter your script credentials into the accompanying file 'shothub_api_config.py'. Make sure that your script
# user is in at least one project, or the script will not show any useful output!
#
# No pip modules are required.

import shothub_api_utils
import shothub_api_config


def print_folder(folder, recursion_level = 0):
    padding = recursion_level * "  "
    print(f'{padding} + {folder["name"]} ({folder["id"]})')
    for child in folder["children"]:
        print_folder(child, recursion_level + 1)


def print_project_folder_tree(project, headers):
    # load folder tree
    fres = shothub_api_utils.request_get(shothub_api_config.base_url + "/v1.0/folders-tree/" + project["id"],
                                         headers=shothub_api_utils.get_login_header())
    if fres.status_code != 200:
        print('ERROR: Folder tree request returned status code', fres.status_code)
        exit(1)

    print()
    print("=== PROJECT " + project["name"] + " ===")
    print()

    for folder in fres.json():
        print_folder(folder)


def main():
    # get a JWT token
    shothub_api_utils.login()

    # get project list
    res = shothub_api_utils.request_get(shothub_api_config.base_url + "/v1.0/projects?page=0&take=50",
                       headers=shothub_api_utils.get_login_header())

    if res.status_code != 200:
        print('ERROR: Project list request returned status code', res.status_code)
        exit(1)

    project_list = res.json()

    for project in project_list:
        print_project_folder_tree(project, headers=shothub_api_utils.get_login_header())


main()
