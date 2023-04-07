import React, {useEffect, useState} from 'react';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './components/Home';
import Signup from './components/Signup';
import Login from './components/Login';
import GenerateRec from './components/GenerateRec';
import GenerateReview from './components/GenerateReview';
import About from './components/About';
import { useNavigate } from "react-router-dom";
import Logo from '/Users/emilyhalperin/Development/code/phase-5/halpreads-project/client/src/assets/Logo.png'
//import {useSelector, useDispatch} from 'react-redux'
//import {increments} from './actions'

//inside app, 
  //const counter = useSelector(state => state.counter)
  //const dispatch = useDispatch();
  //inside return 
  //<h1>Counter {counter}</h1>
  //if you want to add an argument, like 5 to increment. then you go back to actions and pass in num to increment, then under type add payload: num 
  // then in the reducer, change the return to state + action.payload 
  //<button onClick ={() => dispatch(increment())}>+</button>

function App() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // auto-login
    fetch('/check_session').then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  if (!user) return <Login onLogin={setUser} />;

  const navtoHome = () => {
    navigate('/home')
  };
  
  const navToAbout = () => {
    navigate('/about')
  };

  return (
    <div> 

      <div className='mx-auto px-.5'>
        <div className="flex justify-between items-center py-4 bg-blue-900 text-white">
        <div className="flex-shrink-0 ml-10 cursor-pointer">
           <img className="w-1/12 h-auto" src={Logo}></img>
        </div>
          <ul className="hidden md:flex overflow-x-hidden mr-10 font-semibold text-white">
            <li onClick={navtoHome} className="mr-6 p-1 ">Home</li>
            <li onClick={navToAbout} className="mr-6 p-1 ">About</li>
            <li className="mr-6 p-1">Contact</li>
          </ul>
        </div>
      </div>

      <Routes>
          <Route exact path ="/" element={<Login user={user} setUser={setUser} />} />
          <Route path ="/home" element={<Home user={user} setUser={setUser}/>} />
          <Route path="/signup" element={<Signup />} />
          <Route path='/generatereview' element={<GenerateReview />} />
          <Route path="/about" element={<About />} />
        </Routes>
    </div>
    
  );
}

export default App;