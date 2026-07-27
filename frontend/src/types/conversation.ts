import type { ChatMessage } from "./chatMessage";

export interface Conversation {
    id: string;
    title: string;
    createdAt: string;
    messages: ChatMessage[];
}