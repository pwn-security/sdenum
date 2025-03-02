# sdenum
A subdomain enumeration tool for OSINT enthusiasts

### Current Feature
* [crt.sh](https://crt.sh/) search ✅
* [Google Dorks](https://exploit-db.com/google-hacking-database) ✅
* Bruteforcing subdomains via DNS resolution ✅

### Setup Guide (RECOMMENDED): [LINUX USERS]
Install python3 and pip: **Google it**

**NOTE**: Most linux distro comes with Python3 by default.

Install venv: 

`pip install virtualenv`

Setup venv:

 `python3 -m venv venv`

Activate the Virtual Environment:

`source ./venv/bin/activate`

Install dependencies:

`pip install -r requirements.txt`


### Usage Guide

1. Bruteforce DNS strategy
    ```
    python3 sdenum.py <DOMAIN_NAME> -s bruteforce
    ```
    When using bruteforce strategy, we can also specify the wordlist to search from. When the wordlist is not specified, the program tries to find **wordlist.txt** from the current working directory, and fails if not found.

    Here is the extended command:
    ```
    python3 sdenum.py <DOMAIN_NAME> -s bruteforce -w subdomains-top1million-5000.txt
    ```
2. Crt.sh search strategy
    ```
    python3 sdenum.py <DOMAIN_NAME> -s crtsh
    ```
3. Google Dorking strategy
    ```
    python3 sdenum.py <DOMAIN_NAME> -s dork
    ```
By default, when strategy is not specified, all the available strategy are run one-by-one and the subdomains found from each strategy are merged into one.
```
python3 sdenum.py <DOMAIN_NAME> -s all
```

### Future Improvements
1. Support for multi-threading
