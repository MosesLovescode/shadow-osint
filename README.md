# Shadow-Osint
a powerful tool to find vulnerable IOT devices 


has two commands for operation i.e Find and Info

## Find
searches for vulnerable devices matching a particular query

returns ip address and scrapped information for each device found

Usage:

find - query
      
## Info
returns infomation about a given IP address

it finds the country , city of origin
it finds ports open on the device
if finds the last time it was detected by the scanner (Shodan)
if finds associated domains 

Usage:

info - IP-address


note: Shadow osint has also been bundled to a windows excutable 

you can also build it for windows using pyinstaller using the following commands

pip install pyintaller
pyinstaller --onefile --windowed shadow.py  

for linux 

you can run it directly (slower) or use the cython compiler
