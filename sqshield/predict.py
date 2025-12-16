import importlib.resources
import joblib
import re
import pandas as pd

model_path = importlib.resources.files("sqshield.model").joinpath("sql_injection_model.pkl")
with importlib.resources.as_file(model_path) as p:
    model = joblib.load(p)


def get_query_length(query: str) -> int:
    """Calculates the length of the query string.

    Args:
        query (str): The SQL query string.

    Returns:
        int: The total number of characters in the query.
    """
    return len(query)

def has_mixed_case(query: str) -> int:
    """Checks if the query string contains both uppercase and lowercase characters.

    Args:
        query (str): The SQL query string.

    Returns:
        int: 1 if the query has mixed case, 0 otherwise.
    """
    return 1 if any(c.islower() for c in query) and any(c.isupper() for c in query) else 0

def get_comment_count(query: str) -> int:
    """Counts the number of comments in the query.

    Args:
        query (str): The SQL query string.

    Returns:
        int: The total count of '--' and '#' comment indicators.
    """
    return query.count('--') + query.count('#')

def get_special_char_count(query: str) -> int:
    """Counts the occurrences of specific special characters in the query.

    The special characters counted are: ''', '"', ';', '=', '(', ')'

    Args:
        query (str): The SQL query string.

    Returns:
        int: The total count of the specified special characters.
    """
    special_chars = ['\'', '"' , ';', '=', '(', ')']
    count = 0
    for char in special_chars:
        count += query.count(char)
    return count

def get_keyword_count(query: str) -> int:
    """Counts the number of SQL keywords in the query.

    The keywords are matched in a case-insensitive manner. Keywords are:
    'select', 'from', 'where', 'union', 'insert', 'delete', 'update', 'and', 'or', 'not'

    Args:
        query (str): The SQL query string.

    Returns:
        int: The total number of keywords found in the query.
    """
    keywords = ['select', 'from', 'where', 'union', 'insert', 'delete', 'update', 'and', 'or', 'not']
    count = 0
    for keyword in keywords:
        if re.search(r'\b' + keyword + r'\b', query, re.IGNORECASE):
            count += 1
    return count

def get_tautology_count(query: str) -> int:
    """Counts the number of tautological patterns in the query.

    This function specifically looks for patterns like '1=1' after normalizing the query.

    Args:
        query (str): The SQL query string.

    Returns:
        int: The number of tautological patterns found.
    """
    normalized_query = query.replace("'", "").replace(" ", "")
    tautologies = [r"1=1"]
    count = 0
    for tautology in tautologies:
        count += len(re.findall(tautology, normalized_query, re.IGNORECASE))
    return count

def get_time_based_keyword_count(query: str) -> int:
    """Counts keywords related to time-based SQL injection attacks.

    Keywords are matched in a case-insensitive manner. Keywords are:
    'sleep', 'benchmark', 'waitfor delay'

    Args:
        query (str): The SQL query string.

    Returns:
        int: The total number of time-based keywords found.
    """
    time_based_keywords = ['sleep', 'benchmark', 'waitfor delay']
    count = 0
    for keyword in time_based_keywords:
        if re.search(r'\b' + keyword + r'\b', query, re.IGNORECASE):
            count += 1
    return count

def preprocess_query(query: str) -> pd.DataFrame:
    """Preprocesses a raw SQL query to extract features for the prediction model.

    This function engineers a set of features from the query string and returns them
    as a pandas DataFrame.

    Args:
        query (str): The raw SQL query string.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted features.
    """
    # This function will take a raw query and return a dataframe with the engineered features
    features = {
        'query_length': [get_query_length(query)],
        'has_mixed_case': [has_mixed_case(query)],
        'comment_count': [get_comment_count(query)],
        'special_char_count': [get_special_char_count(query)],
        'keyword_count': [get_keyword_count(query)],
        'tautology_count': [get_tautology_count(query)],
        'time_based_keyword_count': [get_time_based_keyword_count(query)]
    }
    return pd.DataFrame(features)

    
def predict(query: str) -> list[bool]:
    """Predicts whether a SQL query is a potential injection attack.

    It first checks for simple tautologies. If none are found, it uses a
    pre-trained machine learning model to make the prediction based on
    various query features.

    Args:
        query (str): The SQL query to analyze.

    Returns:
        list[int]: A list containing the prediction, where 1 indicates a
                   potential SQL injection attack and 0 indicates a safe query.
    """
    if get_tautology_count(query) > 0:
        return [1]
        
    # If no tautology, use the model
    processed_query_df = preprocess_query(query)
    
    return model.predict(processed_query_df)
    