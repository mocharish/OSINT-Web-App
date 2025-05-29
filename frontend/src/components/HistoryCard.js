import React from "react";

export default function HistoryCard({ item, onViewDetails }) {
  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", marginTop: "10px" }}>
      <h4>{item.domain}</h4>
      <p>
        <strong>Started:</strong> {new Date(item.start * 1000).toLocaleString()}<br />
        <strong>Ended:</strong> {new Date(item.end * 1000).toLocaleString()}
      </p>
      <ul>
        {item.summary &&
          Object.entries(item.summary).map(([k, v]) => (
            <li key={k}><strong>{k}</strong>: {v}</li>
          ))}
      </ul>
      <button onClick={() => onViewDetails(item)}>View Details</button>
      <button
        style={{ marginLeft: "1rem" }}
        onClick={() =>
          window.open(`http://localhost:8000/export/${item.domain}`, "_blank")
        }
      >
        Download Excel Report
      </button>
    </div>
  );
}
