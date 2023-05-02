#!/usr/bin/env python3
#
# ShotHub API sample script #4: Download dynamic metadata for all flagged clips from a selected shooting day
#
# (c) 2022 - 2023 Pomfort GmbH, https://pomfort.com/
#
# To use, enter your script credentials into the accompanying file 'shothub_api_config.py' and insert your project ID,
# folder ID or shooting day below
#
# No pip modules are required.

import os
import shothub_api_utils
import shothub_api_config

# insert your project ID here
project_id = '643533041b92c40aa318d8db'

# if your project uses a folder for every shooting day, enter the folder ID for the shooting day you want to export here
# otherwise set it to None.
#
# If both this and shooting_day are set to None, dynamic metadata will be downloaded for all flagged clips in the
# project, regardless of shooting day.
folder_id = None

# if your project uses the "Shooting Day" metadata field, enter the value for the shooting day you want to export here
shooting_day = None

output_dir = f'output/dynamic-metadata/{project_id}/'


def main():
    global folder_id
    shothub_api_utils.login()

    if folder_id is None:
        folder_id = shothub_api_utils.get_project_root_folder(project_id)

    # now we can start fetching the assets
    page_counter = 0
    page_size = 50
    page_count = 1  # will be updated after the first request
    relevant_assets = []

    while page_counter < page_count:
        asset_response = shothub_api_utils.request_get(f'{shothub_api_config.base_url}/v1.0/assets'
                                                       f'?folderId={folder_id}'
                                                       f'&assetType=VideoClip'
                                                       f'&page={page_counter}'
                                                       f'&pageSize={page_size}',
                                                       headers=shothub_api_utils.get_login_header())

        if asset_response.status_code != 200:
            raise Exception(f"couldn't load assets: HTTP status {asset_response.status_code}")

        for asset in asset_response.json():
            if shooting_day is None or shooting_day == asset['shootingDay']:
                if asset['flag'] and asset['hasDynamicMetadata']:
                    relevant_assets.append(asset)

        page_counter = page_counter + 1

    print(f'Found {len(relevant_assets)} flagged clips with dynamic metadata, beginning download...')

    os.makedirs(output_dir, exist_ok=True)

    for asset in relevant_assets:
        dmd_response = shothub_api_utils.request_get(
            f'{shothub_api_config.base_url}/v1.0/assets/{asset["id"]}/dynamic-metadata',
            headers=shothub_api_utils.get_login_header())

        if dmd_response.status_code != 200:
            raise Exception(f"couldn't load dynamic metadata: HTTP status {dmd_response.status_code}")

        with open(f'{output_dir}/{asset["name"]}_{asset["id"]}.csv', 'w') as f:
            f.write(dmd_response.text)


main()
