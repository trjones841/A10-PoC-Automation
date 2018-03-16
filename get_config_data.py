#!/usr/bin/python3

import pandas as pd
import re


def get_server_data():
    server_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Servers')
    return server_data


def get_vip_data():
    vip_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Virtual-Servers')
    return vip_data


def get_http_templates():
    print('!\nslb template http redirect_to_https')
    print('\tredirect port 443 response-code 301')
    return True


def get_client_ssl_templates():
    client_ssl = get_vip_data()
    for index, row in client_ssl.iterrows():
        if str(row['SSL Cert Name']) != ('' or 'nan'):
            print('!\nslb template client-ssl',row['SSL Cert Name'])
            print('\tcert', row['SSL Cert Name'])
            print('\tkey', row['SSL Cert Name'])
            print('\tdisable-sslv3')
            print('\tenable-tls-alert-logging fatal')
    return True


def get_slb_servers():
    slb_servers = get_server_data()
    slb_servers = slb_servers[['Server','Server_IP','TCP Listner Ports', 'UDP Listner Ports']]
    # print("slb_servers: \n", slb_servers)
    for index, row in slb_servers.iterrows():
        print('!\nslb server', row['Server'], row['Server_IP'])
        tcp_port_list = row['TCP Listner Ports'].split(',')
        tcp_port_list = [x.strip(' ')for x in tcp_port_list]
        for port in tcp_port_list:
            print('\tport', port, 'tcp')
    return True


def get_slb_service_groups():
    slb_service_groups = get_vip_data()
    slb_service_groups = slb_service_groups[['virtual_server_name', 'slb_server_name', 'slb_server_port', 'add_slb_server',
                                   'protocol', 'load_balance_method']]
    #print(slb_service_group_df.head(5))
    for index, row in slb_service_groups.iterrows():
        sg_name = row['virtual_server_name'].split(',')
        for item in sg_name:
            sg_name = re.sub(r"vip", "sg", item)
        print('!\nslb service-group',sg_name+'_'+str(row['slb_server_port']), row['protocol'])
        print('\tmethod',row['load_balance_method'])
        print('\tmember',row['slb_server_name'], row['slb_server_port'],'\n\tmember', row['add_slb_server'], row['slb_server_port'])
    return True


def get_slb_virtual_servers():
    vip_data = get_vip_data()
    for item, row in vip_data.iterrows():
        print('!\nslb virtual-server', row['virtual_server_name'], row['virtual_server_ip'], '/32')
        print('\tport', row['vport'], row['vport type'])
        sg_name = re.sub(r"vip", "sg", row['virtual_server_name'])
        print('\t\tservice-group', sg_name+'_'+str(row['slb_server_port']))
        print('\t\tsource-nat auto')
        if row['vport type'] == 'https':
            print('\t\ttemplate client-ssl', row['SSL Cert Name'])
        if row['HTTP_to_HTTPS_redirect'] == 'YES':
            print('\t\ttemplate http redirect_to_https')
    print('!')
    return True


if __name__ == "__main__":

    #print("type(get_server_data(): ", type(get_server_data()))
    #print('\n')
    #print(get_server_data())
    #print('\n')
    #print("type(get_server_data(): ", type(get_server_data()))
    #print('\n')
    #print(get_vip_data())
    #print('\n')
    get_http_templates()
    get_client_ssl_templates()
    get_slb_servers()
    get_slb_service_groups()
    get_slb_virtual_servers()
