import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import KpiCard from "../components/KpiCard";
import FollowersChart from "../components/FollowersChart";
import PostsList from "../components/PostsList";

import { connectSocialAccount } from "../services/social";
import { getMetrics } from "../services/metrics";
import { getPosts } from "../services/posts";

export default function Dashboard() {
  const [platform, setPlatform] = useState("instagram");
  const [metrics, setMetrics] = useState([]);
  const [posts, setPosts] = useState([]);

  /* ---------------- FETCH METRICS ---------------- */
  useEffect(() => {
    let ignore = false;

    const fetchMetrics = async () => {
      try {
        const data = await getMetrics(platform);
        if (!ignore) setMetrics(data);
      } catch (err) {
        if (!ignore)
          console.error("Failed to load metrics:", err.message);
      }
    };

    fetchMetrics();

    return () => {
      ignore = true;
    };
  }, [platform]);

  /* ---------------- FETCH POSTS ---------------- */
  useEffect(() => {
    let ignore = false;

    const fetchPosts = async () => {
      try {
        const data = await getPosts();
        if (!ignore) setPosts(data);
      } catch (err) {
        if (!ignore)
          console.error("Failed to load posts:", err.message);
      }
    };

    fetchPosts();

    return () => {
      ignore = true;
    };
  }, []);

  /* ---------------- OAUTH CONNECT ---------------- */
  const handleConnect = async () => {
    try {
      const data = await connectSocialAccount();
      window.location.href = data.auth_url;
    } catch (err) {
      alert("Failed to connect social account", err.message);
    }
  };

  const latest = metrics[metrics.length - 1];

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="p-6 space-y-6">
        {/* PLATFORM SWITCH */}
        <div className="flex gap-2">
          {["instagram", "facebook"].map((p) => (
            <button
              key={p}
              onClick={() => setPlatform(p)}
              className={`px-4 py-1 rounded ${
                platform === p
                  ? "bg-blue-600 text-white"
                  : "bg-white"
              }`}
            >
              {p}
            </button>
          ))}
        </div>

        {/* CONNECT SOCIAL */}
        <div className="bg-white p-4 rounded shadow">
          <button
            onClick={handleConnect}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Connect Instagram / Facebook
          </button>
        </div>

        {/* KPI CARDS */}
        {latest && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <KpiCard title="Followers" value={latest.followers} />
            <KpiCard title="Likes" value={latest.likes ?? "-"} />
            <KpiCard title="Reach" value={latest.reach ?? "-"} />
          </div>
        )}

        {/* FOLLOWERS CHART */}
        {metrics.length > 0 && (
          <FollowersChart data={metrics} />
        )}

        {/* POSTS LIST */}
        <div className="space-y-2">
          <h3 className="text-lg font-semibold">
            Your Posts
          </h3>
          <PostsList posts={posts} />
        </div>
      </div>
    </div>
  );
}
