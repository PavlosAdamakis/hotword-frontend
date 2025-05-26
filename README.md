# HotWord — A Wordle-style Challenge Game

HotWord is a new fast-paced game, semantically-driven word game where players get only 6 attempts to guess the 5-letter word of the day.

Instead of color tiles, you get 🔥 heat-based clues:
- **"Freezing" 🧊** = way off
- **"Getting Warmer" 🌡️** = closer
- **"On Fire" 🔥🔥🔥** = nearly there

And if you're stuck? Hints drop after 3 incorrect tries to guide you in the right direction 🧠

---

## 🎮 How to Play

1. Type a 5-letter word
2. Get heat feedback based on semantic similarity
3. After 3 bad guesses, you'll receive a clue
4. Can’t get it by the 6th guess? The answer is revealed 😵

---

## 🌟 Features

- Word changes **automatically every day**
- Hints appear dynamically to assist players
- Uses **sentence-transformers** to semantically rank guesses
- Built with Python, Flask & NLTK

---

## 🧪 Run Locally

```bash
git clone https://github.com/PavlosAdamakis/HotWord.git
cd HotWord
pip install -r requirements.txt
python app.py

> ⚠️ This game and its concept are original to [@PavlosAdamakis](https://github.com/PavlosAdamakis).  
> You may fork or remix under the MIT License, but attribution is required. No commercial clones without permission.

