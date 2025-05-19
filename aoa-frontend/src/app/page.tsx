"use client";
import { useEffect, useState } from "react";
import Leaderboard, { LeaderboardUser } from "../components/Leaderboard";

export default function Home() {
  // Set default chatId
  const [chatId, setChatId] = useState("870695974476062811");
  const [users, setUsers] = useState<LeaderboardUser[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!chatId) return;
    setLoading(true);
    setError("");
    fetch(`/api/leaderboard?chatId=${chatId}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) setError(data.error);
        else setUsers(data);
      })
      .catch(() => setError("Failed to fetch leaderboard."))
      .finally(() => setLoading(false));
  }, [chatId]);

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex flex-col items-center py-10 text-gray-100">
      <h1 className="text-4xl font-bold mb-6 text-indigo-300">
        AdiPray Leaderboard
      </h1>
      <input
        className="mb-8 px-4 py-2 border border-gray-700 rounded shadow bg-gray-800 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        placeholder="Enter Chat ID"
        value={chatId}
        onChange={(e) => setChatId(e.target.value)}
      />
      {loading ? (
        <div className="text-center text-gray-400">Loading...</div>
      ) : error ? (
        <div className="text-center text-red-400">{error}</div>
      ) : (
        <Leaderboard users={users} />
      )}
      <footer className="mt-10 text-gray-500 text-sm">
        Made with ❤️ for AdiPray
      </footer>
    </main>
  );
}
