const API_BASE_URL = 'http://localhost:8002/api';

export interface TaskResponse {
    task_id: string;
    status: string;
}

export async function submitTask(description: string): Promise<TaskResponse> {
    const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description }),
    });

    if (!response.ok) {
        throw new Error('Failed to submit task');
    }

    return response.json();
}

export async function getTaskStatus(taskId: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`);
    if (!response.ok) {
        throw new Error('Failed to get task status');
    }
    return response.json();
}
