import {
    forwardRef,
    useEffect,
    useImperativeHandle,
    useRef,
    useState,
} from "react";

import type {
    ChangeEvent,
    DragEvent,
} from "react";

import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Alert,
    Box,
    Button,
    IconButton,
    LinearProgress,
    List,
    ListItem,
    ListItemText,
    Paper,
    Tooltip,
    Typography,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import DeleteIcon from "@mui/icons-material/Delete";

import {
    deleteDocument,
    getDocuments,
    uploadDocument,
    type DocumentDto,
} from "../services/documentService";

export interface KnowledgeBasePanelHandle {
    refresh: () => void;
}

interface Props {
    onUploadSuccess?: () => void;
}

const KnowledgeBasePanel = forwardRef<
    KnowledgeBasePanelHandle,
    Props
>(({ onUploadSuccess }, ref) => {
    const inputRef =
        useRef<HTMLInputElement>(null);

    const [documents, setDocuments] =
        useState<DocumentDto[]>([]);

    const [expanded, setExpanded] =
        useState(false);

    const [uploading, setUploading] =
        useState(false);

    const [message, setMessage] =
        useState("");

    const [isError, setIsError] =
        useState(false);

    const [dragging, setDragging] =
        useState(false);

    async function loadDocuments() {
        try {
            const data =
                await getDocuments();

            setDocuments(data);
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(() => {
        loadDocuments();
    }, []);

    useImperativeHandle(ref, () => ({
        refresh: loadDocuments,
    }));

    async function upload(file: File) {
        try {
            setUploading(true);
            setMessage("");
            setIsError(false);

            const response =
                await uploadDocument(file);

            setMessage(
                response.message ??
                    "Document uploaded successfully.",
            );

            await loadDocuments();

            setExpanded(false);

            onUploadSuccess?.();

            if (inputRef.current) {
                inputRef.current.value = "";
            }
        } catch (error) {
            console.error(error);

            setIsError(true);
            setMessage(
                "Upload failed.",
            );
        } finally {
            setUploading(false);
        }
    }

    function handleChange(
        e: ChangeEvent<HTMLInputElement>,
    ) {
        const file =
            e.target.files?.[0];

        if (file) {
            upload(file);
        }
    }

    function handleDrop(
        e: DragEvent<HTMLDivElement>,
    ) {
        e.preventDefault();

        setDragging(false);

        const file =
            e.dataTransfer.files?.[0];

        if (!file) return;

        if (
            file.type !==
            "application/pdf"
        ) {
            setIsError(true);
            setMessage(
                "Only PDF files are supported.",
            );

            return;
        }

        upload(file);
    }

    async function handleDelete(
        id: number,
    ) {
        if (
            !window.confirm(
                "Delete this document?",
            )
        ) {
            return;
        }

        await deleteDocument(id);

        loadDocuments();
    }

    return (
        <Accordion
            expanded={expanded}
            onChange={(_, value) =>
                setExpanded(value)
            }
            sx={{
                mb: 2,
                borderRadius: 3,
                "&:before": {
                    display: "none",
                },
            }}
        >
            <AccordionSummary
                expandIcon={
                    <ExpandMoreIcon />
                }
            >
                <Typography
                    fontWeight={700}
                >
                    Knowledge Base (
                    {documents.length}{" "}
                    documents)
                </Typography>
            </AccordionSummary>

            <AccordionDetails>

                <input
                    hidden
                    ref={inputRef}
                    type="file"
                    accept=".pdf"
                    onChange={
                        handleChange
                    }
                />

                <Paper
                    variant="outlined"
                    onDragOver={(e) => {
                        e.preventDefault();
                        setDragging(
                            true,
                        );
                    }}
                    onDragLeave={() =>
                        setDragging(
                            false,
                        )
                    }
                    onDrop={handleDrop}
                    sx={{
                        p: 3,
                        mb: 3,
                        textAlign:
                            "center",
                        borderStyle:
                            "dashed",
                        bgcolor:
                            dragging
                                ? "action.hover"
                                : "background.default",
                        transition:
                            "0.2s",
                    }}
                >
                    <DescriptionOutlinedIcon
                        sx={{
                            fontSize: 40,
                            mb: 1,
                        }}
                    />

                    <Typography
                        fontWeight={600}
                    >
                        Drag a PDF here
                    </Typography>

                    <Typography
                        color="text.secondary"
                        sx={{
                            mb: 2,
                        }}
                    >
                        or browse
                    </Typography>

                    <Button
                        variant="contained"
                        startIcon={
                            <CloudUploadIcon />
                        }
                        onClick={() =>
                            inputRef.current?.click()
                        }
                        disabled={
                            uploading
                        }
                    >
                        Upload PDF
                    </Button>
                </Paper>

                {uploading && (
                    <LinearProgress
                        sx={{
                            mb: 2,
                        }}
                    />
                )}

                {message && (
                    <Alert
                        severity={
                            isError
                                ? "error"
                                : "success"
                        }
                        sx={{
                            mb: 2,
                        }}
                    >
                        {message}
                    </Alert>
                )}

                <List
                    sx={{
                        maxHeight: 250,
                        overflowY:
                            "auto",
                    }}
                >
                    {documents.map(
                        (
                            document,
                        ) => (
                            <ListItem
                                key={
                                    document.id
                                }
                                divider
                                secondaryAction={
                                    <Tooltip title="Delete">
                                        <IconButton
                                            color="error"
                                            onClick={() =>
                                                handleDelete(
                                                    document.id,
                                                )
                                            }
                                        >
                                            <DeleteIcon />
                                        </IconButton>
                                    </Tooltip>
                                }
                            >
                                <ListItemText
                                    primary={
                                        document.filename
                                    }
                                    secondary={new Date(
                                        document.uploaded_at,
                                    ).toLocaleString()}
                                />
                            </ListItem>
                        ),
                    )}
                </List>

            </AccordionDetails>
        </Accordion>
    );
});

KnowledgeBasePanel.displayName =
    "KnowledgeBasePanel";

export default KnowledgeBasePanel;