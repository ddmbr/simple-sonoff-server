# Your wifi ssid
ssid=MyWifi
# Wifi password
password=12345678
# IP of your RPi. Must be consistent with sonoff-server.py
IP=192.168.0.101
# Port of your RPi. Must be consistent with sonoff-server.py
port=8888

curl http://10.10.7.1/device
curl -d '{ "version": 4, "ssid": "$ssid", "password": "$password", "serverName": "$IP", "port": $port }' -H "Content-Type: application/json" -X POST http://10.10.7.1/ap
