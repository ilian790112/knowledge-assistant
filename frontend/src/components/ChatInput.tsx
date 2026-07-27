import {
    Box,
    Button,
    Paper,
    TextField,
} from "@mui/material";

import SendIcon from "@mui/icons-material/Send";

interface ChatInputProps {
    question: string;
    loading: boolean;
    onQuestionChange: (
        value: string,
    ) => void;
    onSubmit: () => void;
}

function ChatInput({
    question,
    loading,
    onQuestionChange,
    onSubmit,
}: ChatInputProps) {
    function handleSubmit() {
        console.log("ChatInput: Send clicked");
        onSubmit();
    }

    function handleKeyDown(
        event: React.KeyboardEvent<HTMLDivElement>,
    ) {
        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {
            event.preventDefault();
            handleSubmit();
        }
    }

    return (
        <Paper
            elevation={3}
            sx={{
                p: 2,
                borderRadius: 3,
            }}
        >
            <TextField
                fullWidth
                multiline
                minRows={2}
                maxRows={8}
                placeholder="Ask anything about your documents..."
                value={question}
                onChange={(e) =>
                    onQuestionChange(e.target.value)
                }
                onKeyDown={handleKeyDown}
                disabled={loading}
                variant="outlined"
            />

            <Box
                sx={{
                    display: "flex",
                    justifyContent: "flex-end",
                    mt: 2,
                }}
            >
                <Button
                    variant="contained"
                    endIcon={<SendIcon />}
                    onClick={handleSubmit}
                    disabled={
                        loading ||
                        !question.trim()
                    }
                >
                    Send
                </Button>
            </Box>
        </Paper>
    );
}

export default ChatInput;