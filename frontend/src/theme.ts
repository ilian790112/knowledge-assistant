import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        mode: "light",

        primary: {
            main: "#2563eb",
        },

        secondary: {
            main: "#7c3aed",
        },

        background: {
            default: "#f5f7fb",
            paper: "#ffffff",
        },
    },

    shape: {
        borderRadius: 14,
    },

    typography: {
        fontFamily: [
            "Inter",
            "Segoe UI",
            "Roboto",
            "Helvetica",
            "Arial",
            "sans-serif",
        ].join(","),

        h4: {
            fontWeight: 700,
        },

        h5: {
            fontWeight: 600,
        },

        button: {
            textTransform: "none",
            fontWeight: 600,
        },
    },

    components: {
        MuiPaper: {
            styleOverrides: {
                root: {
                    borderRadius: 16,
                },
            },
        },

        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 12,
                    paddingLeft: 24,
                    paddingRight: 24,
                },
            },
        },

        MuiTextField: {
            defaultProps: {
                fullWidth: true,
            },
        },
    },
});

export default theme;