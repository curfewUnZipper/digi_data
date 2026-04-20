import React from "react";

export default function DataTable({ data }) {
  if (!data.length) return null;

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Recent Logs</h3>
      <table border="1" style={{ width: "100%", background: "#1e293b" }}>
        <thead>
          <tr>
            {Object.keys(data[0]).map(k => <th key={k}>{k}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.slice(-50).map((row, i) => (
            <tr key={i}>
              {Object.values(row).map((v, j) => (
                <td key={j}>{v}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}