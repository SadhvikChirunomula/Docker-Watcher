from flask import Flask, render_template
import docker

app = Flask(__name__)
client = docker.from_env()


def get_container_stats(container):
    if container.status == 'running':
        stats = container.stats(stream=False)
        health = container.attrs.get('State', {}).get('Health', {}).get('Status', 'N/A')
        cpu_usage = round(stats['cpu_stats']['cpu_usage']['total_usage'] / (stats['cpu_stats']['online_cpus'] * 10 ** 9) * 100, 2)
        memory_usage = round(stats['memory_stats']['usage'] / (1024 * 1024), 2)
        network_rx = round(stats['networks']['eth0']['rx_bytes'] / (1024 * 1024), 2)
        network_tx = round(stats['networks']['eth0']['tx_bytes'] / (1024 * 1024), 2)
    else:
        stats = None
        health = 'N/A'
        cpu_usage = 'N/A'
        memory_usage = 'N/A'
        network_rx = 'N/A'
        network_tx = 'N/A'

    return {
        'id': container.short_id,
        'name': container.name,
        'image': container.image.tags[0] if container.image.tags else 'N/A',
        'status': container.status,
        'health': health,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'network_rx': network_rx,
        'network_tx': network_tx
    }



@app.route('/')
def containers():
    containers = client.containers.list(all=True)
    container_stats = [get_container_stats(container) for container in containers]
    return render_template('containers.html', containers=container_stats)


if __name__ == '__main__':
    app.run(debug=True)
