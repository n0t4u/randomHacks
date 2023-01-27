# randomHacks

Repository with small scripts for specific tasks for work

## fromNmapsVtoCSV
Python 3 script that takes a gnmap file and output a table/CSV in the format given by the user. Works with several IPs scans.

### Usage
```
# Option 1
python3 fromNapsVtoCSV.py nmap_sV_127.0.0.1.gnmap
# Option 2
python3 fromNapsVtoCSV.py nmap_sV_127.0.0.1.gnmap --print
# Change Order
python3 fromNapsVtoCSV.py nmap_sV_127.0.0.1.gnmap --order=ip,port,service,version
# Multiple files
for file in $(ls nmap_sV_*.gnmap); do python3 fromNmapsVtoCSV.py $file --print; done > nmapParser.txt
```
Order output options.   ip,port,protocol,state,service,version

## nmapScans
Bash script that executes a full ports scan, parse the results and performs a second scan with version option only to the open ports.

### Usage
```
chmod +x nmapScans.sh
# Option 1
./nmapScans.sh 127.0.0.1
# Option 2
./nmapScans.sh ips.txt
# Scan options
./nmapScans.sh 127.0.0.1 "-sS -T4 -Pn"
```

## alternateBruteForce
Simple Python script that allows to generate a dictionary to avoid bruteforce username blocks when a web server checks the number of consecutive tries.

### Usage
```
python3 -u <USER_TO_BRUTEFORCE> -r <NUMBER OF REPETITIONS> -t <LENGTH OF DICTIONARY> [-o <OUTPUT>]
```

## Deprecated
* fromFuriousToNmapsV