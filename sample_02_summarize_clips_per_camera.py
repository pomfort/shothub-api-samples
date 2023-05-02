#!/usr/bin/env python3
#
# ShotHub API sample script #2: Group clips by camera and export some metadata for statistics
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

# Set a folder ID here if you want to restrict the export to a folder and its subfolders (you can get the folder ID via
# the /v1.0/folders-tree/{project_id} endpoint or by opening the folder in the ShotHub UI and looking at the URL
# parameters).
#
# If you set this to None, the root folder of the project specified above will be used.
folder_id = None

# You can add more fields here to customize the export - please refer to
# https://shothub.pomfort.com/openapi/ui.html#tag/Assets/operation/getAssets for a full list of available fields
csv_fields = ['id', 'name', 'shotId', 'duration', 'durationInSecs', 'tcStart', 'tcEnd', 'tcFps', 'tcDropFlag']

output_dir = f'output/clips-per-camera/{project_id}/'


def main():
    global folder_id

    shothub_api_utils.login()

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
                                                       f'&assetType=VideoClip'
                                                       f'&page={page_counter}'
                                                       f'&pageSize={page_size}',
                                                       headers=shothub_api_utils.get_login_header())

        if asset_response.status_code != 200:
            raise Exception(f"couldn't load assets: HTTP status {asset_response.status_code}")

        # calculate page count
        total_count = int(asset_response.headers['x-total-count'])
        page_count = total_count // page_size
        if total_count % page_size > 0:
            page_count = page_count + 1

        assets.extend(asset_response.json())
        page_counter = page_counter + 1

    # Now, we can start the actual data manipulation
    clips_by_camera = {}

    for asset in assets:
        camera_manufacturer = asset['manufacturer']
        camera_model = asset['model']

        if camera_model is None and camera_manufacturer is None:
            camera = 'Unknown'
        elif camera_model is None:
            camera = f'Unknown {camera_manufacturer} camera'
        elif camera_manufacturer is None:
            camera = camera_model
        else:
            camera = f'{camera_manufacturer} {camera_model}'

        if camera in clips_by_camera:
            clips_by_camera[camera].append(asset)
        else:
            clips_by_camera[camera] = [asset]

    for camera in clips_by_camera.keys():
        os.makedirs(output_dir, exist_ok=True)
        outfile = f'{output_dir}/{camera}.csv'
        with open(outfile, 'w') as f:
            shothub_api_utils.write_csv(f, assets, csv_fields)


main()
