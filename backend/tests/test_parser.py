from scanner.parser import extract_artifacts

def test_extract_artifacts():
    harvester = {
        "emails": ["info@example.com", "Test@Example.com"],
        "hosts": ["www.sub.example.com."],
        "social": ["@handle"]
    }
    amass = [
        "another.sub.example.com (FQDN)",
        "192.168.1.1 (IPAddress)"
    ]
    result = extract_artifacts(harvester, amass)

    assert result["emails"] == ["info@example.com", "test@example.com"]
    assert "sub.example.com" in result["subdomains"]
    assert result["ips"] == ["192.168.1.1"]
    assert result["socials"] == ["@handle"]
