#!/usr/bin/env python3

import ssl
import socket
from urllib.parse import urlparse

read_fileb = "sites.txt"
res_tls = "tls_version_results.txt"

PORT = 443
TIMEOUT = 5

def normalize_host(site):
    if not site.startswith(("http://", "https://")):
        site = "https://" + site

    parsed = urlparse(site)
    return parsed.hostname

def get_tls_version(host):
    context = ssl.create_default_context()

    try:
        with socket.create_connection((host, PORT), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                return ssock.version()
    except Exception as e:
        return f"ERROR: {e}"

def main():
    with open(read_fileb, "r") as f:
        sites = [line.strip() for line in f if line.strip()]

    with open(res_tls, "w") as out:
        for site in sites:
            host = normalize_host(site)

            if not host:
                result = f"{site} -> INVALID"
                print(result)
                out.write(result + "\n")
                continue

            tls_version = get_tls_version(host)
            result = f"{host} -> {tls_version}"

            print(result)
            out.write(result + "\n")

    print(f"\nResults saved to {res_tls}")

if __name__ == "__main__":
    main()