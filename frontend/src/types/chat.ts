export interface Source {
    document_id: number;
    filename: string;
    chunk_id: number;
    chunk_index: number;
    score: number;
}

export interface ChatResponse {
    answer: string;
    sources: Source[];
}