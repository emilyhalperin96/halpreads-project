import React from 'react';

const About = ({user, setUser}) => {

    function handleLogoutClick() {
        fetch("/logout", { method: "DELETE" }).then((r) => {
          if (r.ok) {
            setUser(null);
          }
        });
      }
    return (
        <div className= 'flex justify-between items-center h-20 max-w-[1240] mx-auto px-4 bg-[#f6e1e7]'>
            <h1 className='w-full text-3xl font-bold text-black'>Halpreads</h1>
            <ul className='list-none flex'>
                <li className='p-4'>About</li>
                <li className='p-4'>Contact</li>
            </ul>
            <button onClick={handleLogoutClick}>Logout</button>
        </div>
    )
}

export default About;