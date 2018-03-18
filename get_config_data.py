#!/usr/bin/python3

import pandas as pd
import re


def create_vrrpa_commmon_config():
    server_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='VCS_VRRPA')
    print('! ***FOR DEVICE 1***')
    print('!\nvrrp-a common')
    print('\tdevice-id 1')
    print('\tset-id', server_data['VRRP-a set-id'][0])
    print('\tenable')
    print('!\n! ***END DEVICE 1***\n!')
    print('! ***FOR DEVICE 2***')
    print('!\nvrrp-a common')
    print('\tdevice-id 2')
    print('\tset-id', server_data['VRRP-a set-id'][0])
    print('\tenable')
    print('!\n! ***END DEVICE 2***\n!')
    return True

def create_vrrpa_config():
    vrrpa_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Vlan_Interfaces')
    print('!\nvrrp-a vrid 0')
    print('\tfloating-ip', vrrpa_data['floating-ip'][0] )
    print('\tdevice-context 1')
    print('\t\tblade-parameters')
    print('\t\t\tpriority 195')
    print('\tdevice-context 2')
    print('\t\tblade-parameters')
    print('\t\t\tpriority 175\n!')
    return True

def create_vcs_config():
    vcs_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='VCS_VRRPA')
    if vcs_data['VCS State'][0] == 'Enabled':
        print('! ***FOR DEVICE 1***')
        print('!\nvcs enable')
        print('!')
        print('vcs device 1')
        print('\tpriority 195')
        print('\tinterface management')
        if vcs_data['VCS affinity'][0] == 'Enabled':
            print('\taffinity-vrrp-a-vrid 0')
        print('\tenable\n!')
        if vcs_data['VCS SSL-enable'][0] == 'YES':
            print('vcs ssl-enable\n!')
        print('vcs multicast-ip', vcs_data['VCS-mutlicast'][0],'\n!')
        print('vcs floating-ip', vcs_data['VCS Floating IP'][0],'\n!')
        print('! ***FOR DEVICE 2***')
        print('!\nvcs enable')
        print('!')
        print('vcs device 2')
        print('\tpriority 175')
        print('\tinterface management')
        if vcs_data['VCS affinity'][0] == 'Enabled':
            print('\taffinity-vrrp-a-vrid 0')
        print('\tenable\n!')
        if vcs_data['VCS SSL-enable'][0] == 'YES':
            print('vcs ssl-enable\n!')
        print('vcs multicast-ip', vcs_data['VCS-mutlicast'][0],'\n!')
        print('vcs floating-ip', vcs_data['VCS Floating IP'][0], '\n!')
    return True


def create_base_system_config():
    system_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='System Vars')
    vcs_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='VCS_VRRPA')
    if vcs_data['VCS State'][0] == 'Enabled':
        print('!\ndevice-context 2')
        print('!\nhostname', str(system_data['Hostname'][0])+'_02')
        print('!\ndevice-context 1')
        print('!\nhostname', str(system_data['Hostname'][0]) + '_01')
    else:
        print('\nhostname', str(system_data['Hostname'][0]))
    print('!\nbanner exec', '\"'+system_data['Exec Banner'][0]+'\"')
    print('!\nbanner login', '\"'+system_data['Login Banner'][0]+'\"')
    print('!\nweb-service login-message', '\"'+system_data['Web Login Message'][0]+'\"')
    if system_data['Multiconfig'][0] == 'Enabled':
        print('!\nmulti-config enable')
    print('!\nip dns primary', system_data['DNS servers'][0])
    print('!\nip dns secondary', system_data['DNS servers'][1])
    print('!\nip dns suffix', system_data['DNS suffix'][0])
    print('!\nntp server', system_data['NTP servers'][0])
    print('\tprefer')
    print('!\nntp server', system_data['NTP servers'][1])
    print('!')
    return True

def create_interface_vlan_routes():
    ivr_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Vlan_Interfaces')
    vcs_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='VCS_VRRPA')
    if vcs_data['VCS State'][0] == 'Enabled':
        for index, row in ivr_data.iterrows():
            print('!\ninterface ethernet 1/' + str(ivr_data['interface'][0]))
            print('\tname \"' + row['interface description'] + '\"')
            print('\tenable')
            print('!\ninterface ethernet 2/' + str(ivr_data['interface'][0]))
            print('\tname \"' + row['interface description'] + '\"')
            print('\tenable')
            print('!\nvlan 1/'+ str(row['vlan-id']))
            if row['802.1q'] == 'NO' :
                print('\tuntaggged ethernet', row['interface'])
            else:
                print('\tagged ethernet', row['interface'])
            print('\trouter-interface ve', row['vlan-id'])
            print('!\nvlan 2/' + str(row['vlan-id']))
            if row['802.1q'] == 'NO':
                print('\tuntaggged ethernet', row['interface'])
            else:
                print('\tagged ethernet', row['interface'])
            print('\trouter-interface ve', row['vlan-id'])
        print('!\ninterface ve 1/' + str(ivr_data['vlan-id'][0]))
        print('\tip address', row['ve IP (device 1)'], row['ve netmask'])
        print('!\ninterface ve 2/' + str(ivr_data['vlan-id'][0]))
        print('\tip address', row['ve IP (device 2)'], row['ve netmask'])
        print('!\ndevice-context 2')
        print('!\nip route 0.0.0.0 /0', row['default-gateway'])
        print('!\ndevice-context 1')
        print('!\nip route 0.0.0.0 /0', row['default-gateway'])

    else:
        for index, row in ivr_data.iterrows():
            print('!\ninterface ethernet', ivr_data['interface'][0])
            print('\tname \"', row['interface description'], '\"')
            print('\tenable')
            print('!\nvlan', str(row['vlan-id']))
            if row['802.1q'] == 'NO':
                print('\tuntaggged ethernet', row['interface'])
            else:
                print('\tagged ethernet', row['interface'])
            print('\trouter-interface ve', row['vlan-id'])
        print('!\ninterface ve', ivr_data['vlan-id'][0])
        print('\tip address', row['ve IP (device 1)'], row['ve netmask'])
    print('!')

    return True


def create_logging_config():

    # TODO: Add in email settings
    '''
    smtp smtp.domain.com
    smtp port 465
    smtp needauthentication
    smtp mailfrom vthunder@domain.com
    smtp username user.name password <PASSWORD>
    !
    logging email-address user.name@domain.com
    '''
    log_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Logging')

    if ['use-mgmt-port'] == 'YES':
        print('!\nlogging host', log_data['syslog host'][0], 'use-mgmt-port port', log_data['syslog port'][0],
              log_data['syslog protocol'][0])
    else:
        print('!\nlogging host', log_data['syslog host'][0], 'port', log_data['syslog port'][0], log_data['syslog protocol'][0])
    print('!\nlogging syslog', log_data['syslog level'][0])
    print('!\nlogging trap', log_data['trap level'][0])
    print('!\nlogging console', log_data['console level'][0],'\n!')
    return True

def create_http_templates():
    print('!\nslb template http redirect_to_https')
    print('\tredirect port 443 response-code 301')
    return True


def create_client_ssl_templates():
    client_ssl = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Virtual-Servers')
    for index, row in client_ssl.iterrows():
        if str(row['SSL Cert Name']) != ('' or 'nan'):
            print('!\nslb template client-ssl',row['SSL Cert Name'])
            print('\tcert', row['SSL Cert Name'])
            print('\tkey', row['SSL Cert Name'])
            print('\tdisable-sslv3')
            print('\tenable-tls-alert-logging fatal')
    return True


def create_slb_servers():
    print('!\nslb common')
    print('\textended-stats')
    print('\tdrop-icmp-to-vip-when-vip-down')
    print('!')
    slb_servers = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Servers')
    slb_servers = slb_servers[['Server','Server_IP','TCP Listner Ports', 'UDP Listner Ports']]
    for index, row in slb_servers.iterrows():
        print('!\nslb server', row['Server'], row['Server_IP'])
        tcp_port_list = row['TCP Listner Ports'].split(',')
        tcp_port_list = [x.strip(' ')for x in tcp_port_list]
        for port in tcp_port_list:
            print('\tport', port, 'tcp')
    return True


def create_slb_service_groups():
    slb_service_groups = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Virtual-Servers')
    slb_service_groups = slb_service_groups[['virtual_server_name', 'slb_server_name', 'slb_server_port', 'add_slb_server',
                                   'protocol', 'load_balance_method']]
    for index, row in slb_service_groups.iterrows():
        sg_name = row['virtual_server_name'].split(',')
        for item in sg_name:
            sg_name = re.sub(r"vip", "sg", item)
        print('!\nslb service-group',sg_name+'_'+str(row['slb_server_port']), row['protocol'])
        print('\tmethod',row['load_balance_method'])
        print('\tmember',row['slb_server_name'], row['slb_server_port'],'\n\tmember', row['add_slb_server'], row['slb_server_port'])
    return True


def create_snat_pools():
    snat_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Virtual-Servers')
    for item, row in snat_data.iterrows():
        if str(row['source-nat name']) != 'nan':
            print('!\nip nat pool', row['source-nat name'], row['source-nat IP (top)'], row['source-nat IP (bottom)'],
              'netmask', row['source-nat netmask'])
    return


def create_slb_virtual_servers():
    vip_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Virtual-Servers')
    for item, row in vip_data.iterrows():
        print('!\nslb virtual-server', row['virtual_server_name'], row['virtual_server_ip'], '/32')
        print('\tport', row['vport'], row['vport type'])
        sg_name = re.sub(r"vip", "sg", row['virtual_server_name'])
        print('\t\tservice-group', sg_name+'_'+str(row['slb_server_port']))
        if str(row['source-nat name']) == ('nan' or 'auto'):
            print('\t\tsource-nat auto')
        else:
            print('\t\tsource-nat pool',row['source-nat name'])
        if row['vport type'] == 'https':
            print('\t\ttemplate client-ssl', row['SSL Cert Name'])
        if row['HTTP_to_HTTPS_redirect'] == 'YES':
            print('\t\ttemplate http redirect_to_https')
    print('!')
    return True


if __name__ == "__main__":

    print('\nA10 ACOS configuration builder\n')
    print('!*****************************************************************')
    print('! Configuration per device. Enable vcs clustering after entering')
    print('! these commands (ie: vcs reload).')
    print('!*****************************************************************\n')
    create_vrrpa_commmon_config()
    create_vcs_config()
    print('!*****************************************************************')
    print('!** Common Configuration to be used once devices are clustered. **')
    print('!*****************************************************************\n')
    create_vrrpa_config()
    create_base_system_config()
    create_interface_vlan_routes()
    create_logging_config()
    create_snat_pools()
    create_http_templates()
    create_client_ssl_templates()
    create_slb_servers()
    create_slb_service_groups()
    create_slb_virtual_servers()

