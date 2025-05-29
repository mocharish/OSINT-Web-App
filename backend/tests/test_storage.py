import os
import json
from scanner.storage import save_to_history, get_scan_history, DB_PATH

def test_save_and_get_history(tmp_path):
    fake_result = {
        "domain": "example.com",
        "start": 1620000000,
        "end": 1620000100,
        "status": "completed"
    }
    os.environ["DB_PATH"] = str(tmp_path / "test.db")
    save_to_history(fake_result)

    history = get_scan_history()
    assert isinstance(history, list)
    assert any(entry.get("domain") == "example.com" for entry in history)
