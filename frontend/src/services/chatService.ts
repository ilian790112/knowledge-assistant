import { api } from "../api/client";

import type { HistoryMessage } from "../types/chatMessage";
import type { ChatResponse } from "../types/chatResponse";

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