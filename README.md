# sdenum
A subdomain enumeration tool for OSINT enthusiasts

### Current Feature
* [crt.sh](https://crt.sh/) search ✅
* [Google Dorks](https://exploit-db.com/google-hacking-database) ✅

### Setup Guide (RECOMMENDED): [LINUX USERS]
Install python3 and pip: **Google it**

Install venv: `pip install virtualenv`

Setup venv: `python3 -m venv venv`

Activate the Virtual Environment:

`source ./venv/bin/activate`

Install dependencies:`pip install -r requirements.txt`


### Usage Guide

(venv)$ `python3 sdenum.py <DOMAIN_NAME>`



### Future Improvements
1. Additional strategies for subdomain enumeration
    * Brute-force
    * DNS Scraping
2. Support for multi-threading
