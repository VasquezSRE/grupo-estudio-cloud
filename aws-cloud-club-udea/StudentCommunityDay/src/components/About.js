import React from 'react';
import './About.css';

const About = () => {
  return (
    <section id="about" className="about section-light">
      <div className="container">
        <h2 className="section-title text-center">About Student Community Day</h2>
        <div className="about-content">
          <div className="about-text">
            <p>
              AWS Student Community Days (SCD) are one-day, community-led conferences where event logistics and content are planned, sourced, and delivered by student community leaders with minimal guidance from AWS.
            </p>
            <p>
              SCDs are the culminating experience of an AWS Cloud Club Captain, similar to how a student wraps up their academic degree with a senior thesis or capstone project. While a standard Cloud Club event focuses on one topic, a Student Community Day features 3+ topics, sessions, and speakers to gather, educate, and celebrate with a wider array of audiences.
            </p>
            <p>
              Join us for a day filled with technical workshops, inspiring keynotes, networking opportunities, and hands-on experiences with AWS technologies. Whether you're a beginner or an experienced cloud practitioner, there's something for everyone!
            </p>
          </div>
          <div className="about-features">
            <div className="feature">
              <div className="feature-icon">
                <i className="fas fa-users"></i>
              </div>
              <h3>Community-Led</h3>
              <p>Organized by students for students</p>
            </div>
            <div className="feature">
              <div className="feature-icon">
                <i className="fas fa-laptop-code"></i>
              </div>
              <h3>Hands-On Learning</h3>
              <p>Interactive workshops and labs</p>
            </div>
            <div className="feature">
              <div className="feature-icon">
                <i className="fas fa-network-wired"></i>
              </div>
              <h3>Networking</h3>
              <p>Connect with peers and industry experts</p>
            </div>
            <div className="feature">
              <div className="feature-icon">
                <i className="fas fa-certificate"></i>
              </div>
              <h3>Career Growth</h3>
              <p>Enhance your cloud skills and resume</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;