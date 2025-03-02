import sys
import requests
import argparse

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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch subdomain for a given domain.")
    
    # Add arguments for the domain and verbosity flags
    parser.add_argument("domain", help="The domain to fetch from")
    parser.add_argument(
        "-v", "--verbose",
        action="count",  # Count the number of -v/-V flags
        default=0,  # Default verbosity level is 0
        help="Increase output verbosity (use -v for verbose, -vv for more verbose)."
    )
    
    # Parse arguments
    args = parser.parse_args()
    domain = args.domain
    verboseLevel = min(args.verbose, 2)  # Limit verbosity to 2
    certificates = fetch_certificates(domain)

    if certificates:
        certificates_having_common_name = filter(lambda cert: "common_name" in cert, certificates)
        common_names = set(map(lambda cert: cert["common_name"], certificates_having_common_name))
        
        if verboseLevel > 0:
            print(f"Found {len(common_names)} subdomains in {domain}")
        print(f"Subdomains: {common_names}")
    else:
        print("No certificates found or an error occurred.")

if __name__ == "__main__":
    main()