import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import About from './components/About';
import Tracks from './components/Tracks';
import Speakers from './components/Speakers';
import Sponsors from './components/Sponsors';
import Location from './components/Location';
import Footer from './components/Footer';
import './App.css';

function App() {
  return (
    <div className="App">
      <Header />
      <Hero />
      <About />
      <Tracks />
      <Speakers />
      <Sponsors />
      <Location />
      <Footer />
    </div>
  );
}

export default App;