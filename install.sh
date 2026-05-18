#!/bin/bash

set -euo pipefail

echo "Installing DeepRecon dependencies on Linux/Kali..."

sudo apt update
sudo apt install -y python3 python3-pip python3-venv tor

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if command -v systemctl >/dev/null 2>&1; then
	sudo systemctl enable tor || true
	sudo systemctl restart tor || true
fi

echo "Creating global 'deeprecon' command alias..."
echo '#!/bin/bash' | sudo tee /usr/local/bin/deeprecon > /dev/null
echo "python3 $(pwd)/main.py \"\$@\"" | sudo tee -a /usr/local/bin/deeprecon > /dev/null
sudo chmod +x /usr/local/bin/deeprecon

echo "Installation complete. You can now use the 'deeprecon' command anywhere!"
echo "Try: deeprecon --cli OR deeprecon --web"
