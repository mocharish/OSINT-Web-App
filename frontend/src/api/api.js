const API_BASE = "http://localhost:8000";

export async function startScan(domain) {
  const res = await fetch(`${API_BASE}/scan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ domain }),
  });
  return res.json();
}

export async function fetchStatus(domain) {
  const res = await fetch(`${API_BASE}/scan/status/${domain}`);
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${API_BASE}/history`);
  return res.json();
}
