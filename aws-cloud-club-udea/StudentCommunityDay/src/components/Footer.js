import React from 'react';
import { Link } from 'react-scroll';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-logo">
            <img src="/logo.png" alt="AWS Cloud Club Logo" />
            <h3>AWS Student Community Day</h3>
            <p>A one-day conference organized by AWS Cloud Club</p>
          </div>
          
          <div className="footer-links">
            <h4>Quick Links</h4>
            <ul>
              <li>
                <Link to="hero" spy={true} smooth={true} offset={-80} duration={500}>
                  Home
                </Link>
              </li>
              <li>
                <Link to="about" spy={true} smooth={true} offset={-80} duration={500}>
                  About
                </Link>
              </li>
              <li>
                <Link to="tracks" spy={true} smooth={true} offset={-80} duration={500}>
                  Tracks
                </Link>
              </li>
              <li>
                <Link to="speakers" spy={true} smooth={true} offset={-80} duration={500}>
                  Speakers
                </Link>
              </li>
              <li>
                <Link to="sponsors" spy={true} smooth={true} offset={-80} duration={500}>
                  Sponsors
                </Link>
              </li>
              <li>
                <Link to="location" spy={true} smooth={true} offset={-80} duration={500}>
                  Location
                </Link>
              </li>
            </ul>
          </div>
          
          <div className="footer-contact">
            <h4>Contact Us</h4>
            <p>
              <i className="fas fa-envelope"></i>
              <a href="mailto:cloudclub@university.edu">cloudclub@university.edu</a>
            </p>
            <p>
              <i className="fas fa-phone"></i>
              <a href="tel:+1234567890">(123) 456-7890</a>
            </p>
            <div className="social-links">
              <a href="https://twitter.com/" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="https://facebook.com/" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="https://instagram.com/" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-instagram"></i>
              </a>
              <a href="https://linkedin.com/" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-linkedin-in"></i>
              </a>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} AWS Cloud Club. All rights reserved.</p>
          <p>
            <a href="#privacy">Privacy Policy</a> | 
            <a href="#terms">Terms of Service</a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;