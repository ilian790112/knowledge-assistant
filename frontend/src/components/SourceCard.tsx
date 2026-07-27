import {
    Divider,
    Paper,
    Typography,
} from "@mui/material";

import type { Source } from "../types/source";

interface SourceCardProps {
    source: Source;
}

function SourceCard({
    source,
}: SourceCardProps) {
    return (
        <Paper
            variant="outlined"
            sx={{
                p: 2.5,
                mb: 2,
                borderRadius: 2,
                bgcolor: "background.default",
                borderColor: "divider",
            }}
        >
            <Typography
                variant="subtitle2"
                color="primary"
                fontWeight={700}
                sx={{ mb: 1 }}
            >
                Supporting excerpt
            </Typography>

            <Divider sx={{ mb: 2 }} />

            <Typography
                variant="body2"
                sx={{
                    whiteSpace: "pre-wrap",
                    lineHeight: 1.8,
                    color: "text.secondary",
                }}
            >
                {source.preview}
            </Typography>
        </Paper>
    );
}

export default SourceCard;