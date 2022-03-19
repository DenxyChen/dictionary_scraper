import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'
import Dropdown from '../components/Dropdown';
import DefinitionList from '../components/DefinitionList';
import CommentTable from '../components/CommentTable';
import CopyButton from '../components/CopyButton';

export default function HomePage( ) {
  const navigate = useNavigate();

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
      await loadReviews();
      document.body.style.cursor="default"; 
    }
  }

  const loadReviews = async () => {
    const response = await fetch(`/reviews/${word}`);
    
    if (response.status === 200) {
      const data = await response.json();
      console.log(data.all_reviews);
      await setReviews(data.all_reviews);
    }
  }

  const confirmNav = (e) => {
    let choice = window.confirm("Are you sure you want to navigate to Merriam-Webster? You will lose the current word.");
    if (choice === true) {
      return
    }
    else{
      e.preventDefault();
    }  
  }


  useEffect(() => {
    loadReviews();
  }, []);

  return (
    <article>
      <div class="center">
        <p>Select a language using the dropdown:</p>
        <Dropdown setLanguage={setLanguage}/>
      </div>
      <button id="go" onClick={() => getWordData(language)}>GO</button>
      <CopyButton word={word}/>
      <div id="ran-word">
          <h2>{word}</h2>
          <h3>{type}</h3>
      </div>
      <div id="definition">
          <h4>Definition of {word}</h4>
          <DefinitionList definitionArray={definition} />
      <a href={`https://www.merriam-webster.com/dictionary/${word}`} onClick={confirmNav}>Link to the dictionary entry</a><br></br><br></br>
      </div>

      <CommentTable reviewsArray={reviews} />
      <iframe id="iframe" name="my_iframe"></iframe>
      <form method="POST" action="http://localhost:8000/add_review" target="my_iframe">
        <input type="hidden" value={word} placeholder="Confirm word" name="word"/>
        <input type="text" placeholder="Add a comment" name="review"/>
        <button type="submit" onClick={() => loadReviews()}>Submit comment</button>
      </form>
    </article>
  );
}