import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

export default function Charts({ data }) {
  if (!data.length) return null;

  const formatted = data.map((d, i) => ({ ...d, index: i }));

  return (
    <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
      
      <LineChart width={500} height={300} data={formatted}>
        <XAxis dataKey="index" />
        <YAxis />
        <Tooltip />
        <Line dataKey="fan1" stroke="#3b82f6" />
        <Line dataKey="predicted_fan" stroke="#22c55e" />
      </LineChart>

      <LineChart width={500} height={300} data={formatted}>
        <XAxis dataKey="index" />
        <YAxis />
        <Tooltip />
        <Line dataKey="cpu_temp" stroke="#ef4444" />
        <Line dataKey="gpu_temp" stroke="#f97316" />
      </LineChart>

    </div>
  );
}