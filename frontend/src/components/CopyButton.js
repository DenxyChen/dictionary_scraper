import React from 'react';

export default function Copybutton({ word }) {
    const copyToClipboard = () => {
        navigator.clipboard.writeText(word)
    }

    return ( 
        <button onClick={copyToClipboard}>Copy to Clipboard</button>
    );
}

