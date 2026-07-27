import {
    Box,
    Paper,
    Typography,
} from "@mui/material";

import PersonIcon from "@mui/icons-material/Person";

interface UserMessageProps {
    question: string;
}

function UserMessage({
    question,
}: UserMessageProps) {
    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: "flex-end",
                mb: 3,
            }}
        >
            <Paper
                elevation={2}
                sx={{
                    maxWidth: "65%",
                    px: 3,
                    py: 2,
                    borderRadius: 4,
                    bgcolor: "primary.main",
                    color: "primary.contrastText",
                }}
            >
                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: 1,
                        mb: 1,
                    }}
                >
                    <PersonIcon fontSize="small" />

                    <Typography
                        variant="subtitle2"
                        fontWeight={600}
                    >
                        You
                    </Typography>
                </Box>

                <Typography
                    sx={{
                        whiteSpace: "pre-wrap",
                        wordBreak: "break-word",
                    }}
                >
                    {question}
                </Typography>
            </Paper>
        </Box>
    );
}

export default UserMessage;