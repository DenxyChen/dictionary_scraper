import React, { useState } from 'react';
import Dropdown from '../components/Dropdown';
import DisplayView from '../components/DisplayView';
import logo from "../images/MWLogo_DarkBG_120x120_2x.png";
import DefinitionList from '../components/DefinitionList';

export default function HomePage( ) {
  const [language, setLanguage] = useState("english");
  const [word, setWord] = useState("");
  const [definition, setDefinition] = useState([]);
  const [type, setType] = useState("");
  const [reviews, setReviews] = useState([]);

  const getWordData = async (language) => {
    document.body.style.cursor="wait"; 
    const response = await fetch(`/${language}`);

    if (response.status === 200) {
      const data = await response.json();
      await setWord(data.word);
      await setDefinition(data.definition);
      await setType(data.type);
      await setReviews(data.reviews);
      document.body.style.cursor="default"; 
    }
  }

  return (
    <article>
      <div class="center">
        <p>Select a language using the dropdown:</p>
        <Dropdown setLanguage={setLanguage}/>
      </div>
      <button id="go" onClick={() => getWordData(language)}>GO</button>
      <div id="ran-word">
          <h2>{word}</h2>
          <h3>{type}</h3>
      </div>
      <div id="definition">
          <h4>Definition of {word}</h4>
          <DefinitionList definitionArray={definition} />
      <a href={`https://www.merriam-webster.com/dictionary/${word}`}>Link to the dictionary entry</a><br></br><br></br>
      </div>
      <p>{reviews}</p>
    </article>
  );
}
  