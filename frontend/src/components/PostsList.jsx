import React from "react";

import StatusBadge from "./StatusBadge";

export default function PostsList({ posts }) {
  if (!posts.length) {
    return (
      <p className="text-sm text-gray-500">
        No posts scheduled yet.
      </p>
    );
  }

  return (
    <div className="bg-white rounded shadow overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 text-left">
          <tr>
            <th className="p-3">Platform</th>
            <th className="p-3">Content</th>
            <th className="p-3">Scheduled At</th>
            <th className="p-3">Status</th>
          </tr>
        </thead>

        <tbody>
          {posts.map((post) => (
            <tr key={post.id} className="border-t">
              <td className="p-3 capitalize">
                {post.platform}
              </td>

              <td className="p-3 max-w-xs truncate">
                {post.content}
              </td>

              <td className="p-3">
                {new Date(post.scheduled_at).toLocaleString()}
              </td>

              <td className="p-3">
                <StatusBadge status={post.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
