from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import os

# Add parent directory to path so we can import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.word_manager import get_word_of_the_day, load_words
    from backend.game import evaluate_guess
    from backend.utils import get_dynamic_hints

    # Build VALID_WORDS from your full data/words.txt
    VALID_WORDS = set(load_words())
except ImportError as e:
    print(f"Import error: {e}")
    VALID_WORDS = set()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length).decode('utf-8'))

            guess = data.get('guess', '').lower()
            attempts = data.get('attempts', 0)

            # Validate guess length and characters
            if len(guess) != 5 or not guess.isalpha():
                self._send_json({
                    "feedback": "❌ Please enter exactly 5 alphabetic letters.",
                    "correct": False,
                    "hint": None,
                    "reveal": None,
                    "attempts": attempts,
                    "lost": False
                })
                return

            # Validate against backed word list
            if guess not in VALID_WORDS:
                self._send_json({
                    "feedback": "❌ Not a recognized word!",
                    "correct": False,
                    "hint": None,
                    "reveal": None,
                    "attempts": attempts,
                    "lost": False
                })
                return

            word = get_word_of_the_day()
            attempts += 1

            label, emoji, similarity, correct, _ = evaluate_guess(guess, word)

            hint = None
            reveal = None
            lost = False

            # Provide dynamic hints on 4th and 5th attempts
            if not correct:
                if attempts == 4:
                    hint = get_dynamic_hints(word, 0)
                elif attempts == 5:
                    hint = get_dynamic_hints(word, 1)
                elif attempts >= 6:
                    reveal = word
                    lost = True

            feedback = f"{label} {emoji} (Similarity: {similarity:.2f})"

            response = {
                "feedback": feedback,
                "correct": correct,
                "hint": hint,
                "reveal": reveal,
                "attempts": attempts,
                "lost": lost
            }
            self._send_json(response)

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _send_json(self, obj):
        """Helper to send a 200 JSON response with CORS headers"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())

if __name__ == "__main__":
    addr = ("0.0.0.0", 8000)
    print(f"Starting API at http://{addr[0]}:{addr[1]}/guess")
    server = HTTPServer(addr, handler)
    server.serve_forever()
