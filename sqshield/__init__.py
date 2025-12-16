from .predict import *
import importlib.metadata

__all__ = ["get_query_length", "has_mixed_case", "get_comment_count", "get_special_char_count", "get_keyword_count", "get_tautology_count", "get_time_based_keyword_count", "preprocess_query", "predict"]
__version__ = importlib.metadata.version("sqshield")