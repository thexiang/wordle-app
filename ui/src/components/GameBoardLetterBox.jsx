import classNames from "classnames";

/**
 * 
 * @param {string} letter
 * @param {int} boxNumber
 * @param {object} result // correct, incorrect, or wrong_position
 * @param {Function} onUpdateLetter
 * 
 */

export const GameBoardLetterBox = ({ letter, boxNumber, result, onUpdateLetter }) => {
    
    return (
        <input 
            className={classNames('gameboard-letter-box', {
                // this ticky keyname is trying to match CSS classname
                [`letter-${result?.replace("_", "-")}`] : Boolean(result)
            })}
            onChange={e => onUpdateLetter(boxNumber, e.target.value)} 
            value={letter}
            maxLength="1"
        />
    )
}