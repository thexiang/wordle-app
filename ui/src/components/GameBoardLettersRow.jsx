import { useMemo, useState } from "react";
import { GameBoardLetterBox } from "./GameBoardLetterBox";

/**
 * 
 * @param {int} rowIndex
 * @param {string} letters 
 * @param {object | undefined} rowGuessResponse
 * @param {Function} onSubmitRound
 * 
 */

 export const LETTER_BOX_RESPONSE_KEY_ARR = ['letter1', 'letter2', 'letter3', 'letter4', 'letter5'];

export const GameBoardLettersRow = ({ rowIndex, letters, rowGuessResponse, onSubmitRound }) => {
    const [newLetters, setNewLetters] = useState([]);
    
    // the row will be either undefined or a object with all information
    const isIncompleteRow = useMemo(() => rowGuessResponse === undefined, [rowGuessResponse]);

    const handleUpdateLetter = (index, value) => {
        const newArr = [...newLetters];
        newArr[index] = value;
        setNewLetters(newArr)
    }

    const handleSubmit = () => {
        const lettersStr = newLetters.join('');

        onSubmitRound(rowIndex, lettersStr);
    }

    const isSubmitDisabled = useMemo(() => {
        return newLetters.length < 5;
    }, [newLetters])

    return (
        <div className="game-board-letters-row">
            {/* boxKey: letter1, letter2, etc */}
            {LETTER_BOX_RESPONSE_KEY_ARR.map((boxKey, idx) => {
                return (
                    <GameBoardLetterBox
                        key={idx}
                        letter={letters?.[idx]}
                        boxNumber={idx}
                        result={rowGuessResponse?.[boxKey]}
                        onUpdateLetter={handleUpdateLetter}
                    />
                )
            })}

            {isIncompleteRow && (<button onClick={handleSubmit} disabled={isSubmitDisabled}>submit</button>)}            
        </div>
    )
}