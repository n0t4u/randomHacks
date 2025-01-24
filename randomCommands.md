# randomCommands

Small bash commands to perform specific tasks.

## Get multiple web servers response headers
```shell
for ip in $(cat ips.txt); do 
	echo "\033[1;34m[»] curl -X GET http://${ip} -I -L\033[0m";
	curl -X GET http://${ip} -I -L --connect-timeout 2 2>/dev/null;
	echo "\033[1;34m[»] curl -X GET https://${ip} -I -L -k\033[0m";
	curl -X GET https://${ip} -I -L -k --connect-timeout 2  2>/dev/null;
done
```

## Check allowed HTTP Methods
### One URL
```shell
url=https://github.com/n0ttu
for method in {GET,POST,HEAD,OPTIONS,PUT,DELETE,PATCH,TRACE,TRACK,CONNECT,SET,DEBUG,REMOVE,FORWARD,MOVE,INFO}; do
	if [[ $method =~ ^(POST|PUT|DELETE)$ ]]; then
		echo -e "$method\t $(curl -s ${url} -X $method -k --data 'username=audit' | grep -i -P 'HTTP[\/\. 0-9]+')"; #-I removed
	else
		echo -e "$method\t $(curl -s ${url} -I -X $method -k | grep -i -P 'HTTP[\/\. 0-9]+')";
	fi
done
```

### Several URLs
```shell
for url in $(cat apiRoutes.txt); do
	echo $url;
	for method in {GET,POST,HEAD,OPTIONS,PUT,DELETE,PATCH,TRACE,CONNECT}; do
			if [[ $method =~ ^(POST|PUT|DELETE)$ ]]; then
				echo -e "$method\t $(curl -s ${url} -X $method -k -i --data 'username=audit' | grep -i -P 'HTTP[\/\. 0-9]+')"; #-I removed
			else
				echo -e "$method\t $(curl -s ${url} -I -X $method -k | grep -i -P 'HTTP[\/\. 0-9]+')";
			fi
	done;
done | tee output.txt
```

## API versions
```shell
for v in "v1" "v2" "v3" "v4" "v5"; do         
	for url in $(cat apiRoutes.txt); do
		aux=$(echo $url | sed "s/v[0-9]/${v}/g");
		echo -e "${aux}";
		echo -e "$(curl -s ${aux} -X GET -k -I | grep -i -P 'HTTP[\/\. 0-9]+')";
	done;
done | tee fuzzing_versions.txt
```

## Remove empty lines
```shell
sed '/^$/d' | sed '/^[[:space:]]*$/d'
```

## Parse nmap output
Check [nmapScans.sh](nmapScans.sh)