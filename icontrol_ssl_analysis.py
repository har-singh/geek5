#!/bin/python
# -----HS 23Jul21-----
# The requirement: SSL analysis in order to update the security level

# HS 19Oct21
## Lesson learned: Harpreet should alway save the "kind" and "selfLink" information for future reference
## Still to be done


import re, json, csv, datetime, getpass, sys
import requests
from requests.auth import HTTPBasicAuth
import urlparse

def get_request(device, username, password, url_path):
  headers = {"Content-Type": "application/json"}
  request_url = 'https://' + device + url_path
  #
  print('Running GET ' + request_url)
  response = requests.get(request_url, auth = HTTPBasicAuth(username, password), verify=False, headers=headers)
  if response.status_code == 200:
    print('GET request complete')  
    response_data = response.json()
    return(response_data)
  else:
    print('HTTP request error. Reason: %s; Status Code: %s') % (response.reason, response.status_code)
    quit(1)

def get_reference_path(dictionary, key_for_path):
  # https://realpython.com/python-defaultdict/
  # Data example:
  # {
  #   "name": "demo_443_pool",
  #   "membersReference": {
  #     "isSubcollection": true,
  #     "link": "https://localhost/mgmt/tm/ltm/pool/~Ficus_Prova~demo_443_pool/members?ver=14.1.4"
  #   },
  # }
  #
  value_path = ''
  if key_for_path in dictionary:
    value_url = dictionary[key_for_path]['link']
    value_path = urlparse.urlparse(value_url).path
    return(value_path)

def get_ssl_profile(device, username, password, vs_dictionary, client_ssl_profile_dict):
  # In this function the data has been combined from two difference source. First source is the /ltm/profile/client-ssl for the configuration and second source are the statistics from the virtual server
  profile_path = get_reference_path(vs_dictionary, 'profilesReference')
  profile_data = get_request(device, username, password, profile_path)['items']
  profile_list = []
  for profile in profile_data:
    if profile['name'] in client_ssl_profile_dict:
      profile_data_details = client_ssl_profile_dict.get(profile['name'])
      profile_statistics_path = urlparse.urlparse(profile['selfLink']).path + '/stats'
      profile_cert_path = urlparse.urlparse(profile_data_details['certReference']['link']).path
      profile_cert_details = get_request(device, username, password, profile_cert_path)
      profile_statistics = get_request(device, username, password, profile_statistics_path)
      # F5 engineers have formatted the data in a strange manner. To access the TLS statistics there is dictionary and the key needs to be specified
      profile_statistics_path_key = profile_statistics['entries'].keys()[0]
      tls_stats_dict = profile_statistics['entries'][profile_statistics_path_key]['nestedStats']['entries']
      profile_data_details['dtlsv1'] = tls_stats_dict['common.protocolUses.dtlsv1']['value']
      profile_data_details['sslv2'] = tls_stats_dict['common.protocolUses.sslv2']['value']
      profile_data_details['sslv3'] = tls_stats_dict['common.protocolUses.sslv3']['value']
      profile_data_details['tlsv1'] = tls_stats_dict['common.protocolUses.tlsv1']['value']
      profile_data_details['tlsv1_1'] = tls_stats_dict['common.protocolUses.tlsv1_1']['value']
      profile_data_details['tlsv1_2'] = tls_stats_dict['common.protocolUses.tlsv1_2']['value']
      profile_data_details['tlsv1_3'] = tls_stats_dict['common.protocolUses.tlsv1_3']['value']
      # Section for Certificate Common Name from Subject and expiration date. Extracted from the string provided
      ## https://stackoverflow.com/questions/52612435/how-to-convert-string-without-quotes-to-dictionary-in-python/
      # Parse the date and time information to keep only the date.
      ## https://stackabuse.com/converting-strings-to-datetime-in-python
      ## https://www.programiz.com/python-programming/datetime/strftime
      cert_subject_data = profile_cert_details['subject']
      profile_data_details['certSubject'] = {i.split('=')[0]: i.split('=')[1] for i in cert_subject_data.split(',')}['CN']
      cert_expiration_string = datetime.datetime.strptime(profile_cert_details['expirationString'], '%b %d %H:%M:%S %Y %Z')
      profile_data_details['certEexpirationString'] = cert_expiration_string.strftime("%d-%b-%Y")
      # Append information to the list
      profile_list.append(profile_data_details)      
  return(profile_list)

'''
SSL2,SSL3,TLS1.0,TLS1.1,TLS1.2,TLS1.3,DTLS1
"common.protocolUses.dtlsv1": {
  "value": 0
},
"common.protocolUses.sslv2": {
  "value": 0
},
"common.protocolUses.sslv3": {
  "value": 0
},
"common.protocolUses.tlsv1": {
  "value": 0
},
"common.protocolUses.tlsv1_1": {
  "value": 0
},
"common.protocolUses.tlsv1_2": {
  "value": 169358
},
"common.protocolUses.tlsv1_3": {
  "value": 0
},
'''

def csv_export(data_list, column_keys, hostname, csv_data):
  # Export to CSV
  #column_keys = ['name', 'destination', 'pool', 'partition']
  #
  #csv_data = [['Virtual Server Name,', 'VS Destination', 'Pool Name', 'Partition','Hostname']] # list initialized with the columns names
  #csv_data = [['Virtual Server Name', 'VS Destination', 'Pool Name', 'Pool Member', 'Node Address', 'Partition', 'Hostname']] # list initialized with the columns names
  #csv_data = []
  for i in data_list:
    data = [i.get(x) for x in column_keys]
    for j in range(len(data)):
      try:
        data[j] = re.sub(r'%[0-9]+', '', data[j])   # '/Ficus_Prova/10.182.248.95%6:443'. Removes '%6'
        data[j] = re.sub(r'^/[0-9a-zA-Z_-]*/', '', data[j]) # '/Ficus_Prova/10.182.248.95%6:443'. Removes '/Ficus_Prova/'
      except:
        pass
    data.append(hostname)
    csv_data.append(data)
  #
  file_path_name = '/shared/tmp/hsingh/bigip_' + hostname + '_ssl_export.csv'
  with open(file_path_name, 'w') as comma_file:
    wr = csv.writer(comma_file, quoting=csv.QUOTE_ALL)
    wr.writerows(csv_data)
    print('CSV exported.')

def lot1_ssl_analysis(device, username, password):
  stuff_to_return = []
  virtual_data_list = get_request(device, username, password, '/mgmt/tm/ltm/virtual/')['items']
  #
  # Profile binary search. Pre computing the profile data for hash search
  client_ssl_profile_dict = {}
  client_ssl_profile_list = get_request(device, username, password, '/mgmt/tm/ltm/profile/client-ssl/')['items']
  for profile in client_ssl_profile_list:
    client_ssl_profile_dict[profile['name']] = profile
  #
  for vs in virtual_data_list:
    profile_list = get_ssl_profile(device, username, password, vs, client_ssl_profile_dict)
    for profile in profile_list:
      dict_tmp = {}
      dict_tmp['vs_name'] = vs['name']
      dict_tmp['vs_destination'] = vs['destination']
      dict_tmp['vs_partition'] = vs['partition']
      dict_tmp['profile_name'] = profile['name']
      dict_tmp['defaultsFrom'] = profile['defaultsFrom']
      dict_tmp['tmOptions'] = profile['tmOptions']
      dict_tmp['ciphers'] = profile['ciphers']
      dict_tmp['dtlsv1'] = profile['dtlsv1']
      dict_tmp['sslv2'] = profile['sslv2']
      dict_tmp['sslv3'] = profile['sslv3']
      dict_tmp['tlsv1'] = profile['tlsv1']
      dict_tmp['tlsv1_1'] = profile['tlsv1_1']
      dict_tmp['tlsv1_2'] = profile['tlsv1_2']
      dict_tmp['tlsv1_3'] = profile['tlsv1_3']
      dict_tmp['certSubject'] = profile['certSubject']
      dict_tmp['certEexpirationString'] = profile['certEexpirationString']
      # print vs['name'], profile['name']
    #only add information if there are client-ssl profiles
      if dict_tmp:
        stuff_to_return.append(dict_tmp)
  # CSV export
  keys = ['vs_name', 'vs_destination', 'vs_partition', 'profile_name', 'defaultsFrom', 'tmOptions', 'ciphers', 'dtlsv1', 'sslv2', 'sslv3', 'tlsv1', 'tlsv1_1', 'tlsv1_2', 'tlsv1_3', 'certSubject', 'certEexpirationString']
  csv_data = [['vs_name', 'vs_destination', 'vs_partition', 'profile_name', 'defaultsFrom', 'tmOptions', 'ciphers', 'dtlsv1', 'sslv2', 'sslv3', 'tlsv1', 'tlsv1_1', 'tlsv1_2', 'tlsv1_3', 'certSubject', 'certEexpirationString', 'hostname']]
  hostname = get_request(device, username, password, '/mgmt/tm/sys/global-settings?$select=hostname')['hostname']
  csv_export(stuff_to_return, keys, hostname, csv_data)
  # Return
  return(stuff_to_return)

def indent(object):
  print(json.dumps(object, indent=2))

if __name__ == "__main__":
  #
  pattern_ip = re.compile('^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$') #pattern to match ip address e.g. 10.182.129.65
  pattern_comma = re.compile('^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3},') # pattern to match ip address with comma e.g. 10.182.129.65
  device = [sys.argv[0]]
  #
  # Get access details
  # If no IP are provided the users will be prompted. The list can be separated by spaces or commas
  if len(sys.argv) == 1:
    device_ip = raw_input("Provide BIG-IP Management IP: ")
    device.append(device_ip)
  elif pattern_comma.match(sys.argv[1]):
    addr_list = re.split(',', sys.argv[1])
    for addr in addr_list:
      device.append(addr)
  else:
    device = sys.argv
  #
  #
  username = raw_input("Username: ")
  password = getpass.getpass("Password: ")


  for index in range(1, len(device)):
    if pattern_ip.match(device[index]):
      lot1_ssl_analysis(device[index], username, password)
    else:
      print('Error. ' + device[index] + ' is not an IP address.')
