import { useEffect, useMemo, useState } from "react"
import axios from "axios"

import { GameBoardLettersRow } from "./GameBoardLettersRow"
import { Keyboard } from "./Keyboard"
import { API_BASE_URL } from "../helper/helper"

export const GameBoard = () => {
    const [gameId, setGameId] = useState();
    const [guesses, setGuesses] = useState([]); // user inputs
    const [guessResponses, setGuessResponses] = useState([]);

    const [hasCorrectAns, setHasCorrectAns] = useState(false);

    const isGameOver = useMemo(() => guessResponses.length === 5 && !hasCorrectAns, [guessResponses]);

    const handleValidResponse = (roundNum, value, data) => {
        // add API response to state
        setGuessResponses([...guessResponses, data]);
        setHasCorrectAns(data.guess_result === 'correct');
        
        // add user input guessed word into state
        const newGussesArr = [...guesses];
        newGussesArr[roundNum] = value;
        setGuesses(newGussesArr);
    }

    const handleGuessSubmit = async (roundNum, value) => {
        try {
            const url = `${API_BASE_URL}/guess`;
            const payload = {
                game_id: gameId,
                word: value.toUpperCase(),
            }
            const { data } = await axios.post(url, payload);

            if (data.guess_result === 'invalid') {
                alert('invalid word');
            } else {
                handleValidResponse(roundNum, value, data);
            }
        } catch(err) {
            // TODO: error warning
            console.error(err);
        }
    }

    const getNewGameId = async () => {
        // TODO: add loading state

        try {
            const url = `${API_BASE_URL}/new_game`;
            const { data } = await axios.post(url);
            setGameId(data.game_id);
        } catch(err) {
            // TODO: display error message
            console.error(err);
        }
    }

    const handleGameRestart = () => {
        setGuesses([]);
        setGuessResponses([]);
        setHasCorrectAns(false);

        getNewGameId();
    }

    useEffect(() => {
        getNewGameId();
    }, []);

    if (hasCorrectAns) {
        return (
            <div>
                <h2>🎉 Tada~ you win!</h2>
                <button onClick={handleGameRestart}>Start a new game</button>
            </div>
        )
    }

    if (isGameOver) {
        return (
            <div>
                <h2>🔥🧨 Gameover, give another try</h2>
                <button onClick={handleGameRestart}>Start a new game</button>
            </div>
        )
    }

    return (
        <>
            <div className="game-board-rows-container">
                <GameBoardLettersRow rowIndex={0} letters={guesses[0]} onSubmitRound={handleGuessSubmit}  rowGuessResponse={guessResponses[0]} />
                <GameBoardLettersRow rowIndex={1} letters={guesses[1]} onSubmitRound={handleGuessSubmit}  rowGuessResponse={guessResponses[1]} />
                <GameBoardLettersRow rowIndex={2} letters={guesses[2]} onSubmitRound={handleGuessSubmit}  rowGuessResponse={guessResponses[2]} />
                <GameBoardLettersRow rowIndex={3} letters={guesses[3]} onSubmitRound={handleGuessSubmit}  rowGuessResponse={guessResponses[3]} />
                <GameBoardLettersRow rowIndex={4} letters={guesses[4]} onSubmitRound={handleGuessSubmit}  rowGuessResponse={guessResponses[4]} />
            </div>

            <Keyboard gameId={gameId} guessesNum={guesses.length} />
        </>
    )
}