"use client";

import { useState, useEffect } from "react";

// Define the shape of a Job
interface Job {
  id: number;
  filename: string;
  status: string;
  created_at: string;
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [uploading, setUploading] = useState(false);

  // Get API URL from environment (available at build time)
  // NEXT_PUBLIC_ prefix makes it available to the browser
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  // Function to fetch the list of jobs from the API
  const fetchJobs = async () => {
    try {
      const res = await fetch(`${API_URL}/jobs/`);
      const data = await res.json();
      // Sort by newest first
      setJobs(data.reverse());
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  };

  // Poll for updates every 2 seconds
  // TODO: Replace polling with WebSockets for real-time updates
  useEffect(() => {
    fetchJobs(); // Fetch immediately
    const interval = setInterval(fetchJobs, 2000);
    return () => clearInterval(interval);
  }, []);

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  // Handle form submission
  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      await fetch(`${API_URL}/upload/`, {
        method: "POST",
        body: formData,
      });
      // Clear file input
      setFile(null);
      // Refresh list immediately
      fetchJobs();
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Upload failed!");
    } finally {
      setUploading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">MarketSight 📈</h1>

        {/* Upload Section */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">New Training Job</h2>
          <form onSubmit={handleUpload} className="flex gap-4 items-center">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
            />
            <button
              type="submit"
              disabled={!file || uploading}
              className={`px-6 py-2 rounded-full font-bold text-white transition-colors
                ${!file || uploading 
                  ? "bg-gray-400 cursor-not-allowed" 
                  : "bg-blue-600 hover:bg-blue-700"}`}
            >
              {uploading ? "Uploading..." : "Start Training"}
            </button>
          </form>
        </div>

        {/* Status List */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="p-6 border-b border-gray-100">
            <h2 className="text-xl font-semibold text-gray-800">Recent Jobs</h2>
          </div>
          <table className="w-full text-left">
            <thead className="bg-gray-50 text-gray-600">
              <tr>
                <th className="p-4">ID</th>
                <th className="p-4">Filename</th>
                <th className="p-4">Status</th>
                <th className="p-4">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {jobs.map((job) => (
                <tr key={job.id} className="hover:bg-gray-50">
                  <td className="p-4 font-mono text-sm text-gray-500">#{job.id}</td>
                  <td className="p-4 font-medium text-gray-900">{job.filename}</td>
                  <td className="p-4">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium
                      ${job.status === "completed" ? "bg-green-100 text-green-700" :
                        job.status === "processing" ? "bg-blue-100 text-blue-700 animate-pulse" :
                        job.status === "failed" ? "bg-red-100 text-red-700" :
                        "bg-yellow-100 text-yellow-800"
                      }`}>
                      {job.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="p-4 text-sm text-gray-500">
                    {new Date(job.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}
              {jobs.length === 0 && (
                <tr>
                  <td colSpan={4} className="p-8 text-center text-gray-500">
                    No jobs yet. Upload a CSV to start!
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
