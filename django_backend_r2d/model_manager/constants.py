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
    GPT_4_TURBO: gpt-4-turbo - Context Window: 128,000 tokens - 2 
    GPT_3_5_TURBO: gpt-3.5-turbo - Context Window: 16,385 tokens - 3 
 
    List of supported embeddings within R2D
    TEXT_EMBEDDING_3_LARGE: text-embedding-3-large - Most capable embedding model for both english and non-english tasks - 3072 Dimension output
    TEXT_EMBEDDING_3_SMALL: text-embedding-3-small - Increased performance over 2nd generation ada embedding model - 1536 Dimension output
    """
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
