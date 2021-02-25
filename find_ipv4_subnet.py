# HS 04JAN21
# Get the subnet information from the ip address
# https://realpython.com/python-ipaddress-module/#host-interfaces
# https://stackoverflow.com/questions/50867435/get-subnet-from-ip-address
# https://stackoverflow.com/questions/3142054/python-add-items-from-txt-file-into-a-list
# tmp file contains the ip/subnet info. e.g.: '10.248.129.13/255.255.255.252'


from ipaddress import IPv4Interface

with open('tmp', 'r') as f:
  myNames = [line.strip() for line in f]

for line in range(len(myNames)):
  ifc = IPv4Interface(myNames[line])
  print(ifc.network)


#for line in range(len(myNames)):
#  ifc = ipaddress.ip_network(myNames[line]).subnets(new_prefix=29)
#  for i in list(ifc): print(i, end=(','))
#  print('')
#
#test='10.182.160.0/24'
#ipaddress.ip_network(test).subnets(new_prefix=25)
