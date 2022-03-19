import React from 'react';
import Comment from './Comment';

export default function CommentTable({ reviewsArray }) {
    return ( 
        <table>
                <tr>
                    <th>User Reviews</th>
                </tr>
                {reviewsArray.map((comment, i) => <Comment comment={comment} key={i} />)}    
        </table>
    );
}