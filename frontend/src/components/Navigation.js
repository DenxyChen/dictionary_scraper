import React from 'react';
import { Link } from 'react-router-dom';

function Navigation( ) {
    return (
        <nav class="nav-bar">
            <Link to="/" className="link"> Landing Page</Link>
        </nav>
    );
}

export default Navigation;
