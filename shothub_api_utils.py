#!/usr/bin/env python3
#
# This script contains some helper functions for dealing with common tasks (e.g. authentication) when using the ShotHub
# API. Please feel free to use it as a basis for your own scripts.
#
# (c) 2022 - 2023 Pomfort GmbH, https://pomfort.com/

import requests
import time
import shothub_api_config

headers = None


def login():
    global headers
    res = requests.post(shothub_api_config.base_url + "/authenticate", json=shothub_api_config.creds)

    if res.status_code != 200:
        print('ERROR: login request returned status code', res.status_code)
        exit(1)

    token = res.json()['id_token']
    headers = {
        'Authorization': 'Bearer ' + token
    }


def get_login_header():
    if headers is None:
        raise Exception('Must call \'login()\' first!')

    return headers


def get_project_root_folder(project_id):
    # The 'projects' endpoint is paginated - if you have more than 50 projects, you'll need to fetch additional pages.
    # Please refer to the documentation at https://shothub.pomfort.com/openapi/ui.html for details.
    project_response = request_get(f'{shothub_api_config.base_url}/v1.0/projects?pageSize=50',
                                    headers=get_login_header())

    if project_response.status_code != 200:
        raise Exception(f"couldn't load project list: HTTP status {project_response.status_code}")

    # find the project we want from the project list
    project = next(filter(lambda p: p['id'] == project_id, project_response.json()))
    return project['rootFolderId']


# Wrapper around 'requests.get(...)' which handles 429 (Too Many Requests) response from server.
def request_get(*args, **kwargs):
    retries = 0
    result = None
    while retries < 3:
        result = requests.get(*args, **kwargs)

        if result.status_code == 429:
            time.sleep(60)
            retries += 1
        else:
            return result

    return result


def write_csv(file, assets, columns):
    write_csv_headers(file, columns)
    for asset in assets:
        write_csv_line(file, asset, columns)


def write_csv_headers(file, columns):
    first = True
    for column_name in columns:
        if first:
            first = False
        else:
            file.write(';')

        file.write(f'"{column_name}"')

    file.write("\r\n")


def write_csv_line(file, asset, columns):
    first = True
    for column_name in columns:
        if first:
            first = False
        else:
            file.write(';')

        if column_name in asset:
            value = asset[column_name]
        else:
            value = ''
        file.write(f'"{value}"')

    file.write("\r\n")
