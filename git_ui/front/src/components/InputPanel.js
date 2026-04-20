import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:5000/predict";

export default function InputPanel({ data, setData }) {

  const [form, setForm] = useState({
    cpu_usage: 50,
    cpu_temp: 60,
    gpu_temp: 50,
    power: 30,
    cpu_freq: 3000,
    fan1: 60
  });

  const handleChange = (key, value) => {
    setForm({ ...form, [key]: parseFloat(value) });
  };

  // 🔥 PRESETS
  const presets = {
    normal: {
      cpu_usage: 35,
      cpu_temp: 55,
      gpu_temp: 45,
      power: 25,
      cpu_freq: 2800,
      fan1: 50
    },
    degrading: {
      cpu_usage: 60,
      cpu_temp: 75,
      gpu_temp: 60,
      power: 45,
      cpu_freq: 3200,
      fan1: 63   // slightly underperforming
    },
    critical: {
      cpu_usage: 80,
      cpu_temp: 95,
      gpu_temp: 80,
      power: 65,
      cpu_freq: 3700,
      fan1: 55   // clearly underperforming
    }
  };

  const applyPreset = (type, autoSend = false) => {
    const preset = presets[type];
    setForm(preset);

    if (autoSend) {
      send(preset);
    }
  };

  const send = async (payload = form) => {
    try {
      const res = await axios.post(API_URL, payload);
      setData([...data, { ...payload, ...res.data }]);
    } catch (err) {
      console.error(err);
      alert("Backend error");
    }
  };

  return (
    <div style={{
      background: "#1e293b",
      padding: 20,
      borderRadius: 12
    }}>
      <h3 style={{ marginBottom: 15 }}>⚙️ System Inputs</h3>

      {/* 🔥 PRESET BUTTONS */}
      <div style={{ marginBottom: 20 }}>
        <h4 style={{ color: "#94a3b8" }}>⚡ Quick Scenarios</h4>

        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <button onClick={() => applyPreset("normal")} style={btn("#22c55e")}>
            Normal
          </button>

          <button onClick={() => applyPreset("degrading")} style={btn("#facc15")}>
            Degrading
          </button>

          <button onClick={() => applyPreset("critical")} style={btn("#ef4444")}>
            Critical
          </button>

          {/* 🔥 Auto-send versions
          <button onClick={() => applyPreset("normal", true)} style={btn("#16a34a")}>
            ▶ Normal
          </button>

          <button onClick={() => applyPreset("degrading", true)} style={btn("#ca8a04")}>
            ▶ Degrading
          </button>

          <button onClick={() => applyPreset("critical", true)} style={btn("#dc2626")}>
            ▶ Critical
          </button> */}
        </div>
      </div>

      {/* 🔥 THERMAL */}
      <Section title="🌡️ Thermal">
        {["cpu_temp", "gpu_temp"].map((key) => slider(key))}
      </Section>

      {/* 🔥 LOAD */}
      <Section title="⚡ Load">
        {["cpu_usage", "power"].map((key) => slider(key))}
      </Section>

      {/* 🔥 FAN */}
      <Section title="🌀 Fan">
        {slider("fan1")}
      </Section>

      {/* CPU FREQ */}
      <Section title="⚙️ CPU">
        <label>cpu_freq: {form["cpu_freq"]}</label>
        <input
          type="range"
          min="1000"
          max="5000"
          value={form["cpu_freq"]}
          onChange={(e) => handleChange("cpu_freq", e.target.value)}
          style={{ width: "100%" }}
        />
      </Section>

      <button onClick={() => send()} style={{
        marginTop: 10,
        padding: "10px 20px",
        background: "#3b82f6",
        border: "none",
        borderRadius: 8,
        color: "white",
        cursor: "pointer"
      }}>
        🚀 Send Data
      </button>
    </div>
  );

  // 🔧 Helpers
  function slider(key) {
    return (
      <div key={key}>
        <label>{key}: {form[key]}</label>
        <input
          type="range"
          min="0"
          max="100"
          value={form[key]}
          onChange={(e) => handleChange(key, e.target.value)}
          style={{ width: "100%" }}
        />
      </div>
    );
  }

  function Section({ title, children }) {
    return (
      <div style={{ marginBottom: 20 }}>
        <h4 style={{ color: "#94a3b8" }}>{title}</h4>
        {children}
      </div>
    );
  }

  function btn(color) {
    return {
      background: color,
      border: "none",
      padding: "8px 12px",
      borderRadius: 8,
      cursor: "pointer",
      color: "black",
      fontWeight: "bold"
    };
  }
}