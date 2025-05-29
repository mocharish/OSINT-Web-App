import re

def normalize_host(host):
    # Lowercase, strip leading www and trailing dot
    host = host.strip().lower()
    if host.startswith("www."):
        host = host[4:]
    return host.rstrip(".")

def normalize_ip(ip):
    return ip.strip()

def normalize_email(email):
    return email.strip().lower()

def normalize_social(handle):
    return handle.strip().lower()

def extract_artifacts(harvester_result, amass_result):
    emails = set()
    subdomains = set()
    ips = set()
    socials = set()

    # --- Extract from theHarvester ---
    harv_data = harvester_result if isinstance(harvester_result, dict) else {}

    if "emails" in harv_data:
        for email in harv_data["emails"]:
            if isinstance(email, str):
                emails.add(normalize_email(email))

    if "hosts" in harv_data:
        for host in harv_data["hosts"]:
            if isinstance(host, str):
                subdomains.add(normalize_host(host))

    if "social" in harv_data:
        for handle in harv_data["social"]:
            if isinstance(handle, str):
                socials.add(normalize_social(handle))

    # --- Extract from Amass ---
    if isinstance(amass_result, list):
        for line in amass_result:
            line = line.strip()

            # Match FQDNs
            fqdn_match = re.match(r"^(.*?) \(FQDN\)", line)
            if fqdn_match:
                fqdn = normalize_host(fqdn_match.group(1))
                subdomains.add(fqdn)

            # Match IP addresses
            ip_match = re.match(r"^(.*?) \(IPAddress\)", line)
            if ip_match:
                ip = normalize_ip(ip_match.group(1))
                ips.add(ip)

    return {
         "emails": sorted(list(emails)),
        "subdomains": sorted(list(subdomains)),
        "ips": sorted(list(ips)),
        "socials": sorted(list(socials)),
    }
