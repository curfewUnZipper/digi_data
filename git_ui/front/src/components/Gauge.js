import React from "react";

export default function Gauge({ value }) {
  const color =
    value < 35 ? "#22c55e" :
    value < 70 ? "#facc15" :
    "#ef4444";

  return (
    <div style={{
      width: 200,
      height: 200,
      borderRadius: "50%",
      border: `12px solid ${color}`,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 24,
      fontWeight: "bold"
    }}>
      {value.toFixed(0)}
    </div>
  );
}