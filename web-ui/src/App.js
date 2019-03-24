import React, { Component } from 'react';
import './App.css';
import { Link, Route } from 'react-router-dom';

import GraphUI from './components/GraphUI';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Route exact path="/" component={GraphUI}/>
      </div>
    );
  }
}

export default App;
