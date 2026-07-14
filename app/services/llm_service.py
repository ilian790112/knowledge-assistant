class LLMService:
    """
    Base service for interacting with a language model.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the language model.
        """

        raise NotImplementedError(
            "LLMService.generate() must be implemented."
        )