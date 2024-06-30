from enum import Enum

class ModelProvider(Enum):
    """
    List of model providers within R2D
    OPEN_AI: OpenAI models
    """
    OPEN_AI = "openai"
    # TOGETHER_AI = "togetherai"
    # LLAMA = "llama"
    # Add more providers as needed
    
class OpenAIModels(Enum):
    """
    List of OpenAI models within R2D
    GPT_4_O: gpt-4o - Context Window: 128,000 tokens
    GPT_4_TURBO: gpt-4-turbo - Context Window: 128,000 tokens
    GPT_4: gpt-4 - Context Window: 8,192 tokens
    GPT_3_5_TURBO: gpt-3.5-turbo - Context Window: 16,385 tokens

    List of supported embeddings within R2D
    OPEN_AI_TEXT_EMBEDDING_LARGE: text-embedding-3-large - Most capable embedding model for both english and non-english tasks - 3072 Dimension output
    OPEN_AI_TEXT_EMBEDDING_SMALL: text-embedding-3-small - Increased performance over 2nd generation ada embedding model - 1536 Dimension output
    """
    GPT_4_O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    OPEN_AI_TEXT_EMBEDDING_LARGE = "text-embedding-3-large"
    OPEN_AI_TEXT_EMBEDDING_SMALL = "text-embedding-3-small"
