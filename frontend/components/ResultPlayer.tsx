"use client";

import { Play, Download, Share2 } from "lucide-react";

interface ResultPlayerProps {
    videoUrl: string | null;
}

export default function ResultPlayer({ videoUrl }: ResultPlayerProps) {
    if (!videoUrl) return null;

    const handleDownload = () => {
        if (!videoUrl) return;
        const link = document.createElement('a');
        link.href = videoUrl;
        link.download = 'highlight_reel.mp4';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const handleShare = () => {
        if (!videoUrl) return;
        navigator.clipboard.writeText(window.location.host + videoUrl).then(() => {
            alert("Video URL copied to clipboard!");
        });
    };

    return (
        <div className="glass-panel p-2 w-full max-w-4xl mx-auto mt-8 overflow-hidden animate-in zoom-in duration-500">
            <div className="relative aspect-video bg-black rounded-xl overflow-hidden group">
                <video
                    src={videoUrl}
                    controls
                    className="w-full h-full object-contain"
                />
            </div>

            <div className="p-6 flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-bold text-white">Your Highlight Reel</h3>
                    <p className="text-zinc-400 text-sm">Ready to share!</p>
                </div>
                <div className="flex space-x-3">
                    <button
                        onClick={handleDownload}
                        className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded-lg text-white text-sm font-medium transition-colors flex items-center space-x-2"
                    >
                        <Download className="w-4 h-4" />
                        <span>Download</span>
                    </button>
                    <button
                        onClick={handleShare}
                        className="px-4 py-2 bg-violet-600/20 hover:bg-violet-600/30 text-violet-300 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2"
                    >
                        <Share2 className="w-4 h-4" />
                        <span>Share</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
