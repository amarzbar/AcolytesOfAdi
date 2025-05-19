'use client'
import React from "react";

export type LeaderboardUser = {
    user_id: string;
    user_name: string;
    user_display_name: string;
    count: number;
    avatar?: string | null;
};



export default function Leaderboard({ users }: { users: LeaderboardUser[] }) {
    return (
        <div className="w-full max-w-2xl bg-gray-900 rounded-xl shadow-lg p-6">
            <ul>
                {users.map((user, idx) => (
                    <li
                        key={user.user_name}
                        className="flex items-center py-3 border-b border-gray-800 last:border-b-0"
                    >
                        <span className="text-xl font-bold w-8 text-right mr-4 text-indigo-300">{idx + 1}</span>
                        <img
                            src={user.avatar}
                            alt="avatar"
                            className="w-12 h-12 rounded-full border border-gray-700 mr-4 bg-gray-800"
                            onError={e => (e.currentTarget.src = "/default-avatar.png")}
                        />
                        <div>
                            <div className="font-semibold text-lg text-gray-100">{user.user_display_name || user.user_name}</div>
                            <div className="text-gray-400 text-sm">@{user.user_name}</div>
                        </div>
                        <div className="ml-auto text-indigo-300 font-bold text-xl">{user.count}</div>
                    </li>
                ))}
            </ul>
        </div>
    );
}
