

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os

from scanner.core import scan_domain, scan_status
from scanner.storage import get_scan_history
from fastapi.responses import FileResponse
from scanner.export import export_scan_to_excel

class ScanRequest(BaseModel):
    domain: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "OSINT API is running"}

@app.post("/scan")
async def scan(scan_request: ScanRequest):
    domain = scan_request.domain.strip()
    if not domain or "." not in domain:
        raise HTTPException(status_code=400, detail="Invalid domain")

    # If already scanning, return message
    if domain in scan_status:
        current_status = scan_status[domain].get("status")
        if current_status == "running":
            return {"message": "Scan already in progress", "domain": domain}
        elif current_status == "completed":
            return {"message": "Scan already completed", "domain": domain}

    # Start background scan
    asyncio.create_task(scan_domain(domain))
    return {"message": "Scan started", "domain": domain}

@app.get("/scan/status/{domain}")
def scan_result(domain: str):
    if domain not in scan_status:
        raise HTTPException(status_code=404, detail="No scan result for domain")
    return scan_status[domain]

@app.get("/history")
def history():
    return get_scan_history()


@app.get("/export/{domain}")
def export_excel(domain: str):
    print(f"Export request for domain: {domain}")
    print(f"scan_status keys: {list(scan_status.keys())}")
    if domain not in scan_status or scan_status[domain]["status"] != "completed":
        raise HTTPException(status_code=404, detail="Scan not found or not completed")

    path = export_scan_to_excel(domain, scan_status[domain])
    return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=os.path.basename(path))