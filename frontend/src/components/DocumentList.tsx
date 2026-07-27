import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Box,
    IconButton,
    List,
    ListItem,
    ListItemText,
    Tooltip,
    Typography,
} from "@mui/material";

import DeleteIcon from "@mui/icons-material/Delete";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

import {
    forwardRef,
    useEffect,
    useImperativeHandle,
    useState,
} from "react";

import {
    deleteDocument,
    getDocuments,
    type DocumentDto,
} from "../services/documentService";

export interface DocumentListHandle {
    refresh: () => void;
}

const DocumentList = forwardRef<DocumentListHandle>((_, ref) => {
    const [documents, setDocuments] = useState<DocumentDto[]>([]);

    async function loadDocuments() {
        try {
            const data = await getDocuments();
            setDocuments(data);
        } catch (error) {
            console.error(error);
        }
    }

    async function handleDelete(id: number) {
        if (
            !window.confirm(
                "Delete this document? This action cannot be undone.",
            )
        ) {
            return;
        }

        try {
            await deleteDocument(id);
            await loadDocuments();
        } catch (error) {
            console.error(error);
        }
    }

    useImperativeHandle(ref, () => ({
        refresh: loadDocuments,
    }));

    useEffect(() => {
        loadDocuments();
    }, []);

    return (
        <Accordion
            defaultExpanded={false}
            sx={{
                mb: 3,
                borderRadius: 3,
                overflow: "hidden",
                "&:before": {
                    display: "none",
                },
            }}
        >
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography
                    variant="h6"
                    sx={{
                        fontWeight: 700,
                    }}
                >
                    Uploaded Documents ({documents.length})
                </Typography>
            </AccordionSummary>

            <AccordionDetails>
                {documents.length === 0 ? (
                    <Box
                        sx={{
                            py: 5,
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            textAlign: "center",
                        }}
                    >
                        <Typography
                            variant="h2"
                            sx={{
                                mb: 2,
                            }}
                        >
                            📚
                        </Typography>

                        <Typography
                            variant="h6"
                            sx={{
                                fontWeight: 600,
                            }}
                        >
                            No documents uploaded
                        </Typography>

                        <Typography
                            color="text.secondary"
                            sx={{
                                mt: 1,
                                maxWidth: 400,
                            }}
                        >
                            Upload your first PDF to start building your AI
                            knowledge base.
                        </Typography>
                    </Box>
                ) : (
                    <Box
                        sx={{
                            maxHeight: 300,
                            overflowY: "auto",
                        }}
                    >
                        <List disablePadding>
                            {documents.map((document) => (
                                <ListItem
                                    key={document.id}
                                    divider
                                    secondaryAction={
                                        <Tooltip title="Delete document">
                                            <IconButton
                                                color="error"
                                                onClick={() =>
                                                    handleDelete(document.id)
                                                }
                                            >
                                                <DeleteIcon />
                                            </IconButton>
                                        </Tooltip>
                                    }
                                >
                                    <ListItemText
                                        primary={
                                            <Typography fontWeight={600}>
                                                {document.filename}
                                            </Typography>
                                        }
                                        secondary={
                                            document.uploaded_at
                                                ? new Date(
                                                      document.uploaded_at,
                                                  ).toLocaleString()
                                                : "Unknown upload date"
                                        }
                                    />
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                )}
            </AccordionDetails>
        </Accordion>
    );
});

DocumentList.displayName = "DocumentList";

export default DocumentList;