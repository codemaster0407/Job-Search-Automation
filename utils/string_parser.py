import re

def extract_https_links(text):
    pattern = r'https://[^\s]*\bjob\d+\b[^\s]*'
    return re.findall(pattern, text)