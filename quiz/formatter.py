import re

def format_answer(text):
    """
    Used to format the correct_answer and player_answer removing characters, spaces
    and leading article words to check if the player_answer is correct.
    E.g. If the correct answer to a question is "X-Men" then a player submissions 
    of XMen, xmen, x-men, The X-Men etc should all return as a correct answer
    """
    # Modified From Stack Overflow answers:
    # https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
    # https://stackoverflow.com/questions/6531482/how-to-check-if-a-string-contains-an-element-from-a-list-in-
    # https://stackoverflow.com/questions/12883376/remove-the-first-word-in-a-python-string
    
    article_words = ("the ", "a ", "an ")
    lower_and_strip = text.strip().lower() 
    
    if lower_and_strip.startswith(article_words) and lower_and_strip not in article_words:
        split_string = lower_and_strip.split(" ", 1)
        # remove non alphanumeric characters and strip again removing 
        # spaces after reomving article words 
        flatten = re.sub("[\W_]+", "", split_string[1]).strip()
        
    else:
        flatten = re.sub("[\W_]+", "", lower_and_strip).strip()
        
    return flatten
