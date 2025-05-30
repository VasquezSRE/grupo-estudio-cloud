from flask import Flask
import requests
import random

app = Flask(__name__)

def get_instance_ip():
    try:
        return requests.get("http://169.254.169.254/latest/meta-data/public-ipv4", timeout=2).text
    except:
        return "Unavailable"

COLORS = ["#FFCDD2", "#F8BBD0", "#E1BEE7", "#BBDEFB", "#B2EBF2", "#C8E6C9", "#FFF9C4", "#D7CCC8"]

@app.route('/')
def home():
    ip = get_instance_ip()
    color = random.choice(COLORS)
    return f"""
    <html>
        <body style="background-color:{color}; text-align:center; padding-top:50px;">
            <h1>Hello from EC2 instance 🚀</h1>
            <h2>Public IP: {ip}</h2>
            <p>This page is served from a Flask app running on EC2, behind a Load Balancer.</p>
        </body>
    </html>
    """
