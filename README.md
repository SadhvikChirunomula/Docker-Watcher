# Docker-Watcher

Docker-Watcher is a web-based application that provides real-time monitoring of Docker containers running on a local or remote machine. The application displays various metrics such as CPU and memory usage, network activity, and container health status.

## Features

* Displays a table of all Docker containers with their current status and metrics
* Updates metrics in real-time without requiring page refresh
* Provides color-coded status badges and container color blocks for easy identification of running and stopped containers
* Includes a responsive design that works on desktop and mobile devices

## Installation

To use Docker-Watcher, you need to have Docker installed on your local or remote machine.

1. Clone the repository: `git clone https://github.com/SadhvikChirunomula/Docker-Watcher.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Open your web browser and navigate to [http://localhost:5000](http://localhost:5000)

# Usage

Once you have the application running, you can view the metrics for all Docker containers by navigating to http://localhost:5000 in your web browser. The table displays various metrics such as container ID, name, image, status, health, CPU usage, memory usage, network RX, and network TX.

# License

Docker-Watcher is licensed under the MIT License. See LICENSE for more information.

# Credits
Docker-Watcher was created by Sadhvik Chirunomula.