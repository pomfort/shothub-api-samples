#!/usr/bin/env python3
"""
__copyright__ = "Copyright 2023, Pomfort GmbH"
__license__ = "MIT"
__email__ = "opensource@pomfort.com"
"""
# configuration - please enter your credentials here, or set the environment variables
# 'SH_API_SCRIPT_ID' and 'SH_API_SCRIPT_KEY' to override the values given here
creds = {
    "scriptId": "0123456789abcdef01234567/ExampleScript",
    "scriptKey": "ThirtyTwoRandomLettersAndNumbers"
}

# ================================== #
# PLEASE DO NOT EDIT BELOW THIS LINE #
# ================================== #
import os

base_url = "https://api.pomfort.com/sh"

env = os.getenv('SH_API_SCRIPT_ID')
if env is not None:
    creds['scriptId'] = env

env = os.getenv('SH_API_SCRIPT_KEY')
if env is not None:
    creds['scriptKey'] = env

env = os.getenv('SH_API_BASE_URL')
if env is not None:
    base_url = env
