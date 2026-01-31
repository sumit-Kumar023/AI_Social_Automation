import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { createPost } from "../services/posts";
import React from "react";

export default function Schedule() {
  const [platform, setPlatform] = useState("facebook");
  const [content, setContent] = useState("");
  const [mediaUrl, setMediaUrl] = useState("");
  const [scheduledAt, setScheduledAt] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      // 🔥 CRITICAL FIX: convert local time → UTC
      const localDate = new Date(scheduledAt);
      const utcDate = localDate.toISOString(); // timezone-aware UTC

      await createPost({
        platform,
        content,
        media_url: mediaUrl || null,
        scheduled_at: utcDate,
      });

      navigate("/dashboard");
    } catch (err) {
      setError("Failed to schedule post");
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="p-6 flex justify-center">
        <form
          onSubmit={handleSubmit}
          className="bg-white p-6 rounded shadow w-full max-w-md"
        >
          <h2 className="text-2xl font-bold mb-4">
            Schedule a Post
          </h2>

          {error && (
            <p className="text-red-500 text-sm mb-2">
              {error}
            </p>
          )}

          {/* PLATFORM */}
          <label className="block mb-2 text-sm font-medium">
            Platform
          </label>
          <select
            className="w-full mb-4 p-2 border rounded"
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
          >
            <option value="facebook">Facebook</option>
            <option value="instagram">Instagram</option>
          </select>

          {/* CONTENT */}
          <label className="block mb-2 text-sm font-medium">
            Content
          </label>
          <textarea
            className="w-full mb-4 p-2 border rounded"
            rows={4}
            placeholder="Write your caption..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />

          {/* MEDIA URL */}
          <label className="block mb-2 text-sm font-medium">
            Media URL (optional)
          </label>
          <input
            type="url"
            className="w-full mb-4 p-2 border rounded"
            placeholder="https://example.com/image.jpg"
            value={mediaUrl}
            onChange={(e) => setMediaUrl(e.target.value)}
          />

          {/* SCHEDULE TIME */}
          <label className="block mb-1 text-sm font-medium">
            Schedule Time
          </label>
          <input
            type="datetime-local"
            className="w-full mb-1 p-2 border rounded"
            value={scheduledAt}
            onChange={(e) => setScheduledAt(e.target.value)}
            required
          />
          <p className="text-xs text-gray-500 mb-4">
            Time is in your local timezone
          </p>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded"
          >
            Schedule Post
          </button>
        </form>
      </div>
    </div>
  );
}
