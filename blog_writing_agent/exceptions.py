class BaseException(Exception):
    """Base exception for all custom exceptions."""

    def __init__(self, message: str):
        super().__init__(message)

    def __str__(self):
        return f"{self.__class__.__name__}: {super().__str__()}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{super().__str__()}')"


class LLMException(Exception):
    """Base exception for LLM-related errors."""

    def __init__(self, message: str):
        super().__init__(message)


class LLMInvocationException(LLMException):
    """Exception raised when an LLM invocation fails."""

    def __init__(self, message: str):
        super().__init__(message)


class GraphExecutionException(BaseException):
    """Exception raised when graph execution fails."""

    def __init__(self, message: str):
        super().__init__(message)


class ConfigurationException(BaseException):
    """Base exception for configuration-related errors."""

    def __init__(self, message: str):
        super().__init__(message)


class MissingAPIKeyException(ConfigurationException):
    """Raised when OPENROUTER_API_KEY is missing."""

    def __init__(self, message: str):
        super().__init__(message)


class InvalidModelConfigurationException(ConfigurationException):
    """Raised when model configuration is invalid."""

    def __init__(self, message: str):
        super().__init__(message)


class LLMRateLimitException(LLMException):
    """Exception raised when model provider rate limits requests."""

    def __init__(self, message: str):
        super().__init__(message)


class PlanGenerationException(BaseException):
    """Raised when the orchestrator fails to generate a valid plan."""

    def __init__(self, message: str):
        super().__init__(message)


class SectionGenerationException(BaseException):
    """Raised when a worker fails to generate a section."""

    def __init__(self, message: str):
        super().__init__(message)


class OutputWriteException(BaseException):
    """Raised when writing final markdown output fails."""

    def __init__(self, message: str):
        super().__init__(message)

__all__ = [
    "BaseException",
    "LLMException",
    "LLMInvocationException",
    "GraphExecutionException",
    "ConfigurationException",
    "MissingAPIKeyException",
    "InvalidModelConfigurationException",
    "LLMRateLimitException",
    "PlanGenerationException",
    "SectionGenerationException",
    "OutputWriteException",
]
