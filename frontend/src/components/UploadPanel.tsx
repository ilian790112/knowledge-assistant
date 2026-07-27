import { useRef, useState } from "react";
import type {
    ChangeEvent,
    DragEvent,
} from "react";

import {
    Alert,
    Box,
    Button,
    LinearProgress,
    Paper,
    Typography,
} from "@mui/material";

import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";

import { uploadDocument } from "../services/documentService";

interface UploadPanelProps {
    onUploadSuccess?: () => void;
}

function UploadPanel({
    onUploadSuccess,
}: UploadPanelProps) {
    const inputRef = useRef<HTMLInputElement>(null);

    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");
    const [isDragging, setIsDragging] = useState(false);
    const [isError, setIsError] = useState(false);

    async function uploadFile(file: File) {
        try {
            setUploading(true);
            setMessage("");
            setIsError(false);

            const response = await uploadDocument(file);

            setMessage(
                response.message ??
                    `"${file.name}" uploaded successfully.`,
            );

            onUploadSuccess?.();

            if (inputRef.current) {
                inputRef.current.value = "";
            }
        } catch (error) {
            console.error(error);

            setIsError(true);
            setMessage("Failed to upload the document.");
        } finally {
            setUploading(false);
        }
    }

    function handleUpload(
        event: ChangeEvent<HTMLInputElement>,
    ) {
        const file = event.target.files?.[0];

        if (!file) {
            return;
        }

        uploadFile(file);
    }

    function handleDrop(
        event: DragEvent<HTMLDivElement>,
    ) {
        event.preventDefault();
        setIsDragging(false);

        const file = event.dataTransfer.files?.[0];

        if (!file) {
            return;
        }

        if (file.type !== "application/pdf") {
            setIsError(true);
            setMessage("Only PDF files are supported.");
            return;
        }

        uploadFile(file);
    }

    return (
    <Paper
        sx={{
            p: 2.5,
            mb: 2,
        }}
    >
        <Typography
            variant="h6"
            fontWeight={700}
            gutterBottom
        >
            Upload Documents
        </Typography>

        <input
            ref={inputRef}
            hidden
            type="file"
            accept=".pdf"
            onChange={handleUpload}
        />

        <Box
            onDragOver={(e) => {
                e.preventDefault();
                setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            sx={{
                border: "2px dashed",
                borderColor: isDragging
                    ? "primary.main"
                    : "divider",
                borderRadius: 3,
                py: 3,
                px: 3,
                textAlign: "center",
                bgcolor: isDragging
                    ? "action.hover"
                    : "background.default",
                transition: "all .2s ease",
            }}
        >
            <DescriptionOutlinedIcon
                sx={{
                    fontSize: 36,
                    color: "text.secondary",
                    mb: 1,
                }}
            />

            <Typography
                variant="subtitle1"
                fontWeight={600}
            >
                Drag & drop a PDF here
            </Typography>

            <Typography
                variant="body2"
                color="text.secondary"
                sx={{
                    mb: 2,
                }}
            >
                or browse from your computer
            </Typography>

            <Button
                variant="contained"
                startIcon={<CloudUploadIcon />}
                disabled={uploading}
                onClick={() =>
                    inputRef.current?.click()
                }
            >
                Select PDF
            </Button>
        </Box>

        {uploading && (
            <Box sx={{ mt: 2 }}>
                <LinearProgress />
                <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mt: 1 }}
                >
                    Uploading document...
                </Typography>
            </Box>
        )}

        {message && (
            <Alert
                severity={
                    isError
                        ? "error"
                        : "success"
                }
                sx={{ mt: 2 }}
            >
                {message}
            </Alert>
        )}
    </Paper>
);
}

export default UploadPanel;