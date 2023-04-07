import React from 'react';
import {Link} from "react-router-dom"
import {useState, useEffect} from 'react';

const Signup = ({onLogin}) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirmation, setPasswordConfirmation] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    function handleSubmit(e) {
        e.preventDefault();
        setIsLoading(true);
        fetch("/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            password,
            password_confirmation: passwordConfirmation,
          }),
        }).then((r) => {
          setIsLoading(false);
          r.json().then((user) => onLogin(user));
        });
      }

    return (
        <div>
        <form className="mt-6" onSubmit={handleSubmit}>
            <h1 className="text-3xl font-semibold text-center text-[#243D98]">
                   Sign up
            </h1>
        <div className="mb-2">
            <label className="block text-sm font-semibold text-gray-800" htmlFor="username">Username</label>
            <input className="block w-full px-4 py-2 mt-2 text-purple-700 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40"
                type="text"
                id="username"
                autoComplete="off"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
        </div>
        <div className="mb-2">   
            <label className="block text-sm font-semibold text-gray-800" htmlFor="password">Password</label>
            <input className="block w-full px-4 py-2 mt-2 text-purple-700 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40"
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
        />
        </div>
        <div className="mb-2">
            <label className="block text-sm font-semibold text-gray-800" htmlFor="password">Password Confirmation</label>
            <input className="block w-full px-4 py-2 mt-2 text-purple-700 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40"
            type="password"
            id="password_confirmation"
            value={passwordConfirmation}
            onChange={(e) => setPasswordConfirmation(e.target.value)}
            autoComplete="current-password"
        />
        </div>
        <div className="mb-2">
        <button className="w-full px-4 py-2 tracking-wide text-white transition-colors duration-200 transform bg-[#243D98] hover:bg-[#9daada] focus:outline-none focus:bg-purple-600" variant="fill" color="primary" type="submit">{isLoading ? "Loading..." : "Sign Up"}</button>
        </div>
    </form>
    </div>
    )
}

export default Signup;