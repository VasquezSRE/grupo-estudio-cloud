import React from 'react';
import './Sponsors.css';

const Sponsors = () => {
  const sponsorTiers = [
    {
      tier: "Platinum",
      sponsors: [
        {
          name: "AWS",
          logo: "https://d1.awsstatic.com/logos/aws-logo-lockups/poweredbyaws/PB_AWS_logo_RGB_stacked_REV_SQ.91cd4af40773cbfbd15577a3c2b8a346fe3e8fa2.png",
          website: "https://aws.amazon.com"
        }
      ]
    },
    {
      tier: "Gold",
      sponsors: [
        {
          name: "Tech Company 1",
          logo: "https://via.placeholder.com/200x100?text=Gold+Sponsor",
          website: "#"
        },
        {
          name: "Tech Company 2",
          logo: "https://via.placeholder.com/200x100?text=Gold+Sponsor",
          website: "#"
        }
      ]
    },
    {
      tier: "Silver",
      sponsors: [
        {
          name: "Tech Company 3",
          logo: "https://via.placeholder.com/150x75?text=Silver+Sponsor",
          website: "#"
        },
        {
          name: "Tech Company 4",
          logo: "https://via.placeholder.com/150x75?text=Silver+Sponsor",
          website: "#"
        },
        {
          name: "Tech Company 5",
          logo: "https://via.placeholder.com/150x75?text=Silver+Sponsor",
          website: "#"
        }
      ]
    }
  ];

  return (
    <section id="sponsors" className="sponsors section-dark">
      <div className="container">
        <h2 className="section-title text-center">Our Sponsors</h2>
        <p className="text-center sponsors-intro">
          We're grateful to the following organizations for supporting AWS Student Community Day.
        </p>
        
        {sponsorTiers.map((tier, index) => (
          <div key={index} className="sponsor-tier">
            <h3 className="tier-title">{tier.tier} Sponsors</h3>
            <div className={`sponsors-grid tier-${tier.tier.toLowerCase()}`}>
              {tier.sponsors.map((sponsor, idx) => (
                <a 
                  key={idx} 
                  href={sponsor.website} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="sponsor-card"
                >
                  <img src={sponsor.logo} alt={sponsor.name} />
                </a>
              ))}
            </div>
          </div>
        ))}
        
        <div className="become-sponsor">
          <h3>Become a Sponsor</h3>
          <p>
            Interested in sponsoring AWS Student Community Day? Reach out to us to learn about sponsorship opportunities.
          </p>
          <a href="#contact" className="btn">Contact Us</a>
        </div>
      </div>
    </section>
  );
};

export default Sponsors;