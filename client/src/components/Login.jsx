import React from 'react';
import LoginForm from "../components/LoginForm";
import Signup from "../components/Signup";
import Home from "../components/Home";
import { useState } from "react";

const Login = ({onLogin}) => {
    const [showLogin, setShowLogin] = useState(true)
    const [showHome, setShowHome] = useState(false)
    return (
        <div className="relative flex flex-col justify-center min-h-screen overflow-hidden">
            <div className="w-full p-6 m-auto bg-white rounded-md shadow-xl shadow-rose-600/40 ring-2 ring-[#243D98] lg:max-w-xl">
                <>
            {showLogin ? (
                <> 
                <h1 className="text-3xl font-semibold text-center text-[#243D98]">
                   Login
                </h1>
                <LoginForm className="mt-6" onLogin={onLogin} />
                <p className="mt-8 text-xs font-light text-center text-gray-700">
                    {" "}
                    Don't have an account? 
                    {" "}
                    <button className="font-medium text-[#243D98] hover:underline" onClick={() => setShowLogin(false)}>
                        Sign Up
                    </button>
                </p>
                </>
                ) : (
                <>
                <Signup onLogin={onLogin} />
                {showHome ? <Home /> : null}
                </>
                )}
                </>
            </div>
        </div>
    )
}

export default Login;