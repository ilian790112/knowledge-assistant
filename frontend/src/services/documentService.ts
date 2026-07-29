import axios from "axios";

const API_URL =
    import.meta.env.VITE_API_URL ??
    "http://localhost:8000";

const api = axios.create({
    baseURL: API_URL.replace(/\/$/, ""),
});

export interface DocumentDto {
    id: number;
    filename: string;
    uploaded_at: string;
}

export async function uploadDocument(file: File) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post(
        "/documents/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        },
    );

    return response.data;
}

export async function getDocuments() {
    const response = await api.get<DocumentDto[]>(
        "/documents",
    );

    return response.data;
}

export async function deleteDocument(id: number) {
    await api.delete(`/documents/${id}`);
}