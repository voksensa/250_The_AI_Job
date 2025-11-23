import React, { useState, useEffect } from 'react';

interface TestStep {
    action: string;
    url?: string;
    selector?: string;
    value?: string;
    passed?: boolean;
}

interface TestPlan {
    steps: TestStep[];
}

interface TestResult {
    step: number;
    passed: boolean;
}

interface QAResultsProps {
    events: any[];
}

export default function QAResults({ events }: QAResultsProps) {
    const [testPlan, setTestPlan] = useState<TestPlan | null>(null);
    const [stepResults, setStepResults] = useState<TestResult[]>([]);
    const [evaluation, setEvaluation] = useState<{ passed: boolean; report: string } | null>(null);
    const [screenshots, setScreenshots] = useState<string[]>([]);

    useEffect(() => {
        // Process events to build state
        events.forEach(event => {
            const data = event.data;
            if (!data) return;

            if (data.status === 'test_planned' && data.test_plan) {
                setTestPlan(data.test_plan);
            }

            if (data.status === 'test_step_complete') {
                setStepResults(prev => {
                    // Avoid duplicates
                    if (prev.some(r => r.step === data.step)) return prev;
                    return [...prev, { step: data.step, passed: data.passed }];
                });
            }

            if (data.status === 'test_evaluation_complete') {
                setEvaluation({ passed: data.passed, report: data.report });
            }

            // Screenshots might come in step results or separate events
            // Based on backend implementation, screenshots are returned in the final result
            // But we might want to show them as they happen if we streamed them.
            // Current backend implementation returns them at the end of executor node.
            if (data.executor && data.executor.screenshots) {
                setScreenshots(data.executor.screenshots);
            }
            // Also check for direct screenshot events if we added them (we didn't explicitly, but good to have)
        });
    }, [events]);

    if (!testPlan && !evaluation) return null;

    return (
        <section className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg animate-fade-in mt-6">
            <h2 className="text-xl font-semibold mb-4 text-purple-400">Synthetic QA Results</h2>

            {/* Test Plan & Progress */}
            {testPlan && (
                <div className="mb-6">
                    <h3 className="text-sm font-medium text-gray-400 mb-2">Test Plan Execution</h3>
                    <div className="space-y-2">
                        {testPlan.steps.map((step, index) => {
                            const result = stepResults.find(r => r.step === index + 1);
                            const statusIcon = result
                                ? (result.passed ? '✅' : '❌')
                                : (index === stepResults.length ? '⏳' : '○');

                            return (
                                <div key={index} className="flex items-center justify-between bg-gray-900 p-2 rounded border border-gray-700">
                                    <div className="flex items-center gap-2">
                                        <span className="text-lg">{statusIcon}</span>
                                        <span className="text-gray-300 font-mono text-sm">
                                            {step.action.toUpperCase()}
                                            {step.selector ? ` ${step.selector}` : ''}
                                            {step.url ? ` ${step.url}` : ''}
                                        </span>
                                    </div>
                                    {result && (
                                        <span className={`text-xs px-2 py-1 rounded ${result.passed ? 'bg-green-900/50 text-green-300' : 'bg-red-900/50 text-red-300'}`}>
                                            {result.passed ? 'PASS' : 'FAIL'}
                                        </span>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Screenshots */}
            {screenshots.length > 0 && (
                <div className="mb-6">
                    <h3 className="text-sm font-medium text-gray-400 mb-2">Evidence</h3>
                    <div className="grid grid-cols-2 gap-4">
                        {screenshots.map((src, i) => {
                            // Extract filename from path (e.g. /app/screenshots/step_1.png -> step_1.png)
                            const filename = src.split('/').pop();
                            const imageUrl = `http://localhost:8002/api/v1/screenshots/${filename}`;

                            return (
                                <div key={i} className="relative group">
                                    <div className="bg-gray-950 border border-gray-700 rounded p-2">
                                        <img
                                            src={imageUrl}
                                            alt={`Screenshot ${i + 1}`}
                                            className="w-full rounded border border-gray-700 mb-2"
                                            onError={(e) => {
                                                (e.target as HTMLImageElement).style.display = 'none';
                                                (e.target as HTMLImageElement).nextElementSibling?.classList.remove('hidden');
                                            }}
                                        />
                                        <div className="hidden text-xs text-red-400 p-2">
                                            Failed to load: {filename}
                                        </div>
                                        <div className="text-xs text-gray-500 break-all truncate">
                                            {filename}
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Final Evaluation */}
            {evaluation && (
                <div className={`p-4 rounded border ${evaluation.passed ? 'bg-green-900/20 border-green-800' : 'bg-red-900/20 border-red-800'}`}>
                    <div className="flex items-center gap-2 mb-2">
                        <span className="text-2xl">{evaluation.passed ? '🎉' : '⚠️'}</span>
                        <h3 className={`font-bold ${evaluation.passed ? 'text-green-400' : 'text-red-400'}`}>
                            {evaluation.passed ? 'QA Passed' : 'QA Failed'}
                        </h3>
                    </div>
                    <p className="text-gray-300 text-sm whitespace-pre-wrap">{evaluation.report}</p>
                </div>
            )}
        </section>
    );
}
