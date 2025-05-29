## ✅ Additional Production-Grade Tests

Although basic functionality is already tested manually, the following automated tests should be implemented for a production-grade submission:

### Backend Tests (FastAPI + Pytest)
- ✅ Unit tests for `HarvesterScanner`, `AmassScanner` (mock subprocess calls)
- ✅ Unit test for `extract_artifacts()` parser function (covers edge cases)
- ✅ Endpoint test for `/scan` with valid & invalid input
- ✅ Test for `/scan/status/{domain}` including edge cases
- ✅ Test for `/export/{domain}` route generating XLSX file
- ✅ Test for persistence via SQLite (`save_to_history`, `get_scan_history`)

Example:
```python
def test_extract_emails():
    harvester_data = {"emails": ["user@example.com", " user@example.com "]}
    amass_data = []
    result = extract_artifacts(harvester_data, amass_data)
    assert result["emails"] == ["user@example.com"]
```

## How Would You Benchmark & Optimize Performance?

1. Time Profiling: Measure start → end timestamps per scan.

2. Tool Execution Time: Benchmark Amass and theHarvester separately.

3. Async Improvements:

- Use asyncio.wait_for() with configurable timeout per tool

- Add timeout/error annotations to frontend if a scan stalls

4. Frontend Optimization:

- Replace polling with WebSockets for real-time updates (in future)

- Lazy load large JSON outputs inside modals

## Known OSINT Tool Bottlenecks & Mitigations

- ### Amass:	
Can run indefinitely or consume lots of memory.	 Set -timeout, -max-dns-queries to limit runtime

- ### theHarvester:
May fail if API keys are not configured.	Add API key validation and fallback to limited engines


##  Suggestions for Future Improvement

- Add WebSocket-based real-time updates instead of polling

- Add user authentication (OAuth) to restrict usage

- Add Redis queue 

- Add logging 

## Docker Image Deployment

- Backend image: `docker.io/mocharish/osint-dashboard-backend:latest`
- Frontend image: `docker.io/mocharish/osint-dashboard-frontend:latest`

These images are public and can be pulled without credentials using:

```bash
docker pull mocharish/osint-dashboard-backend:latest
docker pull mocharish/osint-dashboard-frontend:latest
```