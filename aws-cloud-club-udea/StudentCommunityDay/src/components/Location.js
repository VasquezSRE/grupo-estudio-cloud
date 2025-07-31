import React from 'react';
import './Location.css';

const Location = () => {
  return (
    <section id="location" className="location section-light">
      <div className="container">
        <h2 className="section-title text-center">Event Location</h2>
        <div className="location-container">
          <div className="location-info">
            <h3>University Campus</h3>
            <address>
              <p>Main Auditorium</p>
              <p>123 University Avenue</p>
              <p>City, State 12345</p>
            </address>
            <div className="location-details">
              <div className="detail">
                <h4>Date</h4>
                <p>June 15, 2024</p>
              </div>
              <div className="detail">
                <h4>Time</h4>
                <p>8:30 AM - 5:00 PM</p>
              </div>
            </div>
            <div className="location-directions">
              <h4>Getting There</h4>
              <div className="direction">
                <i className="fas fa-car"></i>
                <p>Parking available in Lot A and B</p>
              </div>
              <div className="direction">
                <i className="fas fa-bus"></i>
                <p>Bus routes 10, 15, and 22 stop nearby</p>
              </div>
              <div className="direction">
                <i className="fas fa-subway"></i>
                <p>Metro station: University Center (5 min walk)</p>
              </div>
            </div>
          </div>
          <div className="location-map">
            <iframe 
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.2219901290355!2d-74.00369368400567!3d40.71312937933185!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a23e28c1191%3A0x49f75d3281df052a!2s150%20Park%20Row%2C%20New%20York%2C%20NY%2010007%2C%20USA!5e0!3m2!1sen!2sus!4v1579814389985!5m2!1sen!2sus" 
              width="100%" 
              height="450" 
              style={{border:0}} 
              allowFullScreen="" 
              loading="lazy" 
              referrerPolicy="no-referrer-when-downgrade"
              title="Event Location"
            ></iframe>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Location;