import { useState } from 'react';
import classNames from "classnames";
import axios from "axios"

import { API_BASE_URL } from "../helper/helper";
import { useEffect, useMemo } from "react";

const ALPHABET_ARR = 'abcdefghijklmnopqrstuvwxyz'.toUpperCase().split('');

/**
 * 
 * @param {string} gameId 
 * @param {object} result 
 */
export const Keyboard = ({ gameId, guessesNum }) => {
    const [keyboardStatus, setKeyboardStatus] = useState(); 

    const getKeyboardResult = async () => {
        if (gameId) {
            try {
                const url = `${API_BASE_URL}/games/${gameId}`;
                const { data } = await axios.get(url);
                setKeyboardStatus(data.data);
            } catch (err) {
                console.error(err);
            }
        }
    }

    useEffect(() => {
        getKeyboardResult();
    }, [guessesNum, gameId]);

    console.log(keyboardStatus);

    const getIsInCorrectLetters = (letter) => {
        return keyboardStatus?.incorrect_letters?.find(item => letter === item);
    }

    const getIsCorrectLetters = (letter) => {
        return keyboardStatus?.correct_letters?.find(item => letter === item);
    }

    const getIsWrongPosition = (letter) => {
        return keyboardStatus?.wrong_position_letters?.find(item => letter === item);
    }
    return (
        <div className="keyboard-container">
            {ALPHABET_ARR.map((char, idx) => {
                const isIncorrect = getIsInCorrectLetters(char);
                const isCorrect = getIsCorrectLetters(char);
                const isWrongPosition = getIsWrongPosition(char);

                return (
                    <div 
                        key={idx} 
                        className={classNames("keyboard-letter", {
                            'letter-incorrect': isIncorrect,
                            'letter-wrong-position': isWrongPosition,
                            'letter-correct': isCorrect,
                        })}
                    >
                        {char}
                    </div>
                )
            })}
        </div>
    )
}