import { useEffect, useMemo, useRef, useState } from "react";
import EditIcon from "@mui/icons-material/Edit";

import type { Conversation } from "./types/conversation";

import {
Alert,
Box,
Button,
CircularProgress,
Container,
IconButton,
Paper,
Snackbar,
TextField,
Tooltip,
Typography,
} from "@mui/material";

import RestartAltIcon from "@mui/icons-material/RestartAlt";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";

import KnowledgeBasePanel, {
type KnowledgeBasePanelHandle,
} from "./components/KnowledgeBasePanel";

import AssistantMessage from "./components/AssistantMessage";
import ChatInput from "./components/ChatInput";
import UserMessage from "./components/UserMessage";

import { askQuestion } from "./services/chatService";

import type {
ChatMessage,
HistoryMessage,
} from "./types/chatMessage";

function App() {
const [question, setQuestion] = useState("");
const [loading, setLoading] = useState(false);
const [errorMessage, setErrorMessage] = useState("");

const [conversations, setConversations] = useState<
Conversation[]
>([]);

const [
currentConversationId,
setCurrentConversationId,
] = useState<string | null>(null);

const documentListRef =
useRef<KnowledgeBasePanelHandle>(null);

const bottomRef = useRef<HTMLDivElement>(null);

const currentConversation = useMemo(
() =>
conversations.find(
(conversation) =>
conversation.id ===
currentConversationId,
) ?? null,
[conversations, currentConversationId],
);

const messages =
currentConversation?.messages ?? [];

const [editingConversationId, setEditingConversationId] =
useState<string | null>(null);

const [editingTitle, setEditingTitle] =
useState("");

useEffect(() => {
bottomRef.current?.scrollIntoView({
behavior: "smooth",
});
}, [messages, loading]);

useEffect(() => {
const saved = localStorage.getItem("conversations");

try {
const loaded: Conversation[] = saved
? JSON.parse(saved)
: [];

if (loaded.length === 0) {
const conversation = createConversation();

setConversations([conversation]);
setCurrentConversationId(conversation.id);
return;
}

setConversations(loaded);
setCurrentConversationId(loaded[0].id);
} catch (error) {
console.error(error);

const conversation = createConversation();

setConversations([conversation]);
setCurrentConversationId(conversation.id);
}
}, []);

useEffect(() => {
localStorage.setItem(
"conversations",
JSON.stringify(conversations),
);
}, [conversations]);

function createConversation(): Conversation {
return {
id: crypto.randomUUID(),
title: "New Chat",
createdAt: new Date().toISOString(),
messages: [],
};
}

async function handleAsk() {
console.log("handleAsk() called");

console.log({
question,
currentConversationId,
currentConversation,
conversations,
});

if (
!question.trim() ||
!currentConversation
) {
console.log("Returning early");
return;
}

console.log("About to call backend...");

const currentQuestion = question;

setQuestion("");
setLoading(true);

try {
const history: HistoryMessage[] =
currentConversation.messages.flatMap(
(message) => [
{
role: "user",
content:
    message.question,
    },
    {
    role: "assistant",
    content:
        message.response
        .answer,
        },
        ],
        );

        const response =
        await askQuestion(
        currentQuestion,
        history,
        );

        const newMessage: ChatMessage = {
        question: currentQuestion,
        response,
        };

        setConversations((previous) =>
        previous.map(
        (conversation) => {
        if (
        conversation.id !==
        currentConversationId
        ) {
        return conversation;
        }

        return {
        ...conversation,
        title:
            conversation.messages.length === 0
            ? currentQuestion
            .replace(/\?$/, "")
            .trim()
            .slice(0, 50)
            : conversation.title,
            messages: [
            ...conversation.messages,
            newMessage,
            ],
            };
            },
            ),
            );
            } catch (error) {
            console.error(error);

            setErrorMessage(
            "Unable to contact the backend. Please try again.",
            );
            } finally {
            setLoading(false);
            }
            }

            function handleUploadSuccess() {
            documentListRef.current?.refresh();
            }

            function handleNewChat() {
            const conversation =
            createConversation();

            setConversations((previous) => [
            conversation,
            ...previous,
            ]);

            setCurrentConversationId(
            conversation.id,
            );

            setQuestion("");
            }

            function saveConversationTitle() {
    if (!editingConversationId) {
        return;
    }

    setConversations((previous) =>
        previous.map((conversation) =>
            conversation.id === editingConversationId
                ? {
                      ...conversation,
                      title:
                          editingTitle.trim() ||
                          "New Chat",
                  }
                : conversation,
        ),
    );

    setEditingConversationId(null);
    setEditingTitle("");
}

            function handleDeleteConversation(id: string) {
            if (!window.confirm("Delete this conversation?")) {
            return;
            }

            const remaining = conversations.filter(
            (conversation) => conversation.id !== id,
            );

            if (remaining.length === 0) {
            const conversation = createConversation();

            setConversations([conversation]);
            setCurrentConversationId(conversation.id);
            } else {
            setConversations(remaining);

            if (currentConversationId === id) {
            setCurrentConversationId(remaining[0].id);
            }
            }
            }

            return (
            <Container
            maxWidth={false}
            sx={{
            height: "100vh",
            display: "flex",
            p: 3,
            gap: 3,
            }}
            >
            {/* Sidebar */}

            <Paper
            elevation={2}
            sx={{
            width: 300,
            display: "flex",
            flexDirection: "column",
            p: 2,
            flexShrink: 0,
            overflow: "hidden",
            }}
            >
            <Typography
            variant="h6"
            fontWeight={700}
            sx={{ mb: 2 }}
            >
            Conversations
            </Typography>

            <Button
            variant="contained"
            startIcon={<RestartAltIcon />}
            fullWidth
            sx={{ mb: 2 }}
            onClick={handleNewChat}
            >
            New Chat
            </Button>

            <Box
            sx={{
            flex: 1,
            overflowY: "auto",
            }}
            >
            {conversations.map(
            (conversation) => (
            <Paper
            key={
            conversation.id
            }
            variant={
            conversation.id ===
            currentConversationId
            ? "elevation"
            : "outlined"
            }
            elevation={
            conversation.id ===
            currentConversationId
            ? 2
            : 0
            }
            sx={{
            p: 2,
            mb: 1,
            cursor: "pointer",
            bgcolor:
                conversation.id ===
                currentConversationId
                ? "primary.light"
                : undefined,
                }}
                onClick={() =>
                setCurrentConversationId(
                conversation.id,
                )
                }
                >
                <Box
                sx={{
                display:
                    "flex",
                    justifyContent:
                        "space-between",
                        alignItems:
                            "flex-start",
                            gap: 1,
                            }}
                            >
                            <Box
                            sx={{
                            flex: 1,
                            overflow:
                                "hidden",
                                }}
                                >
                                {editingConversationId ===
                                conversation.id ? (
                                <TextField
                                size="small"
                                autoFocus
                                fullWidth
                                value={editingTitle}
                                onChange={(
                                event: React.ChangeEvent<HTMLInputElement>,
                                ) =>
                                {
                                return setEditingTitle(
                                event.target.value
                                );
                                }
                                }
                                onClick={(
                                event: React.MouseEvent,
                                ) => event.stopPropagation()
                                }
                                onBlur={() => {
                                setConversations((previous) =>
                                previous.map((c) =>
                                c.id === editingConversationId
                                ? {
                                ...c,
                                title:
                                    editingTitle.trim() ||
                                    c.title,
                                    }
                                    : c,
                                    ),
                                    );

                                    setEditingConversationId(null);
                                    }}
                                    onKeyDown={(
                                    event: React.KeyboardEvent<HTMLInputElement>,
                                    ) => {
                                    if (event.key === "Enter") {
                                    event.preventDefault();

                                    setConversations((previous) =>
                                    previous.map((c) =>
                                    c.id === editingConversationId
                                    ? {
                                    ...c,
                                    title:
                                        editingTitle.trim() ||
                                        c.title,
                                        }
                                        : c,
                                        ),
                                        );

                                        setEditingConversationId(null);
                                        }

                                        if (event.key === "Escape") {
                                        setEditingConversationId(null);
                                        }
                                        }}
                                        />

                                        ) : (
                                        <Typography
                                        fontWeight={600}
                                        noWrap
                                        >
                                        {conversation.title}
                                        </Typography>
                                        )}

                                        <Typography
                                        variant="caption"
                                        color="text.secondary"
                                        >
                                        {new Date(
                                        conversation.createdAt,
                                        ).toLocaleDateString()}
                                        {" • "}
                                        {
                                        conversation
                                        .messages
                                        .length
                                        }
                                        {" message"}
                                        {conversation
                                        .messages
                                        .length !==
                                        1
                                        ? "s"
                                        : ""}
                                        </Typography>
                                        </Box>

                                        <Tooltip title="Delete conversation">
                                        <IconButton
                                        size="small"
                                        color="error"
                                        onClick={(
                                        event,
                                        ) => {
                                        event.stopPropagation();

                                        handleDeleteConversation(
                                        conversation.id,
                                        );
                                        }}
                                        >
                                        <DeleteOutlineIcon fontSize="small" />
                                        </IconButton>
                                        </Tooltip>

                                        <Tooltip title="Rename conversation">
                                        <IconButton
                                        size="small"
                                        onClick={(event) => {
                                        event.stopPropagation();

                                        setEditingConversationId(
                                        conversation.id,
                                        );

                                        setEditingTitle(
                                        conversation.title,
                                        );
                                        }}
                                        >
                                        <EditIcon fontSize="small" />
                                        </IconButton>
                                        </Tooltip>
                                        </Box>
                                        </Paper>
                                        ),
                                        )}
                                        </Box>
                                        </Paper>

                                        {/* Main Area */}

                                        <Box
                                        sx={{
                                        flex: 1,
                                        display: "flex",
                                        flexDirection: "column",
                                        minWidth: 0,
                                        }}
                                        >
                                        <Box
                                        sx={{
                                        display: "flex",
                                        justifyContent:
                                            "space-between",
                                            alignItems: "center",
                                            mb: 3,
                                            }}
                                            >
                                            <Typography
                                            variant="h4"
                                            fontWeight={700}
                                            >
                                            AI Knowledge Assistant
                                            </Typography>
                                            </Box>

                                            <KnowledgeBasePanel
                                            ref={documentListRef}
                                            onUploadSuccess={
                                            handleUploadSuccess
                                            }
                                            />

                                            <Box
                                            sx={{
                                            flex: 1,
                                            overflowY: "auto",
                                            pr: 1,
                                            }}
                                            >

                                            {messages.length === 0 && !loading && (
                                            <Box
                                            sx={{
                                            height: "100%",
                                            display: "flex",
                                            flexDirection: "column",
                                            justifyContent: "center",
                                            alignItems: "center",
                                            textAlign: "center",
                                            px: 3,
                                            }}
                                            >
                                            <Typography
                                            variant="h4"
                                            fontWeight={700}
                                            mb={2}
                                            >
                                            👋 Welcome to your Knowledge Assistant
                                            </Typography>

                                            <Typography
                                            color="text.secondary"
                                            sx={{
                                            maxWidth: 650,
                                            mb: 5,
                                            }}
                                            >
                                            Upload one or more PDF documents,
                                            then ask questions in natural
                                            language. The assistant searches
                                            your knowledge base and answers
                                            using the most relevant information
                                            from your documents.
                                            </Typography>

                                            <Paper
                                            variant="outlined"
                                            sx={{
                                            p: 3,
                                            borderRadius: 3,
                                            maxWidth: 650,
                                            width: "100%",
                                            }}
                                            >
                                            <Typography
                                            fontWeight={700}
                                            gutterBottom
                                            >
                                            Try asking:
                                                </Typography>

                                                <Typography>
                                                • What is FastAPI?
                                                </Typography>

                                                <Typography>
                                                • Summarize this document.
                                                </Typography>

                                                <Typography>
                                                • Explain dependency injection.
                                                </Typography>

                                                <Typography>
                                                • Compare the uploaded documents.
                                                </Typography>
                                                </Paper>
                                                </Box>
                                                )}

                                                {messages.map((message, index) => (
                                                <Box
                                                key={index}
                                                sx={{
                                                mb: 5,
                                                }}
                                                >
                                                <UserMessage
                                                question={message.question}
                                                />

                                                <AssistantMessage
                                                response={message.response}
                                                />
                                                </Box>
                                                ))}

                                                {loading && (
                                                <Paper
                                                elevation={1}
                                                sx={{
                                                p: 3,
                                                borderRadius: 4,
                                                mb: 3,
                                                }}
                                                >
                                                <Box
                                                sx={{
                                                display: "flex",
                                                alignItems: "center",
                                                gap: 2,
                                                }}
                                                >
                                                <CircularProgress
                                                size={20}
                                                />

                                                <Typography color="text.secondary">
                                                Thinking...
                                                </Typography>
                                                </Box>
                                                </Paper>
                                                )}

                                                <div ref={bottomRef} />
                                                </Box>

                                                <Box
                                                sx={{
                                                pt: 2,
                                                mt: 2,
                                                borderTop: "1px solid",
                                                borderColor: "divider",
                                                }}
                                                >
                                                <ChatInput
                                                question={question}
                                                loading={loading}
                                                onQuestionChange={setQuestion}
                                                onSubmit={handleAsk}
                                                />
                                                </Box>
                                                </Box>

                                                <Snackbar
                                                open={Boolean(errorMessage)}
                                                autoHideDuration={4000}
                                                onClose={() =>
                                                setErrorMessage("")
                                                }
                                                anchorOrigin={{
                                                vertical: "bottom",
                                                horizontal: "center",
                                                }}
                                                >
                                                <Alert
                                                severity="error"
                                                variant="filled"
                                                onClose={() =>
                                                setErrorMessage("")
                                                }
                                                >
                                                {errorMessage}
                                                </Alert>
                                                </Snackbar>
                                                </Container>
                                                );
                                                }

                                                export default App;
