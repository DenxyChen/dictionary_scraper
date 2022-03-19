import React from 'react';
import Definition from './Definition';

export default function DefinitionList({ definitionArray }) {
    return ( 
        <ul>
            {definitionArray.map((definition, i) => <Definition definition={definition} key={i} />)}    
        </ul>
    );
}