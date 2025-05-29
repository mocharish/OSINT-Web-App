import React from "react";

export default function ScanCard({ result, onViewDetails }) {
  return (
    <div style={{ marginBottom: "2rem", border: "2px solid #333", padding: "1rem" }}>
      <h3>Current Scan: <code>{result.domain}</code></h3>
      <p>
        <strong>Status:</strong> {result.status}<br />
        <strong>Started:</strong> {new Date(result.start).toLocaleString()}
        {result.end && (
          <>
            <br />
            <strong>Ended:</strong> {new Date(result.end).toLocaleString()}
          </>
        )}
      </p>
      <ul>
        {result.summary &&
          Object.entries(result.summary).map(([k, v]) => (
            <li key={k}><strong>{k}</strong>: {v}</li>
          ))}
      </ul>
      <button onClick={() => onViewDetails(result)}>View Details</button>
      {result.status === "completed" && (
        <button
          style={{ marginLeft: "1rem" }}
          onClick={() =>
            window.open(`http://localhost:8000/export/${result.domain}`, "_blank")
          }
        >
          Download Excel Report
        </button>
      )}
    </div>
  );
}
