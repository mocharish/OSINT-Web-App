# scanner/core.py

import asyncio
import json
import os
import tempfile
import time
from abc import ABC, abstractmethod

scan_status = {}  # domain -> { status, results }

class Scanner(ABC):
    name: str

    @abstractmethod
    async def scan(self, domain: str) -> dict:
        pass

class HarvesterScanner(Scanner):
    name = "theHarvester"

    def __init__(self, path):
        self.path = path

    async def scan(self, domain: str):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmpfile:
            tmp_filename = tmpfile.name

        command = [
            self.path, "-d", domain, "-b", "bing", "-f", tmp_filename
        ]
        await run_command(command)

        try:
            with open(tmp_filename, "r") as f:
                results = json.load(f)
        except Exception as e:
            results = {"error": f"Failed to parse theHarvester output: {str(e)}"}
        finally:
            if os.path.exists(tmp_filename):
                os.remove(tmp_filename)
        return results

class AmassScanner(Scanner):
    name = "amass"

    def __init__(self, path):
        self.path = path

    async def scan(self, domain: str):
        output_file = f"{domain}_amass.txt"
        command = [self.path, "enum", "-o", output_file, "-d", domain,  "-active", "-timeout", "30", "-max-dns-queries", "100"]

        await run_command(command)

        try:
            with open(output_file, "r") as f:
                results = [line.strip() for line in f if line.strip()]
        except Exception as e:
            results = {"error": f"Failed to parse Amass output: {str(e)}"}
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
        return results

async def run_command(command: list):
    print(f"Running command: {' '.join(command)}")
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await proc.communicate()
        print("STDOUT:", stdout.decode())
        print("STDERR:", stderr.decode())
    except asyncio.CancelledError:
        proc.kill()
        await proc.wait()
        raise

async def scan_domain(domain: str):
    from .parser import extract_artifacts
    from .storage import save_to_history
    from .factory import ScannerFactory

    tools = [
        ScannerFactory.create_scanner("theHarvester"),
        ScannerFactory.create_scanner("amass")
    ]

    scan_status[domain] = {
        "status": "running",
        "tools": {},
        "start": time.time(),
    }

    async def run_tool(scanner):
        try:
            result = await scanner.scan(domain)
            tool_status = "completed"
        except Exception as e:
            result = {"error": str(e)}
            tool_status = "failed"
        scan_status[domain]["tools"][scanner.name] = {
        "status": tool_status,
        "results": result
    }

    await asyncio.gather(*(run_tool(tool) for tool in tools))

    scan_status[domain]["end"] = time.time()
    scan_status[domain]["status"] = "completed"

    artifacts = extract_artifacts(
      scan_status[domain]["tools"].get("theHarvester", {}).get("results", {}),
      scan_status[domain]["tools"].get("amass", {}).get("results", {})
    )

    summary = {k: len(v) for k, v in artifacts.items() if isinstance(v, list)}
    scan_status[domain]["artifacts"] = artifacts
    scan_status[domain]["summary"] = summary

    # Save to permanent history
    save_to_history(scan_status[domain])
