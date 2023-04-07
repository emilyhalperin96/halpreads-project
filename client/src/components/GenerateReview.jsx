import React, {useState, useEffect} from 'react';

const GenerateReview = () => {
    const [question, setQuestion] = useState("")
 
    const [answer, setAnswer] = useState("")
 
    const handleQuestionChange = (e) => {
        setQuestion(e.target.value)
    }

    const handleGetAnswer = () => {
        fetch('/chat-gpt-ai/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question:question
            })
        })
        .then(response => response.json())
        .then(data => {
            setAnswer(data.result.choices[0].text)
        });
    };

   

    return(
        <div>
            <h1 className="text-center text-4xl">Generate a book review</h1>
            <p className="text-center">explaining what this does</p>
            <input type="text" value={question} onChange={handleQuestionChange} />
            <button onClick={handleGetAnswer}>Get Answer</button>
            <p>{answer}</p>
        </div>
    )
}

export default GenerateReview;