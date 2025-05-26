import random
from datetime import date

def load_words():
    """Load valid 5-letter words from data/words.txt"""
    try:
        with open('data/words.txt', 'r') as f:
            return [word.strip().lower() for word in f if len(word.strip()) == 5]
    except FileNotFoundError:
        # Fallback word list for testing
        return [
            'hello', 'world', 'flask', 'games', 'words', 'magic', 'space', 
            'light', 'happy', 'smart', 'quick', 'brave', 'clean', 'fresh',
            'about', 'above', 'abuse', 'actor', 'acute', 'admit', 'adopt',
            'adult', 'after', 'again', 'agent', 'agree', 'ahead', 'alarm',
            'album', 'alert', 'alien', 'align', 'alike', 'alive', 'allow',
            'alone', 'along', 'alter', 'angel', 'anger', 'angle', 'angry'
        ]

def get_word_of_the_day():
    """Get consistent daily word based on date"""
    words = load_words()
    # Use date as seed for consistent daily word
    today = date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    return random.choice(words)
