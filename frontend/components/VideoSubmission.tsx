"use client";

import { useState } from "react";
import { Copy, FileVideo, Sparkles } from "lucide-react";

interface VideoSubmissionProps {
    onSubmit: (url: string, duration: number) => void;
    isLoading: boolean;
}

export default function VideoSubmission({ onSubmit, isLoading }: VideoSubmissionProps) {
    const [url, setUrl] = useState("");
    const [duration, setDuration] = useState(60);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (url) onSubmit(url, duration);
    };

    return (
        <div className="glass-panel p-8 w-full max-w-2xl mx-auto transform transition-all hover:scale-[1.01]">
            <div className="flex items-center space-x-3 mb-6">
                <div className="p-3 bg-violet-500/10 rounded-lg">
                    <FileVideo className="w-6 h-6 text-violet-400" />
                </div>
                <h2 className="text-2xl font-bold bg-gradient-to-r from-white to-zinc-400 bg-clip-text text-transparent">
                    Create Highlight Reel
                </h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                    <label className="text-sm font-medium text-zinc-400 ml-1">Video URL (Twitch, YouTube, Kick)</label>
                    <div className="relative">
                        <input
                            type="text"
                            placeholder="https://www.twitch.tv/videos/..."
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            className="input-field pl-12"
                            disabled={isLoading}
                        />
                        <Copy className="absolute left-4 top-3.5 w-5 h-5 text-zinc-500" />
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="text-sm font-medium text-zinc-400 ml-1">Target Duration (Seconds)</label>
                    <input
                        type="range"
                        min="10"
                        max="300"
                        step="10"
                        value={duration}
                        onChange={(e) => setDuration(Number(e.target.value))}
                        className="w-full h-2 bg-zinc-700 rounded-lg appearance-none cursor-pointer accent-violet-500"
                    />
                    <div className="flex justify-between text-xs text-zinc-500 px-1">
                        <span>10s</span>
                        <span className="text-violet-400 font-bold">{duration}s</span>
                        <span>5m</span>
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={isLoading || !url}
                    className={`btn-primary w-full flex items-center justify-center space-x-2 ${isLoading ? "opacity-50 cursor-not-allowed" : ""
                        }`}
                >
                    {isLoading ? (
                        <span className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></span>
                    ) : (
                        <>
                            <Sparkles className="w-5 h-5" />
                            <span>Generate Highlights</span>
                        </>
                    )}
                </button>
            </form>
        </div>
    );
}
