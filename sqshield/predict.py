import importlib.resources
import joblib
import re
import pandas as pd

def get_query_length(query):
    return len(query)

def has_mixed_case(query):
    return 1 if any(c.islower() for c in query) and any(c.isupper() for c in query) else 0

def get_comment_count(query):
    return query.count('--') + query.count('#')

def get_special_char_count(query):
    special_chars = ['\'', '"' , ';', '=', '(', ')']
    count = 0
    for char in special_chars:
        count += query.count(char)
    return count

def get_keyword_count(query):
    keywords = ['select', 'from', 'where', 'union', 'insert', 'delete', 'update', 'and', 'or', 'not']
    count = 0
    for keyword in keywords:
        if re.search(r'\b' + keyword + r'\b', query, re.IGNORECASE):
            count += 1
    return count

def get_tautology_count(query):
    normalized_query = query.replace("'", "").replace(" ", "")
    tautologies = [r"1=1"]
    count = 0
    for tautology in tautologies:
        count += len(re.findall(tautology, normalized_query, re.IGNORECASE))
    return count

def get_time_based_keyword_count(query):
    time_based_keywords = ['sleep', 'benchmark', 'waitfor delay']
    count = 0
    for keyword in time_based_keywords:
        if re.search(r'\b' + keyword + r'\b', query, re.IGNORECASE):
            count += 1
    return count

def preprocess_query(query):
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
def load_model():
    with importlib.resources.path("sqshield.model", "sql_injection_model.pkl") as p:
        MODEL_PATH = str(p)
        model = joblib.load(MODEL_PATH)
        return model
    
def predict(data, model):
    if get_tautology_count(data) > 0:
        return [1]
        
    # If no tautology, use the model
    processed_query_df = preprocess_query(data)
    
    return model.predict(processed_query_df)
    