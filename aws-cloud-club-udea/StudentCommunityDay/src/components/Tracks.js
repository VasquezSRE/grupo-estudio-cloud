import React, { useState } from 'react';
import './Tracks.css';

const Tracks = () => {
  const [activeTrack, setActiveTrack] = useState(1);

  const tracks = [
    {
      id: 1,
      title: "Cloud Fundamentals",
      description: "Perfect for beginners looking to start their cloud journey",
      color: "var(--aws-blue)",
      sessions: [
        {
          time: "9:00 AM - 10:30 AM",
          title: "Introduction to AWS Cloud",
          speaker: "Jane Smith",
          description: "Learn the basics of AWS cloud services and how they can be used to build scalable applications."
        },
        {
          time: "11:00 AM - 12:30 PM",
          title: "Getting Started with EC2 and S3",
          speaker: "John Doe",
          description: "Hands-on workshop on launching your first EC2 instance and storing data in S3 buckets."
        },
        {
          time: "2:00 PM - 3:30 PM",
          title: "Cloud Security Fundamentals",
          speaker: "Alex Johnson",
          description: "Understanding the shared responsibility model and implementing basic security practices."
        }
      ]
    },
    {
      id: 2,
      title: "DevOps & Automation",
      description: "For those interested in CI/CD pipelines and infrastructure as code",
      color: "var(--aws-orange)",
      sessions: [
        {
          time: "9:00 AM - 10:30 AM",
          title: "CI/CD with AWS CodePipeline",
          speaker: "Michael Brown",
          description: "Build and deploy applications automatically with AWS CodePipeline."
        },
        {
          time: "11:00 AM - 12:30 PM",
          title: "Infrastructure as Code with CloudFormation",
          speaker: "Sarah Wilson",
          description: "Learn how to define your infrastructure using CloudFormation templates."
        },
        {
          time: "2:00 PM - 3:30 PM",
          title: "Containerization with ECS and EKS",
          speaker: "David Lee",
          description: "Deploy and manage containerized applications using Amazon ECS and EKS."
        }
      ]
    },
    {
      id: 3,
      title: "AI & Machine Learning",
      description: "Explore the world of AI/ML services on AWS",
      color: "var(--aws-purple-light)",
      sessions: [
        {
          time: "9:00 AM - 10:30 AM",
          title: "Introduction to Amazon SageMaker",
          speaker: "Emily Chen",
          description: "Build, train, and deploy machine learning models at scale with Amazon SageMaker."
        },
        {
          time: "11:00 AM - 12:30 PM",
          title: "Natural Language Processing with Amazon Comprehend",
          speaker: "Robert Taylor",
          description: "Extract insights from text using Amazon Comprehend's NLP capabilities."
        },
        {
          time: "2:00 PM - 3:30 PM",
          title: "Building AI-Powered Applications",
          speaker: "Lisa Garcia",
          description: "Integrate AI services into your applications to create intelligent experiences."
        }
      ]
    }
  ];

  return (
    <section id="tracks" className="tracks section-gradient">
      <div className="container">
        <h2 className="section-title text-center">Event Tracks</h2>
        <div className="track-tabs">
          {tracks.map(track => (
            <div 
              key={track.id}
              className={`track-tab ${activeTrack === track.id ? 'active' : ''}`}
              onClick={() => setActiveTrack(track.id)}
              style={{borderColor: activeTrack === track.id ? track.color : 'transparent'}}
            >
              <h3>{track.title}</h3>
              <p>{track.description}</p>
            </div>
          ))}
        </div>
        
        <div className="track-content">
          {tracks.map(track => (
            <div 
              key={track.id} 
              className={`track-schedule ${activeTrack === track.id ? 'active' : ''}`}
            >
              <h3 className="track-title" style={{color: track.color}}>
                {track.title} Schedule - Room {track.id}
              </h3>
              <div className="sessions">
                {track.sessions.map((session, index) => (
                  <div key={index} className="session">
                    <div className="session-time">{session.time}</div>
                    <div className="session-details">
                      <h4>{session.title}</h4>
                      <p className="session-speaker">Speaker: {session.speaker}</p>
                      <p className="session-description">{session.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Tracks;