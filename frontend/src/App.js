import './App.css';
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import HomePage from './pages/HomePage';

import Navigation from './components/Navigation'

function App() {
  return (
    <div className="App">
        <Router>
          
          {/* Global design features are displayed across the entire site. */}
          <header className="App-header">
            <h1>Random Word Generator</h1>
          </header>
          
          <Navigation />

          {/* Routing from Exploration — Routing & Forms */}
          <main>
            <Route path="/" exact><HomePage /></Route>
          </main>
          
          <footer>
              © 2022 Xiao Yu Chen, modified 2/14/2022
          </footer>
        
        </Router>
    </div>
  );
}

export default App;
