import React, { useState } from "react";

export default function Tabs({ tabs }) {
  const [active, setActive] = useState(0);

  return (
    <div>
      <div style={{
        display: "flex",
        borderBottom: "1px solid #334155",
        marginBottom: 20
      }}>
        {tabs.map((tab, i) => (
          <div
            key={i}
            onClick={() => setActive(i)}
            style={{
              padding: "10px 20px",
              cursor: "pointer",
              borderBottom: active === i ? "3px solid #3b82f6" : "none",
              color: active === i ? "#3b82f6" : "#94a3b8"
            }}
          >
            {tab.name}
          </div>
        ))}
      </div>

      <div>{tabs[active].component}</div>
    </div>
  );
}