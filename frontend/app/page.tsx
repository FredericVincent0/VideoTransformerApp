"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import VideoSubmission from "@/components/VideoSubmission";
import ProcessingStatus from "@/components/ProcessingStatus";
import ResultPlayer from "@/components/ResultPlayer";

// Configure axios base URL - assumption: backend runs on localhost:8000
const API_BASE_URL = "http://localhost:8000/api";

export default function Home() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("idle"); // idle, queued, downloading, analyzing, editing, completed, failed
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("");
  const [resultPath, setResultPath] = useState<string | null>(null);

  const startProcessing = async (url: string, duration: number) => {
    try {
      setStatus("queued");
      setProgress(0);
      setMessage("Starting job...");

      const response = await axios.post(`${API_BASE_URL}/process`, {
        url,
        target_duration: duration,
        style: "energetic"
      });

      setJobId(response.data.job_id);

    } catch (error) {
      console.error(error);
      setStatus("failed");
      setMessage("Failed to start processing. Is backend running?");
    }
  };

  useEffect(() => {
    if (!jobId || status === "completed" || status === "failed") return;

    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/status/${jobId}`);
        const data = response.data;

        setStatus(data.status);
        setProgress(data.progress);
        setMessage(data.message);

        if (data.status === "completed") {
          // For now, we assume the backend saves it in a way we can access, 
          // but normally we'd need a file serving endpoint.
          // Since we don't have a file server in the backend code yet to serve 'output',
          // we might need to add `StaticFiles` to FastAPI.
          // For now, let's assume we can add that or just use a placeholder.
          // Add string query param to bust browser cache
          setResultPath("http://localhost:8000/static/" + data.result_path.split(/[\\/]/).pop() + "?t=" + Date.now());
        }

      } catch (error) {
        console.error("Polling error", error);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId, status]);

  return (
    <main className="min-h-screen p-8 lg:p-24 relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-violet-600/20 rounded-full blur-[120px] animate-pulse-glow"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[600px] h-[600px] bg-rose-600/10 rounded-full blur-[120px] animate-pulse-glow" style={{ animationDelay: '1.5s' }}></div>
      </div>

      <div className="max-w-5xl mx-auto space-y-12">
        <header className="text-center space-y-4">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-gradient-to-br from-white via-white to-zinc-500 bg-clip-text text-transparent pb-2">
            Antigravity <span className="text-violet-500">Studios</span>
          </h1>
          <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
            Transform long streams into viral masterpieces instantly.
          </p>
        </header>

        <section>
          <VideoSubmission onSubmit={startProcessing} isLoading={status !== 'idle' && status !== 'completed' && status !== 'failed'} />
        </section>

        {(status !== 'idle') && (
          <section>
            <ProcessingStatus status={status} progress={progress} message={message} />
          </section>
        )}

        {status === 'completed' && (
          <section>
            <ResultPlayer videoUrl={resultPath} />
          </section>
        )}
      </div>
    </main>
  );
}
