import React from 'react';
import './Speakers.css';

const Speakers = () => {
  const speakers = [
    {
      id: 1,
      name: "Jane Smith",
      title: "AWS Community Builder",
      bio: "Jane is an AWS Community Builder with expertise in cloud architecture and serverless technologies.",
      image: "https://randomuser.me/api/portraits/women/44.jpg",
      linkedin: "https://linkedin.com/in/",
      github: "https://github.com/"
    },
    {
      id: 2,
      name: "John Doe",
      title: "Solutions Architect",
      bio: "John is a Solutions Architect with over 5 years of experience building cloud-native applications.",
      image: "https://randomuser.me/api/portraits/men/32.jpg",
      linkedin: "https://linkedin.com/in/",
      github: "https://github.com/"
    },
    {
      id: 3,
      name: "Alex Johnson",
      title: "Cloud Security Specialist",
      bio: "Alex specializes in cloud security and compliance, helping organizations secure their AWS environments.",
      image: "https://randomuser.me/api/portraits/women/68.jpg",
      linkedin: "https://linkedin.com/in/",
      github: "https://github.com/"
    },
    {
      id: 4,
      name: "Michael Brown",
      title: "DevOps Engineer",
      bio: "Michael is passionate about automation and has extensive experience with CI/CD pipelines.",
      image: "https://randomuser.me/api/portraits/men/75.jpg",
      linkedin: "https://linkedin.com/in/",
      github: "https://github.com/"
    },
    {
      id: 5,
      name: "Sarah Wilson",
      title: "AWS Certified Trainer",
      bio: "Sarah is an AWS Certified Trainer who loves teaching cloud concepts to beginners.",
      image: "https://randomuser.me/api/portraits/women/22.jpg",
      linkedin: "https://linkedin.com/in/",
      github: "https://github.com/"
    },
    {
      id: 6,
      name: "David Lee",
      title: "Container Specialist",
      bio: "David is an expert in containerization technologies and Kubernetes orchestration.",
      image: "https://randomuser.me/api/portraits/men/41.jpg",
      linkedin: "https://linkedin.com/in/",
      github: "https://github.com/"
    }
  ];

  return (
    <section id="speakers" className="speakers section-light">
      <div className="container">
        <h2 className="section-title text-center">Our Speakers</h2>
        <div className="speakers-grid">
          {speakers.map(speaker => (
            <div key={speaker.id} className="speaker-card">
              <div className="speaker-image">
                <img src={speaker.image} alt={speaker.name} />
              </div>
              <div className="speaker-info">
                <h3>{speaker.name}</h3>
                <h4>{speaker.title}</h4>
                <p>{speaker.bio}</p>
                <div className="speaker-social">
                  <a href={speaker.linkedin} target="_blank" rel="noopener noreferrer" className="social-link linkedin">
                    <i className="fab fa-linkedin"></i>
                  </a>
                  <a href={speaker.github} target="_blank" rel="noopener noreferrer" className="social-link github">
                    <i className="fab fa-github"></i>
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Speakers;