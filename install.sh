#!/bin/bash

echo "🚀 Installing DeepRecon dependencies on Linux/Kali..."

# Update system and install Tor
sudo apt update
sudo apt install -y python3 python3-pip tor

# Install Python requirements
pip3 install -r requirements.txt

# Enable and start Tor service
sudo systemctl enable tor
sudo systemctl start tor

# Check Tor status
echo "✅ Tor status:"
systemctl status tor | grep Active

echo "✅ Installation complete!"
echo "Run the tool with: python3 main.py"
