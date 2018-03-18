#!/usr/bin/env python3

'''
Summary:
    This script will generate an initial configuration based on the data input into the A10_PoC_Data.xls(m) spreadsheet.

Requires:
    - Python 3.x
    - aXAPI v3.0
    - ACOS 4.1 or higher
    - Review README in github repo to see additional libraries required to run this script.

Revisions:
    Rev     Date        Changes
    0.1     2.28.2018   Initial build


'''
import argparse
import requests
import logging
import datetime
import get_config_data


__version__ = '0.1'
__author__ = 'A10 Networks'

parser = argparse.ArgumentParser(description='This program will grab the data necessary to log into A10 ADC.')
devices = parser.add_mutually_exclusive_group()
devices.add_argument('-d', '--device', default='192.168.0.152', help='A10 device hostname or IP address. Multiple devices may be included separated by a comma.')
parser.add_argument('-p', '--password', default='a10', help='user password')
parser.add_argument('-u', '--username', default='admin', help='username (default: admin)')
parser.add_argument('-v', '--verbose', default=0, action='count', help='Enable verbose detail')

try:
    args = parser.parse_args()
    devices = args.device.split(',')
    password = args.password
    username = args.username
    verbose = args.verbose

except Exception as e:
    print(e)


def main():
    requests.packages.urllib3.disable_warnings()

    # set the default logging format
    logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")

    print('\n\nPoC script started at: ' + str(datetime.datetime.now()) + '\n\n')

    print('\nA10 ACOS configuration builder\n')
    print('!*****************************************************************')
    print('! Configuration per device. Enable vcs clustering after entering')
    print('! these commands (ie: vcs reload).')
    print('!*****************************************************************\n')
    get_config_data.create_vrrpa_commmon_config()
    get_config_data.create_vcs_config()
    print('!*****************************************************************')
    print('!** Common Configuration to be used once devices are clustered. **')
    print('!*****************************************************************\n')
    get_config_data.create_vrrpa_config()
    get_config_data.create_base_system_config()
    get_config_data.create_interface_vlan_routes()
    get_config_data.create_logging_config()
    get_config_data.create_snat_pools()
    get_config_data.create_http_templates()
    get_config_data.create_client_ssl_templates()
    get_config_data.create_slb_servers()
    get_config_data.create_slb_service_groups()
    get_config_data.create_slb_virtual_servers()
    print('\n\nPoC script ended at: ' + str(datetime.datetime.now()) + '\n\n')
    return True

if __name__ == "__main__":
    main()
