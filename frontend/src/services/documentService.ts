import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
});

export interface DocumentDto {
    id: number;
    filename: string;
    uploaded_at: string;
}

export async function uploadDocument(
    file: File,
) {
    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/documents/upload",
        formData,
        {
            headers: {
                "Content-Type":
                    "multipart/form-data",
            },
        },
    );

    return response.data;
}

export async function getDocuments() {
    const response =
        await api.get<DocumentDto[]>(
            "/documents",
        );

    return response.data;
}

export async function deleteDocument(
    id: number,
) {
    await api.delete(`/documents/${id}`);
}