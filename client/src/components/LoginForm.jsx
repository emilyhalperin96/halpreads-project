import React, { useState } from "react";

function LoginForm({ onLogin, user, setUser }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
  
    

    function handleSubmit(e) {
      e.preventDefault();
      setIsLoading(true);
      fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      }).then((r) => {
        setIsLoading(false);
        if (r.ok) {
          r.json().then((user) => onLogin(user));
        }
      });
    }

    return (
      <form  className="mt-6" onSubmit={handleSubmit}>
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
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          </div>
          <div className="mt-6">
            <button className="w-full px-4 py-2 tracking-wide text-white transition-colors duration-200 transform bg-[#243D98] hover:bg-[#9daada] focus:outline-none focus:bg-purple-600" variant="fill" color="primary" type="submit">
                {isLoading ? "Loading..." : "Login"}
            </button>
          </div>
      </form>
    );
  }
  
  export default LoginForm;