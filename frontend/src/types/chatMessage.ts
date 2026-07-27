import type { ChatResponse } from "./chatResponse";

export interface ChatMessage {
    question: string;
    response: ChatResponse;
}

export interface HistoryMessage {
    role: "user" | "assistant";
    content: string;
}