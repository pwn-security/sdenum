import sys
import requests
import argparse
from googlesearch import search
import re
import dns.resolver
def fetch_certificates(domain):
    url = f"https://crt.sh/?q={domain}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}  # Set a User-Agent to avoid blocking
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP error codes
        
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
def google_dork_subdomains(domain, verboseLevel=0):
    query = f"site:*.{domain} -site:www.{domain}"
    subdomains = set()
    try:
        results = search(query, num_results=100, unique=True)
        for result in results:
            print(f"{result}")
            if re.search(domain, result):
                subdomain = result.split("://")[1].split('/')[0]
                if subdomain.startswith('www.'):
                    subdomain = subdomain[4:]
                if verboseLevel > 1:
                    print(f"Found {subdomain}")
                subdomains.add(subdomain)
        return subdomains
    except Exception as e:
        print(f"Error during Google Dorking: {e}")
        return None
def bruteforce_dns_subdomains(domain, wordlist="wordlist.txt", verboseLevel=0):
    try:
        with open(wordlist, "r") as file:
            subdomains_list = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: {path} not found")
        return None
    subdomains = set()
    resolver = dns.resolver.Resolver()
    for subdomain in subdomains_list:
        full_domain= f"{subdomain}.{domain}"
        try:
            #Resolve the subdomain
            answers = resolver.resolve(full_domain, 'A')
            if answers:
                subdomains.add(full_domain)
                if verboseLevel > 1:
                    print(f"Found {full_domain} via Bruteforce DNS")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
            continue
        except Exception as e:
            print(f"Error resolving {full_domain}: {e}")
    return subdomains
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch subdomain for a given domain.")
    
    # Add arguments for the domain and verbosity flags
    parser.add_argument("domain", help="The domain to fetch from")
    
    parser.add_argument(
        "-s", "--strategy",
        choices=["dork", "crtsh", "bruteforce", "all"], #Allowed strategies
        default="all",
        help="Subdomain enumeration strategy (dork, crtsh, bruteforce or all). Default is all."
    )
    parser.add_argument(
        "-w", "--wordlist",
        default="wordlist.txt",
        help="Wordlist for bruteforce strategy. Default is wordlist.txt"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",  # Count the number of -v/-V flags
        default=0,  # Default verbosity level is 0
        help="Increase output verbosity (use -v for verbose, -vv for more verbose)."
    )
    
    # Parse arguments
    args = parser.parse_args()
    domain = args.domain
    strategy = args.strategy
    wordlist_path = args.wordlist
    verboseLevel = min(args.verbose, 2)  # Limit verbosity to 2

    subdomains = set()

    if strategy in ["crtsh", "all"]:
        certificates = fetch_certificates(domain)
        if certificates:
            certificates_having_common_name = filter(lambda cert: "common_name" in cert, certificates)
            crtsh_subdomains = set(map(lambda cert: cert["common_name"], certificates_having_common_name))
            if verboseLevel > 0:
                print(f"Found {len(crtsh_subdomains)} subdomains in {domain} via crtsh")
            if verboseLevel > 1:
                print(f"{crtsh_subdomains}")
            subdomains.update(crtsh_subdomains)
        else:
            print("No certificates found or an error occurred.")
    if strategy in ["dork", "all"]:
        dork_subdomains = google_dork_subdomains(domain, verboseLevel)
        if dork_subdomains:
            subdomains.update(dork_subdomains)
            if verboseLevel > 0 :
                print(f"Found {len(dork_subdomains)} subdomains in {domain} via Dorking")
            if verboseLevel > 1:
                print(f"{dork_subdomains}")
    
    if strategy in ["bruteforce", "all"]:
        bruteforce_subdomains = bruteforce_dns_subdomains(domain, wordlist_path, verboseLevel)
        if bruteforce_subdomains:
            subdomains.update(bruteforce_subdomains)
            if verboseLevel > 0:
                print(f"Found {len(bruteforce_subdomains)} subdomains via Bruteforce DNS")

    #print all subdomains accumulated
    if subdomains:
        if verboseLevel > 0:
            print(f"Found {len(subdomains)} subdomains in {domain}")
        print(subdomains)
    else:
        print(f"No subdomains found for {domain}")
if __name__ == "__main__":
    main()