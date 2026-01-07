"use client";

import { Activity, CheckCircle, Loader2, AlertCircle } from "lucide-react";
import { useEffect, useState } from "react";

interface StatusProps {
    status: string;
    progress: number;
    message: string;
}

export default function ProcessingStatus({ status, progress, message }: StatusProps) {
    return (
        <div className="glass-panel p-8 w-full max-w-2xl mx-auto mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                    {status === 'completed' ? (
                        <CheckCircle className="w-6 h-6 text-green-500" />
                    ) : status === 'failed' ? (
                        <AlertCircle className="w-6 h-6 text-red-500" />
                    ) : (
                        <Loader2 className="w-6 h-6 text-violet-500 animate-spin" />
                    )}
                    <h3 className="text-xl font-bold text-white capitalize">{status}</h3>
                </div>
                <span className="text-zinc-500 font-mono">{progress}%</span>
            </div>

            <div className="w-full bg-zinc-800 rounded-full h-2 mb-4 overflow-hidden">
                <div
                    className="bg-violet-600 h-2 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${progress}%` }}
                ></div>
            </div>

            <p className="text-zinc-400 text-sm flex items-center space-x-2">
                <Activity className="w-4 h-4" />
                <span>{message}</span>
            </p>
        </div>
    );
}
