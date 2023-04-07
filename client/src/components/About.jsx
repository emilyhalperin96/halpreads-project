import React from 'react';
import HalpReadsIcon from '/Users/emilyhalperin/Development/code/phase-5/halpreads-project/client/src/assets/HalpReadsIcon.png'


const About = () => {

    return(
        <div>
            <img className="mx-auto w-1/5 h-auto mt-8" src={HalpReadsIcon}></img>
            <h1 className="text-center">About @halpreads</h1>
            <p>Welcome to @halpreads - my book instagram that I started in 2020 with the aim of providing book recommendations to fellow readers. My mission is to encourage people to read more, challenge themselves, consider other perspectives, and turn reading into a habit.</p>
            <p>I hope to create a community of readers who can share their love of books with one another.</p>
            <p>I believe reading is a valuable tool for learning and personal growth. Whether it's fiction or non-fiction, books have the power to expand our minds and enrich our lives. </p>
            <p>For each review, I provide a synopsis of the book - no spoilers, my personal thoughts and impressions, and a recommendation for who might enjoy the book.</p>
            <p>Whether you're a seasoned reader or just starting out, @halpreads is the perfect place to discover new books, share your thoughts, and connect with other readers.</p>
        </div>
    )
}

export default About;