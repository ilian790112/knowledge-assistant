import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Avatar,
    Box,
    Button,
    Chip,
    Paper,
    Typography,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import DescriptionIcon from "@mui/icons-material/Description";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

import MarkdownMessage from "./MarkdownMessage";
import SourceCard from "./SourceCard";

import type { ChatResponse } from "../types/chatResponse";

interface AssistantMessageProps {
    response: ChatResponse;
}

function AssistantMessage({
    response,
}: AssistantMessageProps) {
    async function copyAnswer() {
        await navigator.clipboard.writeText(
            response.answer,
        );
    }

    // Group chunks by filename
    const groupedSources = response.sources.reduce(
        (groups, source) => {
            const key = source.filename;

            if (!groups[key]) {
                groups[key] = [];
            }

            groups[key].push(source);

            return groups;
        },
        {} as Record<
            string,
            typeof response.sources
        >,
    );

    return (
        <Box
            sx={{
                display: "flex",
                alignItems: "flex-start",
                gap: 2,
            }}
        >
            <Avatar
                sx={{
                    bgcolor: "secondary.main",
                }}
            >
                AI
            </Avatar>

            <Paper
                elevation={1}
                sx={{
                    flex: 1,
                    p: 3,
                    borderRadius: 4,
                }}
            >
                <Box
                    sx={{
                        display: "flex",
                        justifyContent:
                            "space-between",
                        alignItems: "center",
                        mb: 2,
                    }}
                >
                    <Typography
                        variant="h6"
                        fontWeight={700}
                    >
                        Assistant
                    </Typography>

                    <Button
                        size="small"
                        startIcon={
                            <ContentCopyIcon />
                        }
                        onClick={copyAnswer}
                    >
                        Copy
                    </Button>
                </Box>

                <MarkdownMessage
                    content={response.answer}
                />

                {Object.keys(groupedSources)
                    .length > 0 && (
                    <Box sx={{ mt: 4 }}>
                        <Typography
                            variant="subtitle1"
                            fontWeight={700}
                            gutterBottom
                        >
                            Sources
                        </Typography>

                        {Object.entries(
                            groupedSources,
                        ).map(
                            ([
                                filename,
                                sources,
                            ]) => (
                                <Accordion
                                    key={
                                        filename
                                    }
                                    elevation={
                                        0
                                    }
                                    sx={{
                                        mb: 2,
                                        border:
                                            "1px solid",
                                        borderColor:
                                            "divider",
                                        borderRadius: 2,
                                        "&:before":
                                            {
                                                display:
                                                    "none",
                                            },
                                    }}
                                >
                                    <AccordionSummary
                                        expandIcon={
                                            <ExpandMoreIcon />
                                        }
                                    >
                                        <Box
                                            sx={{
                                                display:
                                                    "flex",
                                                alignItems:
                                                    "center",
                                                gap: 2,
                                                width:
                                                    "100%",
                                            }}
                                        >
                                            <DescriptionIcon color="primary" />

                                            <Typography
                                                fontWeight={
                                                    600
                                                }
                                            >
                                                {
                                                    filename
                                                }
                                            </Typography>

                                            <Chip
                                                size="small"
                                                label={`${sources.length} passage${
                                                    sources.length >
                                                    1
                                                        ? "s"
                                                        : ""
                                                }`}
                                                sx={{
                                                    ml: "auto",
                                                }}
                                            />
                                        </Box>
                                    </AccordionSummary>

                                    <AccordionDetails>
                                        {sources.map(
                                            (
                                                source,
                                            ) => (
                                                <SourceCard
                                                    key={
                                                        source.chunk_id
                                                    }
                                                    source={
                                                        source
                                                    }
                                                />
                                            ),
                                        )}
                                    </AccordionDetails>
                                </Accordion>
                            ),
                        )}
                    </Box>
                )}
            </Paper>
        </Box>
    );
}

export default AssistantMessage;