import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

export default function Graphs({ data }) {
  if (!data.length) return <p>No data</p>;

  return (
    <div>
      <h3>Fan Speed</h3>
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="index" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="fan1" stroke="#8884d8" />
        <Line type="monotone" dataKey="fan2" stroke="#82ca9d" />
      </LineChart>

      <h3>Temperature</h3>
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="index" />
        <YAxis />
        <Tooltip />
        <Line dataKey="cpu_temp" stroke="red" />
        <Line dataKey="gpu_temp" stroke="orange" />
      </LineChart>
    </div>
  );
}