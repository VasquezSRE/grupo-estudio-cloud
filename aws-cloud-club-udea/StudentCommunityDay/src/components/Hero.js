import React from 'react';
import { Link } from 'react-scroll';
import './Hero.css';

const Hero = () => {
  return (
    <section id="hero" className="hero">
      <div className="hero-content">
        <h1>AWS Student Community Day</h1>
        <h2>June 15, 2024 • University Campus</h2>
        <p>Join us for a day of learning, networking, and innovation with AWS</p>
        <div className="hero-buttons">
          <Link to="about" spy={true} smooth={true} offset={-80} duration={500} className="btn btn-primary">
            Learn More
          </Link>
          <a href="#register" className="btn btn-secondary">
            Register Now
          </a>
        </div>
      </div>
      <div className="hero-overlay"></div>
    </section>
  );
};

export default Hero;