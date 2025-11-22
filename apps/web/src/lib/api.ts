export interface TaskResponse {
    task_id: string;
    status: string;
}

const API_BASE_URL = 'http://localhost:8002';

export async function submitTask(description: string): Promise<TaskResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/tasks`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task: description }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
}
