import React, { useState, useEffect } from 'react';
import { Link } from 'react-scroll';
import './Header.css';

const Header = () => {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <header className={`header ${scrolled ? 'scrolled' : ''}`}>
      <div className="container header-container">
        <div className="logo">
          <img src="/logo.png" alt="AWS Cloud Club Logo" />
          <span>AWS Student Community Day</span>
        </div>
        
        <div className={`menu-toggle ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
          <span></span>
          <span></span>
          <span></span>
        </div>
        
        <nav className={`nav ${menuOpen ? 'active' : ''}`}>
          <ul>
            <li>
              <Link to="hero" spy={true} smooth={true} offset={-80} duration={500} onClick={() => setMenuOpen(false)}>
                Home
              </Link>
            </li>
            <li>
              <Link to="about" spy={true} smooth={true} offset={-80} duration={500} onClick={() => setMenuOpen(false)}>
                About
              </Link>
            </li>
            <li>
              <Link to="tracks" spy={true} smooth={true} offset={-80} duration={500} onClick={() => setMenuOpen(false)}>
                Tracks
              </Link>
            </li>
            <li>
              <Link to="speakers" spy={true} smooth={true} offset={-80} duration={500} onClick={() => setMenuOpen(false)}>
                Speakers
              </Link>
            </li>
            <li>
              <Link to="sponsors" spy={true} smooth={true} offset={-80} duration={500} onClick={() => setMenuOpen(false)}>
                Sponsors
              </Link>
            </li>
            <li>
              <Link to="location" spy={true} smooth={true} offset={-80} duration={500} onClick={() => setMenuOpen(false)}>
                Location
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;