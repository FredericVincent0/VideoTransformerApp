# Video Transformer App 🎥

**Transform long streams into viral masterpieces instantly.**

This application automatically downloads videos from platforms like Twitch, YouTube, and Kick, analyzes them for high-energy moments (using audio levels), and stitches them together into a "Best Of" highlight reel.

![App Screenshot](https://via.placeholder.com/800x450?text=App+Screenshot+Placeholder)

## ✨ Features
*   **Universal Download**: Supports almost any video platform via `yt-dlp`.
*   **Smart Analysis**: Uses `librosa` to detect loud/exciting moments in audio.
*   **Auto-Editing**: Uses `FFmpeg` to cut and merge clips with optimized encoding.
*   **Premium UI**: Modern, dark-themed interface built with Next.js and Tailwind CSS.
*   **Browser Ready**: Outputs web-compatible MP4 (H.264/AAC) with `faststart`.

## 🛠️ Tech Stack
*   **Backend**: Python, FastAPI, Uvicorn
*   **Processing**: FFmpeg, Librosa, NumPy, yt-dlp
*   **Frontend**: Next.js 14, TypeScript, Tailwind CSS v4, Lucide React

## 🚀 Getting Started

### Prerequisites
1.  **Python 3.10+**
2.  **Node.js 18+**
3.  **FFmpeg**: Must be installed and added to your system PATH.

### Installation

#### 1. Backend (Python)
```bash
cd backend
pip install -r requirements.txt
# Start the server
uvicorn main:app --reload
```
*Server runs at: `http://localhost:8000`*

#### 2. Frontend (Next.js)
```bash
cd frontend
npm install
# Start the UI
npm run dev
```
*App runs at: `http://localhost:3000`*

## 📖 How to Use
1.  Launch both Backend and Frontend terminals.
2.  Open `http://localhost:3000`.
3.  Paste a video URL (e.g., a Twitch VOD or YouTube gameplay).
4.  Select your target duration (e.g., 60s).
5.  Click **Generate Highlights**.
6.  Wait for the process to Download -> Analyze -> Edit.
7.  Watch, Download, or Share your result!

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
