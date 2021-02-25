# -----HS 18Dec20-----
# curl command to get the virtual-server data from F5 via iControl API
# iControl API is enabled by default on the management

# [admin@lab-f5:Standby:In Sync] tmp # curl -sk -u admin:<pass> -H "Content-Type: application/json" -X GET https://192.168.1.245/mgmt/tm/ltm/virtual | jq . -M > tmp
# password removed for security

curl -sk -u admin:<pass> -H "Content-Type: application/json" -X GET https://10.181.252.153/mgmt/tm/ltm/virtual | jq . -M
