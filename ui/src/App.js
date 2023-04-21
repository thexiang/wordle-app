import { GameBoard } from './components/GameBoard';

import './App.css';

function App() {
  return (
    <div className="App">
      <div className="layout">
        <h1>Wordle</h1>
        <GameBoard />
      </div>
    </div>
  );
}

export default App;
