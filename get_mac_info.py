#!/usr/bin/python

# Author: @Praveen Pasunuri
# Usage:
# python get_mac_info.py -m "44:38:39:ff:ef:57"
#
# To print api details in json format
# python get_mac_info.py -m "44:38:39:ff:ef:57" --json true

import re
import requests
from argparse import ArgumentParser
import pprint


class Config:
    APIKEY = "at_b0kY8aODTk6dpNgk8GXpuqY3GsmRI"
    API_URL = "https://api.macaddress.io/v1?apiKey="
    OUTPUT_TYPE = "&output=json"
    QUERY = "&search="
    DEBUG = False


def validate_mac_input(mac_input=None):
    """Validates mac input address, returns False if invalid"""
    is_valid_mac = False
    try:
        if mac_input and not isinstance(mac_input, str):
            is_valid_mac = False
        regex = r'[\:\-]'.join(['([0-9a-f]{2})']*6)
        is_mac = re.match(f'^{regex}$', mac_input.lower())
        if bool(is_mac):
            is_valid_mac = True
    except Exception as err:
        print("Please provide a valid mac address")
        if Config.DEBUG:
            print(err)
    return is_valid_mac


def get_mac_info(mac_input):
    """Requests Mac address details from https://api.macaddress.io,
       which returns JSON format"""
    api_url = (f"{Config.API_URL}{Config.APIKEY}"
               f"{Config.OUTPUT_TYPE}{Config.QUERY}{mac_input}")
    response = requests.get(api_url)
    response = response.json()
    if 'error' in response:
        print(f"Error: {response['error']}")
    company_name = response.get('vendorDetails', {}).get('companyName')
    print(f'Mac address: {mac_input} belongs to company -  {company_name}')
    return response


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--mac", dest="mac_address", required=True,
                        help="Input a valid mac address eg. 44:38:39:ff:ef:57")
    parser.add_argument("-j", "--json", dest="json",
                        help="Print JSON formatted response of the API url")
    args = parser.parse_args()
    is_valid_mac = validate_mac_input(args.mac_address)
    if is_valid_mac:
        mac_details = get_mac_info(args.mac_address)
        jsonformat = args.json or ''
        if all([jsonformat, isinstance(jsonformat, str),
                jsonformat in ['yes', 'y', 'true', 'True', '1']]):
            pprint.pprint(mac_details)


if __name__ == '__main__':
    main()
