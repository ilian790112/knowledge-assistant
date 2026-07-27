import type { Source } from "./source";

export interface ChatResponse {
    answer: string;
    sources: Source[];
}