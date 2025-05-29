import { useEffect, useState } from "react";
import ScanForm from "./components/ScanForm";
import ScanCard from "./components/ScanCard";
import HistoryCard from "./components/HistoryCard";
import Modal from "./components/Modal";
import { startScan, fetchStatus, fetchHistory } from "./api/api";

function App() {
  const [domain, setDomain] = useState("");
  const [message, setMessage] = useState("OSINT Dashboard");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedDetails, setSelectedDetails] = useState(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    const data = await fetchHistory();
    setHistory(data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!domain) return;
    setLoading(true);
    setMessage("Starting scan...");
    setResult(null);
    try {
      const data = await startScan(domain);
      if (data.domain) {
        pollStatus(data.domain);
      }
    } catch (e) {
      setMessage("Scan request failed.");
      setLoading(false);
    }
  };

  const pollStatus = async (domainToCheck) => {
    try {
      const data = await fetchStatus(domainToCheck);
      setResult({ ...data, domain: domainToCheck });
      if (data.status === "completed") {
        setMessage("Scan complete.");
        setLoading(false);
        loadHistory();
      } else {
        setTimeout(() => pollStatus(domainToCheck), 3000);
      }
    } catch (e) {
      setMessage("Status fetch failed.");
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial", maxWidth: 900, margin: "auto" }}>
      <h1 style={{ textAlign: "center" }}>{message}</h1>
      <ScanForm {...{ domain, setDomain, loading, onSubmit: handleSubmit }} />
      {result && <ScanCard result={result} onViewDetails={setSelectedDetails} />}
      <h2>Scan History</h2>
      {history.map((item) => (
        <HistoryCard key={`${item.domain}-${item.start}`} item={item} onViewDetails={setSelectedDetails} />
      ))}
      {selectedDetails && <Modal data={selectedDetails} onClose={() => setSelectedDetails(null)} />}
    </div>
  );
}

export default App;
