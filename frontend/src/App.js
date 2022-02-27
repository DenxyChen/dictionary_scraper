import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import HomePage from './pages/HomePage';

import Navigation from './components/Navigation'

function App() {
  const [randomWord, setRandomWord] = useState("");

  useEffect(() => {
    fetch('/English').then(res => res.json()).then(data => {
      setRandomWord(data.word);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          This following word is randomly selected: {randomWord}
        </p>
      </header>
    </div>
    
  );
}

export default App;
