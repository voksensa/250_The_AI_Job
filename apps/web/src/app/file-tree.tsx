'use client';

import { useState, useEffect } from 'react';

interface FileTreeProps {
    taskId: string;
}

export function FileTree({ taskId }: FileTreeProps) {
    const [files, setFiles] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!taskId) return;

        const fetchFiles = async () => {
            try {
                const res = await fetch(`http://localhost:8002/api/v1/artifacts/${taskId}/files`);
                if (res.ok) {
                    const data = await res.json();
                    setFiles(data.files);
                }
            } catch (error) {
                console.error('Failed to fetch files:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchFiles();
        // Poll for files every 5 seconds if task is running (optional, but good for UX)
        const interval = setInterval(fetchFiles, 5000);
        return () => clearInterval(interval);
    }, [taskId]);

    if (loading && files.length === 0) {
        return <div className="text-sm text-gray-500">Loading files...</div>;
    }

    if (files.length === 0) {
        return null; // Don't show if no files
    }

    return (
        <div className="mt-4 p-4 border rounded-lg bg-gray-50 dark:bg-gray-900">
            <div className="flex justify-between items-center mb-2">
                <h3 className="font-semibold text-lg">Generated Files</h3>
                <a
                    href={`http://localhost:8002/api/v1/artifacts/${taskId}/download`}
                    className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm font-medium transition-colors"
                    download
                >
                    Download ZIP
                </a>
            </div>
            <ul className="space-y-1 font-mono text-sm max-h-60 overflow-y-auto">
                {files.map(file => (
                    <li key={file} className="flex items-center text-gray-700 dark:text-gray-300">
                        <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        {file}
                    </li>
                ))}
            </ul>
        </div>
    );
}
