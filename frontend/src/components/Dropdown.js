import React from 'react';

export default function Dropdown({ setLanguage }) {
    return ( 
        <select name="languages" id="languages" onChange={e => setLanguage(e.target.value)}>
            <option value="english">English</option>
            <option value="spanish">Spanish</option>
        </select>
    );
}