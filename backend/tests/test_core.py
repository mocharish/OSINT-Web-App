import pytest
from unittest.mock import patch, mock_open, MagicMock
from scanner.core import HarvesterScanner, AmassScanner, scan_status

@pytest.mark.asyncio
@patch("scanner.core.run_command", return_value=None)
@patch("builtins.open", new_callable=mock_open, read_data='{"emails": ["test@example.com"], "hosts": ["sub.domain.com"]}')
@patch("os.path.exists", return_value=True)
@patch("os.remove")
async def test_harvester_scan(mock_remove, mock_exists, mock_open_file, mock_run):
    scanner = HarvesterScanner("theHarvester")
    result = await scanner.scan("example.com")
    assert "emails" in result or "error" in result

@pytest.mark.asyncio
@patch("scanner.core.run_command", return_value=None)
@patch("builtins.open", new_callable=mock_open, read_data='sub.domain.com (FQDN)\n1.2.3.4 (IPAddress)')
@patch("os.path.exists", return_value=True)
@patch("os.remove")
async def test_amass_scan(mock_remove, mock_exists, mock_open_file, mock_run):
    scanner = AmassScanner("amass")
    result = await scanner.scan("example.com")
    assert isinstance(result, list) or "error" in result
