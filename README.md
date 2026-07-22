requirements:

paho-mqtt







exec start\_network.bat to start the network, activating the Docker and all members.



Its been used mosquitto as a broker initially, it will be replaced by HiveMQ later.



For new machines at the network:

python -m venv .venv
.venv\\Scripts\\activate.bat
pip install -r requirements.txt

