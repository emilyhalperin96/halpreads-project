import React from 'react';
import ReactDOM from 'react-dom/client';
import {BrowserRouter} from 'react-router-dom';
import './index.css';
import App from './App';
//import {createStore} from 'redux';
//import allReducer from './reducers'
//import {Provider} from 'react-redux'

//const store = createStore(allReducer);

//then wrap the app in Provider store={store}
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
        <App />
      </BrowserRouter>
  </React.StrictMode>
);