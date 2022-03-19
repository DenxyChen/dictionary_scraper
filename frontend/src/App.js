// style sheet
import './App.css';

// dependencies
import { useState, React} from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// pages
import HomePage from './pages/HomePage';

// components
import Navigation from './components/Navigation';
import logo from "./images/MWLogo_DarkBG_120x120_2x.png";

export default function App() {
  return (
    <div className="App">
      <BrowserRouter>

        {/* Global design features are displayed across the entire site. */}
        <header className="App-header">
          <img src={logo} alt="Merriam-Webster Logo"/>
          <h1>Word Randomizer</h1>
        </header>

        <Navigation />

        <main>
          <Routes>
            <Route path="/" exact element={<HomePage />} />
          </Routes>
        </main>

        <footer>
              © 2022 Xiao Yu Chen, modified 03/18/2022
        </footer>

    </BrowserRouter>
    </div>
  );
}
