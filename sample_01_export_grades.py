#!/usr/bin/env python3
#
# ShotHub API sample script #1: Export grades from a folder, along with relevant metadata
#
# (c) 2022 - 2023 Pomfort GmbH, https://pomfort.com/
#
# To use, enter your script credentials into the accompanying file 'shothub_api_config.py'. Make sure that your script
# user is in at least one project, or the script will not show any useful output!
#
# No pip modules are required.

import requests
from zipfile import ZipFile
import os
import shothub_api_utils
import shothub_api_config

# enter folder id (e.g. for the folder corresponding to the most recent shooting day) here
folder_id = '641af9c62e1cfc1ad167ce20'

csv_fields = ['clipName', 'clipIdentifier', 'clipNumber', 'lensModel', 'asa', 'whiteBalance',
              'greenTint', 'location', 'crewUnit', 'indoorOutdoor', 'dayNight', 'scene',
              'shot', 'take', 'grade_name', 'grade_mode']

# various file paths
output_dir = f'output/export-grades/{folder_id}/'
temp_dir = f'{output_dir}/tmp/'
temp_zip_file = f'{temp_dir}/grades.zip'


def add_to_output_object(input, output, fieldNames):
    for fieldName in fieldNames:
        output[fieldName] = input[fieldName]


def get_grade_info(shot_id):
    shot_response = shothub_api_utils.request_get(f'{shothub_api_config.base_url}/v1.0/assets/{shot_id}'
                                                  f'?parts=gradeInfo',
                                                  headers=shothub_api_utils.get_login_header())

    shot = shot_response.json()
    grade_info = shot['parts']['gradeInfo']
    grade = grade_info['grade']

    result = {}
    add_to_output_object(shot, result, ['clipName', 'clipIdentifier', 'clipNumber', 'lensModel', 'asa', 'whiteBalance',
                                        'greenTint', 'location', 'crewUnit', 'indoorOutdoor', 'dayNight', 'scene',
                                        'shot', 'take'])

    result['grade_name'] = grade['name']
    result['grade_mode'] = grade['mode']

    return result


def main():
    # Create output dir and temp dir. If those already exist, the script can't run because it might get confused
    # by the output from previous runs.
    #
    # (You could change this to simply delete everything in those directories if they already exist - we do not know
    # the setup on your machine, and don't want to accidentally delete something important.)
    try:
        os.makedirs(output_dir)
    except Exception as e:
        print(f'Could not create output directory at "{output_dir}". '
              f'The directory might already exist - please delete it manually.')
        raise e

    try:
        os.makedirs(temp_dir)
    except Exception as e:
        print(f'Could not create temporary directory at "{temp_dir}". '
              f'The directory might already exist - please delete it manually.')
        raise e

    # get a JWT token
    shothub_api_utils.login()

    # download the grades
    cdl_response = requests.get(f'{shothub_api_config.base_url}/v1.0/cdl-zip/{folder_id}'
                                f'?namingScheme=clipName',
                                headers=shothub_api_utils.get_login_header())

    if cdl_response.status_code != 200:
        raise Exception(f'Could not download CDL files: HTTP status {cdl_response.status_code}')

    with open(temp_zip_file, 'wb') as f:
        f.write(cdl_response.content)

    with ZipFile(temp_zip_file) as f:
        f.extractall(output_dir)

    # then, fetch grading-related metadata and dump it to a CSV
    page_counter = 0
    page_size = 50
    page_count = 1  # will be updated after the first request
    relevant_asset_ids = []

    while page_counter < page_count:
        asset_response = shothub_api_utils.request_get(f'{shothub_api_config.base_url}/v1.0/assets'
                                                       f'?folderId={folder_id}'
                                                       f'&assetType=Shot'
                                                       f'&page={page_counter}'
                                                       f'&pageSize={page_size}',
                                                       headers=shothub_api_utils.get_login_header())

        for asset in asset_response.json():
            # check if this asset is associated with a grade
            clip_name = asset['name']
            expected_path = f'{output_dir}/{clip_name}.cdl'
            if os.path.isfile(expected_path):
                relevant_asset_ids.append(asset['id'])

        page_counter += 1

    # We now have a complete list of relevant shots - now we need to fetch the grading metadata for each shot,
    # and do some data wrangling to make the CSV dump a bit easier
    output_objects = map(get_grade_info, relevant_asset_ids)

    outfile = f'{output_dir}/grading_info.csv'

    with open(outfile, 'w') as f:
        shothub_api_utils.write_csv(f, output_objects, csv_fields)

    # cleanup: delete the temp directory
    os.unlink(temp_zip_file)


main()
