import React from "react";

const statusColors = {
  scheduled: "bg-yellow-100 text-yellow-800",
  posted: "bg-green-100 text-green-800",
  failed: "bg-red-100 text-red-800",
};

export default function StatusBadge({ status }) {
  return (
    <span
      className={`px-2 py-1 rounded text-xs font-semibold ${statusColors[status]}`}
    >
      {status}
    </span>
  );
}

