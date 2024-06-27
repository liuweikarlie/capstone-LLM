import re
from unstructured.documents.elements import Text
from unstructured.cleaners.core import replace_unicode_quotes
from unstructured.cleaners.core import clean
from unstructured.cleaners.core import clean_non_ascii_chars
def remove_links(text):
    """
    Remove all links from the given text.
    
    Args:
    text (str): The input text from which links need to be removed.
    
    Returns:
    str: The text with all links removed.
    """
    # Regular expression pattern to match URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    # Substitute matched URLs with an empty string
    cleaned_text = re.sub(url_pattern, '', text)
    
    return cleaned_text

def contains_link(text):
    """
    Check if the given text contains any links.
    
    Args:
    text (str): The input text to check for links.
    
    Returns:
    bool: True if the text contains at least one link, False otherwise.
    """
    # Regular expression pattern to match URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    # Search for URLs in the text
    if re.search(url_pattern, text):
        return True
    else:
        return False
    




def clean_text(texts):
    texts = [replace_unicode_quotes(text) for text in texts]
    texts = [remove_links(text) for text in texts]
    texts = [clean(text, bullets=True, lowercase=True,extra_whitespace=True, dashes=True) for text in texts]
    texts = [clean_non_ascii_chars(text) for text in texts]
    return texts


