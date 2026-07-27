import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Props = {
    content: string;
};

function MarkdownMessage({
    content,
}: Props) {
    return (
        <ReactMarkdown
            remarkPlugins={[remarkGfm]}
        >
            {content}
        </ReactMarkdown>
    );
}

export default MarkdownMessage;