# ShotHub API sample scripts

This repository contains sample scripts for the ShotHub API. All of these scripts are written in Python 3, and can
be run without installing any pip modules. They were written using Python 3.10, but newer Python versions likely also
work.

# Running the scripts

All of these scripts require you to register a Script in the ShotHub team settings and provide the script ID and key.
Please refer to our quickstart guide for additional info: https://kb.pomfort.com/shothub/sh-api/quick-start/

The script ID and key can be either entered in the file 'shothub_api_config.py', or provided through the environment
variables 'SH_API_SCRIPT_ID' and 'SH_API_SCRIPT_KEY'.

Most scripts require some additional configuration, i.e. selecting a project or folder. Please refer to each script's
header section for more information.

The file 'shothub_api_utils.py' contains some boilerplate functionalities for handling authentication, rate limits,
and CSV files. You can use this as a basis for your own script.

# Further resources
* API Quickstart Guide: https://kb.pomfort.com/shothub/sh-api/quick-start/
* API Documentation: https://shothub.pomfort.com/openapi/ui.html
* More information about these sample scripts: http://pomfort.com/article/four-ways-productions-can-benefit-from-shothubs-rest-api/
