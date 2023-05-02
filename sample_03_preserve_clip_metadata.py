#!/usr/bin/env python3
#
# ShotHub API sample script #3: Export clip metadata
#
# (c) 2023 Pomfort GmbH, https://pomfort.com/
#
# To use, enter your script credentials into the accompanying file 'shothub_api_config.py', enter your project ID and
# an optional folder ID in the configuration section below, and make sure that the script has access to the selected
# project.
#
# No pip modules are required.

import shothub_api_utils
import shothub_api_config
import os

# insert your project ID here
project_id = '643533041b92c40aa318d8db'


# if your project uses a folder for every shooting day, enter the folder ID for the shooting day you want to export here
# otherwise set it to None.
#
# If both this and shooting_day are set to None, data be downloaded for all clips in the project, regardless of shooting
# day.
folder_id = None

# if your project uses the "Shooting Day" metadata field, enter the value for the shooting day you want to export here
shooting_day = None

output_dir = f'output/metadata'
output_file = f'{output_dir}/{project_id}.csv'

# customize which fields will be included in the csv here
csv_fields = ['assetType', 'type', 'name', 'shotId', 'episode', 'scene', 'shot', 'take']

def main():
    global folder_id

    shothub_api_utils.login()

    os.makedirs(output_dir, exist_ok=True)

    if folder_id is None:
        folder_id = shothub_api_utils.get_project_root_folder(project_id)

    # now we can start fetching the assets
    page_counter = 0
    page_size = 50
    page_count = 1  # will be updated after the first request
    assets = []

    while page_counter < page_count:
        asset_response = shothub_api_utils.request_get(f'{shothub_api_config.base_url}/v1.0/assets'
                                                       f'?folderId={folder_id}'
                                                       f'&page={page_counter}'
                                                       f'&pageSize={page_size}',
                                                       headers=shothub_api_utils.get_login_header())

        for asset in asset_response.json():
            if shooting_day is None or asset['shootingDay'] == shooting_day:
                assets.append(asset)

        page_counter += 1

    with open(output_file, 'w') as f:
        shothub_api_utils.write_csv(f, assets, csv_fields)


main()
