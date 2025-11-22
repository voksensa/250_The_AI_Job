'use client';

import { useState, useEffect, useRef } from 'react';
import { submitTask } from '../lib/api';

interface EventLog {
  timestamp: string;
  data: any;
}

export default function Home() {
  const [task, setTask] = useState('');
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('idle');
  const [events, setEvents] = useState<EventLog[]>([]);
  const [result, setResult] = useState<string | null>(null);

  const [error, setError] = useState<string | null>(null);

  // Production Toggle State
  const [lintStatus, setLintStatus] = useState<string | null>(null);
  const [testStatus, setTestStatus] = useState<string | null>(null);
  const [productionReady, setProductionReady] = useState(false);
  const [productionEnabled, setProductionEnabled] = useState(false);
  const [deploymentUrl, setDeploymentUrl] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);

  // MCP Query 3: WebSocket in React/Next.js
  useEffect(() => {
    if (!taskId) return;

    const wsUrl = `ws://localhost:8002/api/v1/tasks/${taskId}/stream`;
    console.log(`Connecting to WebSocket: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
      // Send initial message to start/resume if needed, or just wait for stream
      // Based on routes.py, sending the task description might trigger the run if not started
      // But for now, we assume the POST /tasks started it, and we just listen.
      // However, routes.py logic suggests it waits for a message. 
      // Let's send an empty message or the task again to trigger the stream if needed.
      ws.send(JSON.stringify({ task: task }));
    };

    ws.onmessage = (event) => {
      console.log('WebSocket message:', event.data);
      try {
        // The backend currently sends str(chunk), which might be single quoted python dict string
        // We might need to handle that if it's not valid JSON.
        // Ideally backend sends valid JSON. Assuming backend sends valid JSON for now.
        // If backend sends python string representation, we might see errors here.
        // We will fix backend to send JSON in the next step if this fails.

        // For now, let's try to parse, and if it fails, just log the raw text
        let parsedData;
        try {
          parsedData = JSON.parse(event.data);
        } catch {
          parsedData = event.data;
        }

        setEvents((prev) => [
          ...prev,
          { timestamp: new Date().toISOString(), data: parsedData },
        ]);

        // Check for result in the data
        if (parsedData && typeof parsedData === 'object') {
          // Gate Status Updates
          if (parsedData.lint_status) setLintStatus(parsedData.lint_status);
          if (parsedData.test_status) setTestStatus(parsedData.test_status);

          // Production Readiness
          if (parsedData.production_ready) {
            setProductionReady(true);
          }

          // Production Approval/Deployment
          if (parsedData.production_approved) {
            setProductionEnabled(true);
          }
          if (parsedData.deployment_url) {
            setDeploymentUrl(parsedData.deployment_url);
            setStatus('deployed');
          }

          // Adjust based on actual LangGraph event structure
          if (parsedData.result) {
            setResult(parsedData.result);
            if (!parsedData.deployment_url) setStatus('completed');
          }
          if (parsedData.executor && parsedData.executor.result) {
            setResult(parsedData.executor.result);
            if (!parsedData.deployment_url) setStatus('completed');
          }
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };

    ws.onerror = (event) => {
      console.error('WebSocket error:', event);
      setError('WebSocket connection error');
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [taskId, task]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!task.trim()) return;

    setStatus('submitting');
    setError(null);
    setEvents([]);
    setResult(null);

    setTaskId(null);

    // Reset Toggle State
    setLintStatus(null);
    setTestStatus(null);
    setProductionReady(false);
    setProductionEnabled(false);
    setDeploymentUrl(null);

    try {
      // MCP Query 1: Client-side form submission
      const response = await submitTask(task);
      setTaskId(response.task_id);
      setStatus('running');
    } catch (err: any) {
      console.error('Error submitting task:', err);
      setError(err.message || 'Failed to submit task');
      setStatus('error');
    }
  };

  const handleToggle = () => {
    if (!wsRef.current || !productionReady) return;
    console.log('Approving production deployment...');
    wsRef.current.send(JSON.stringify({ production_approved: true }));
    setProductionEnabled(true); // Optimistic update
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8 font-sans">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8 border-b border-gray-800 pb-4">
          <h1 className="text-3xl font-bold text-white mb-2">Your First Engineer</h1>
          <p className="text-gray-400">Production Toggle Foundation (Phase 1 MVP)</p>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Input & Status */}
          <div className="space-y-6">
            <section className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg">
              <h2 className="text-xl font-semibold mb-4 text-blue-400">New Task</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="task" className="block text-sm font-medium text-gray-300 mb-1">
                    Describe your app idea
                  </label>
                  <textarea
                    id="task"
                    value={task}
                    onChange={(e) => setTask(e.target.value)}
                    className="w-full h-32 bg-gray-900 border border-gray-600 rounded-md p-3 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="e.g., Create a hello world function in Python..."
                    disabled={status === 'submitting' || status === 'running'}
                  />
                </div>
                <button
                  type="submit"
                  disabled={status === 'submitting' || status === 'running' || !task.trim()}
                  className={`w-full py-2 px-4 rounded-md font-medium transition-colors ${status === 'submitting' || status === 'running'
                    ? 'bg-gray-600 cursor-not-allowed text-gray-400'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                    }`}
                >
                  {status === 'submitting' ? 'Submitting...' : status === 'running' ? 'Processing...' : 'Start Building'}
                </button>
              </form>
            </section>

            {taskId && (
              <section className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg animate-fade-in">
                <h2 className="text-xl font-semibold mb-4 text-purple-400">Status</h2>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Task ID:</span>
                    <span className="font-mono text-sm text-gray-200">{taskId}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">State:</span>
                    <span className={`font-medium ${status === 'completed' ? 'text-green-400' :
                      status === 'error' ? 'text-red-400' :
                        'text-yellow-400'
                      }`}>
                      {status.toUpperCase()}
                    </span>
                  </div>
                </div>
              </section>
            )}



            {/* Production Toggle Switch */}
            {taskId && (
              <section className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg animate-fade-in">
                <h2 className="text-xl font-semibold mb-4 text-green-400">Production Mode</h2>

                <div className="flex items-center justify-between mb-4">
                  <div className="text-sm text-gray-300">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={lintStatus === 'pass' ? 'text-green-400' : 'text-gray-500'}>
                        {lintStatus === 'pass' ? '✓' : '○'} Lint Check
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={testStatus === 'pass' ? 'text-green-400' : 'text-gray-500'}>
                        {testStatus === 'pass' ? '✓' : '○'} Unit Tests
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={handleToggle}
                    disabled={!productionReady || productionEnabled}
                    className={`relative inline-flex h-8 w-14 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-gray-800 ${productionEnabled ? 'bg-blue-600' : productionReady ? 'bg-green-600' : 'bg-gray-600 cursor-not-allowed'
                      }`}
                  >
                    <span
                      className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${productionEnabled ? 'translate-x-7' : 'translate-x-1'
                        }`}
                    />
                  </button>
                </div>

                <div className="text-center">
                  {productionEnabled ? (
                    deploymentUrl ? (
                      <div className="bg-blue-900/30 border border-blue-700 rounded p-2">
                        <p className="text-blue-300 text-sm font-semibold">Production: ENABLED</p>
                        <a href={deploymentUrl} target="_blank" rel="noopener noreferrer" className="text-blue-400 text-xs hover:underline">
                          {deploymentUrl}
                        </a>
                      </div>
                    ) : (
                      <p className="text-blue-300 text-sm animate-pulse">Deploying to production...</p>
                    )
                  ) : productionReady ? (
                    <p className="text-green-400 text-sm">Gates Passed. Ready to Deploy.</p>
                  ) : (
                    <p className="text-gray-500 text-sm">Waiting for quality gates...</p>
                  )}
                </div>
              </section>
            )}

            {error && (
              <div className="bg-red-900/50 border border-red-700 text-red-200 p-4 rounded-md">
                {error}
              </div>
            )}
          </div>

          {/* Right Column: Events & Result */}
          <div className="space-y-6">
            {taskId && (
              <section className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg flex flex-col h-[600px]">
                <h2 className="text-xl font-semibold mb-4 text-green-400">Live Build Story</h2>

                <div className="flex-1 overflow-y-auto bg-gray-950 rounded-md p-4 font-mono text-sm space-y-2 border border-gray-800">
                  {events.length === 0 && (
                    <p className="text-gray-500 italic">Waiting for events...</p>
                  )}
                  {events.map((event, index) => (
                    <div key={index} className="border-l-2 border-blue-500 pl-3 py-1">
                      <span className="text-gray-500 text-xs block mb-1">{event.timestamp}</span>
                      <pre className="whitespace-pre-wrap text-gray-300 overflow-x-auto">
                        {typeof event.data === 'string' ? event.data : JSON.stringify(event.data, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {result && (
              <section className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg">
                <h2 className="text-xl font-semibold mb-4 text-yellow-400">Final Result</h2>
                <div className="bg-gray-950 rounded-md p-4 border border-gray-800">
                  <pre className="whitespace-pre-wrap text-gray-200 font-mono text-sm overflow-x-auto">
                    {result}
                  </pre>
                </div>
              </section>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
