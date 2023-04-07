import React from 'react';
import {useState} from 'react';
import GenerateReview from './GenerateReview';
import { useNavigate } from "react-router-dom";

const Home = ({user, setUser}) => {
  const navigate = useNavigate();

  //const handleGenerateReview = () => {
    //setGenerateReview((generateReview) => !generateReview)
 // }

  const navtoGR = () => {
    navigate('/generatereview')
  };

    function handleLogoutClick() {
        fetch("/logout", { method: "DELETE" }).then((r) => {
          if (r.ok) {
            setUser(null);
          }
        });
      }
    return (
    

        <div className="w-full p-6 bg-[#F8BCCE]">
          <div className="w-48 mx-auto pt-6 border-b-2 text-center text-2xl text-blue-700">Services</div>
          <div className="p-2 text-center text-lg text-gray-700">This application is a recommendation engine that choose your next book based on the Halpreads database - ie I liked Verity. What should I read next? It will also generate books reviews for you.</div>
          
          <div className="max-w-screen-lg mx-auto">

          <div className='flex justify-center'>

              <div className="w-1/2 items-center p-10">
                <div className="relative w-50 h-64 m-5 bg-white shadow-lg rounded-md">
                  <p className="mx-2 py-2 border-b-2 text-center text-gray-700 font-semibold uppercase">RECOMMENDATION ENGINE</p>
                  <p className="p-2 text-sm text-gray-700">Looking for your next book? Use this recommendation Engine to find it!</p>
                  <p className="p-2 text-sm text-gray-700">Input a book that you recently enjoyed. Then, the engine will check for something similar in the @halpreads database</p>
                  <button className="rounded-full bg-black text-white">click here</button>
                </div>
              </div>

              <div className="w-1/2 items-center p-10">
                <div className="relative w-50 h-64 m-5 bg-white shadow-lg rounded-md">
                  <p className="mx-2 py-2 border-b-2 text-center text-gray-700 font-semibold uppercase">REVIEW GENERATOR</p>
                   <p className="p-2 text-sm text-gray-700">Input the title & author a book to generate a book review.</p>
                   <button className="rounded-full bg-black text-white" onClick={navtoGR}>click here
                   </button>
              </div>
              </div>

              </div>

              </div>

        </div>
      
    )
}

export default Home;