from flask import Flask, render_template, Response, abort
import docker
import os

app = Flask(__name__)
client = docker.from_env()

HOST = os.getenv('DOCKER_WATCHER_HOST', 'localhost')
PORT = os.getenv('DOCKER_WATCHER_PORT', '5000')


def get_container_stats(container):
    if container.status == 'running':
        stats = container.stats(stream=False)
        health = container.attrs.get('State', {}).get('Health', {}).get('Status', 'N/A')
        cpu_usage = round(stats['cpu_stats']['cpu_usage']['total_usage'] / (stats['cpu_stats']['online_cpus'] * 10 ** 9) * 100, 2)
        memory_usage = round(stats['memory_stats']['usage'] / (1024 * 1024), 2)
    else:
        stats = None
        health = 'N/A'
        cpu_usage = 'N/A'
        memory_usage = 'N/A'

    return {
        'id': container.short_id,
        'name': container.name,
        'image': container.image.tags[0] if container.image.tags else 'N/A',
        'status': container.status,
        'health': health,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
    }


@app.route('/')
def containers():
    containers = client.containers.list(all=True)
    container_stats = [get_container_stats(container) for container in containers]
    return render_template('containers.html', containers=container_stats)


@app.route('/logs/<container_id>')
def logs(container_id):
    try:
        container = client.containers.get(container_id)
        container_logs = container.logs().decode("utf-8")
        container_name = container.name
        return render_template('log_view.html', logs=container_logs, container_name=container_name, container_id=container_id)
    except docker.errors.NotFound:
        abort(404)

@app.route('/logs/<container_id>/text')
def logs_text(container_id):
    container = client.containers.get(container_id)
    logs = container.logs().decode('utf-8')
    return Response(logs, mimetype='text/plain')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
