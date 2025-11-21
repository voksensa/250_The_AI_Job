"use client";

import { useState } from "react";
import { submitTask, TaskResponse } from "@/lib/api";

export default function Home() {
  const [description, setDescription] = useState("");
  const [result, setResult] = useState<TaskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await submitTask(description);
      setResult(data);
    } catch (err) {
      setError("Failed to submit task");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-white dark:bg-zinc-900">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold mb-8 text-center w-full dark:text-white">
          Production Toggle MVP
        </h1>
      </div>

      <div className="w-full max-w-md p-6 bg-zinc-100 dark:bg-zinc-800 rounded-lg shadow-md">
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300">
            Task Description
            <textarea
              className="mt-1 block w-full rounded-md border-zinc-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-zinc-700 dark:border-zinc-600 dark:text-white p-2"
              rows={4}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter your task here..."
              required
            />
          </label>

          <button
            type="submit"
            disabled={loading}
            className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
          >
            {loading ? "Submitting..." : "Submit Task"}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md text-sm">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-md border border-green-200 dark:border-green-800">
            <h3 className="text-lg font-medium text-green-800 dark:text-green-200">
              Task Submitted!
            </h3>
            <div className="mt-2 text-sm text-green-700 dark:text-green-300">
              <p>Task ID: <span className="font-mono">{result.task_id}</span></p>
              <p>Status: <span className="font-mono">{result.status}</span></p>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
