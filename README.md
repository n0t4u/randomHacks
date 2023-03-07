# randomHacks

Repository with small scripts for specific hacking tasks.

- [alternateBruteForce](#alternatebruteforce)
- [bannerGrabber](#bannerGrabber)
- [dnsResolver](#DNSResolver)
- [EasyAndroidStaticAnalysis](https://github.com/n0t4u/easyAndroidStaticAnalysis)
- [fromNmapsVtoCSV](#fromnmapsvtocsv)
- [LinuxAlias](#LinuxAlias)
- [manageProject](https://github.com/n0t4u/manageProject)
- [nmapScans](#nmapscans)
- [WindowsAlias](#WindowsAlias)

**Note.** Major projects have been moved to its own repository.

## alternateBruteForce
Simple Python script that allows to generate a dictionary to avoid bruteforce username blocks when a web server checks the number of consecutive tries.

### Usage
``` bash
python3 -u <USER_TO_BRUTEFORCE> -r <NUMBER OF REPETITIONS> -t <LENGTH OF DICTIONARY> [-o <OUTPUT>]
```

## bannerGrabber
Bash script to automatically perform banner grabbing and highlight which assets and ports responds to any command injected.

It does not perform any further checks, they must be done manually later.

### Usage
``` bash
#file.txt must be in IP PORT format
./bannerGrabber.sh file.txt
```

## DNSResolver
Automatic DNS resolution tool for several domains and different ouputs.

### Usage
``` bash
python3 DNSResolver.py --file <FILE>
python3 DNSResolver.py --file <FILE> --ip
```

## fromNmapsVtoCSV
Python 3 script that takes a gnmap file and output a table/CSV in the format given by the user. Works with several IPs scans.

### Usage
``` bash
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

## LinuxAlias
Small bash script that automatically add some alias to you bash or zsh shell.

TO DO. Add checks before adding any alias.

## nmapScans
Bash script that executes a full ports scan, parse the results and performs a second scan with version option only to the open ports.

### Usage
``` bash
chmod +x nmapScans.sh
# Option 1
./nmapScans.sh 127.0.0.1
# Option 2
./nmapScans.sh ips.txt
# Scan options
./nmapScans.sh 127.0.0.1 "-sS -T4 -Pn"
```

## WindowsAlias
1. Create an alias.bat file (C:\Users\n0t4u\Documents\alias.bat)
2. Access to Register Editor (Windows+r -> regedit).
3. Go to folder:
HKEY_CURRENT_USER\SOFTWARE\Microsoft\Command Processor
4. If this folder does not exist execute the following command.
``` cmd
reg add "HKCU\Software\Microsoft\Command Processor"
REM Alternative for step 5. Not tested
reg add "HKCU\Software\Microsoft\Command Processor" /v AutoRun /d "<PATH_TO_FILE>"
```
5. In the Command Processor folder, add a new "String Value" with name AutoRun and Data the path to alias.bat file.
6. Open [Windows Terminal](https://apps.microsoft.com/store/detail/9N0DX20HK701) and execute the commands

**Note.** It is important to add $* in commands that need arguments.

**Note.** Add *cls* at the end of the script to clear the terminal after the alias execution.

## Deprecated
* fromFuriousToNmapsV