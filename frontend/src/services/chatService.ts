import axios from "axios";

import type { HistoryMessage } from "../types/chatMessage";
import type { ChatResponse } from "../types/chatResponse";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

export async function askQuestion(
    question: string,
    history: HistoryMessage[],
): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>(
        "/chat/",
        {
            question,
            history,
        },
    );

    return response.data;
}