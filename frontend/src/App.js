import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import HomePage from './pages/HomePage';

import Navigation from './components/Navigation'

function App() {
  const [aWord, setWord] = useState("");
  const [definitions, setDefinitions] = useState([]);
  const [type, setType] = useState("");

  useEffect(() => {
    fetch('/english').then(res => res.json()).then(data => {
      setWord(data.word);
      setDefinitions(data.definitions);
      setType(data.type);
    });
  }, [])

  return (
    <div className="App">  
          {/* Global design features are displayed across the entire site. */}
          <header className="App-header">
            <h1>Random Word Generator</h1>
            <p>The word is {aWord}. It is a(n) {type}.</p>
          </header>
          
          <footer>
              © 2022 github.com/DenxyChen
          </footer>
        
    </div>
  );
}

export default App;
