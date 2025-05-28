import { useState } from 'react'
import './App.css'

function App() {
  const [guess, setGuess] = useState('')
  const [attempts, setAttempts] = useState(0)
  const [feedback, setFeedback] = useState('')
  const [hint, setHint] = useState('')
  const [gameOver, setGameOver] = useState(false)
  const [won, setWon] = useState(false)
  const [guessHistory, setGuessHistory] = useState([])
  const [loading, setLoading] = useState(false)

  const makeGuess = async () => {
    if (!guess.trim() || guess.length !== 5 || loading) return

    setLoading(true)
    
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/guess`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          guess: guess.toLowerCase(),
          attempts: attempts
        })
      })

      const data = await response.json()
      
      setFeedback(data.feedback)
      setAttempts(data.attempts)
      
      if (data.hint) {
        setHint(data.hint)
      }
      
      if (data.correct) {
        setWon(true)
        setGameOver(true)
      } else if (data.lost) {
        setGameOver(true)
        setFeedback(data.feedback + ` The word was: ${data.reveal}`)
      }
      
      setGuessHistory(prev => [...prev, {
        word: guess.toLowerCase(),
        feedback: data.feedback,
        attempts: data.attempts
      }])
      
      setGuess('')
      
    } catch {
      setFeedback('❌ Error connecting to server')
    }
    
    setLoading(false)
  }

  const resetGame = () => {
    setGuess('')
    setAttempts(0)
    setFeedback('')
    setHint('')
    setGameOver(false)
    setWon(false)
    setGuessHistory([])
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      makeGuess()
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">🔥 HotWord 🔥</h1>
        <p className="subtitle">Guess the 5-letter word! You have 6 attempts.</p>
        
        <div className="game-area">
          <div className="input-section">
            <input
              type="text"
              value={guess}
              onChange={(e) => setGuess(e.target.value.slice(0, 5))}
              onKeyPress={handleKeyPress}
              placeholder="Enter 5-letter word"
              maxLength={5}
              disabled={gameOver || loading}
              className="guess-input"
            />
            <button 
              onClick={makeGuess}
              disabled={gameOver || loading || guess.length !== 5}
              className="guess-button"
            >
              {loading ? '🔄' : 'Guess!'}
            </button>
          </div>

          <div className="feedback-section">
            <div className="attempts">Attempts: {attempts}/6</div>
            {feedback && <div className="feedback">{feedback}</div>}
            {hint && <div className="hint">{hint}</div>}
          </div>

          {guessHistory.length > 0 && (
            <div className="history">
              <h3>Your Guesses:</h3>
              {guessHistory.map((entry, index) => (
                <div key={index} className="history-entry">
                  <span className="history-word">{entry.word}</span>
                  <span className="history-feedback">{entry.feedback}</span>
                </div>
              ))}
            </div>
          )}

          {gameOver && (
            <div className="game-over">
              <h2>{won ? '🏆 You Won! 🔥🔥🔥' : '💀 Game Over'}</h2>
              <button onClick={resetGame} className="reset-button">
                Play Again Tomorrow
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
