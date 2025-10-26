"""
Flask API Server for Solar System Simulation
Provides REST endpoints and WebSocket for real-time updates.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time
from threading import Thread, Lock

from data import SolarSystemData
from simulation import OrbitSimulator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

# Global simulation instance
simulator = OrbitSimulator()
data_manager = SolarSystemData()
simulation_lock = Lock()

# WebSocket update thread control
update_thread = None
update_running = False


def background_update_loop():
    """Background thread that continuously updates and broadcasts positions."""
    global update_running
    
    while update_running:
        with simulation_lock:
            positions = simulator.update()
        
        # Broadcast to all connected clients
        socketio.emit('position_update', {
            'positions': positions,
            'time': simulator.time,
            'paused': simulator.paused
        })
        
        # Sleep to maintain ~60 FPS
        time.sleep(0.016)


@app.route('/api/bodies', methods=['GET'])
def get_bodies():
    """Get all celestial bodies with their data."""
    with simulation_lock:
        bodies = data_manager.get_all_bodies()
        positions = simulator.get_all_positions()
    
    # Merge position data into bodies
    result = {}
    for name, data in bodies.items():
        result[name] = {
            **data,
            'current_position': positions[name]
        }
    
    return jsonify(result)


@app.route('/api/body/<name>', methods=['GET'])
def get_body(name):
    """Get information about a specific body."""
    body_info = data_manager.get_body_info(name)
    
    if body_info:
        with simulation_lock:
            body_info['current_position'] = simulator.calculate_position(name)
        return jsonify(body_info)
    else:
        return jsonify({'error': 'Body not found'}), 404


@app.route('/api/relationship/<body1>/<body2>', methods=['GET'])
def get_relationship(body1, body2):
    """Get relationship information between two bodies."""
    relationship_text = data_manager.get_relationship(body1, body2)
    
    if relationship_text:
        with simulation_lock:
            positions = simulator.get_all_positions()
        
        distance = data_manager.calculate_distance(body1, body2, positions)
        
        return jsonify({
            'body1': body1,
            'body2': body2,
            'relationship': relationship_text,
            'current_distance': distance
        })
    else:
        return jsonify({
            'body1': body1,
            'body2': body2,
            'relationship': 'No specific relationship documented.',
            'current_distance': None
        })


@app.route('/api/simulation/pause', methods=['POST'])
def toggle_pause():
    """Toggle simulation pause state."""
    with simulation_lock:
        paused = simulator.toggle_pause()
    
    return jsonify({
        'paused': paused,
        'time': simulator.time
    })


@app.route('/api/simulation/reset', methods=['POST'])
def reset_simulation():
    """Reset simulation to initial state."""
    with simulation_lock:
        positions = simulator.reset()
    
    return jsonify({
        'message': 'Simulation reset',
        'time': simulator.time,
        'positions': positions
    })


@app.route('/api/simulation/state', methods=['GET'])
def get_simulation_state():
    """Get current simulation state."""
    with simulation_lock:
        state = simulator.get_state()
    
    return jsonify(state)


@app.route('/api/simulation/speed', methods=['POST'])
def set_speed():
    """Set simulation speed multiplier."""
    data = request.get_json()
    speed = data.get('speed', 1.0)
    
    with simulation_lock:
        new_speed = simulator.set_time_scale(speed)
    
    return jsonify({
        'speed': new_speed
    })


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    global update_thread, update_running
    
    print('Client connected')
    
    # Start update thread if not running
    if not update_running:
        update_running = True
        update_thread = Thread(target=background_update_loop)
        update_thread.daemon = True
        update_thread.start()
    
    # Send initial state
    with simulation_lock:
        state = simulator.get_state()
    
    emit('initial_state', {
        'bodies': data_manager.get_all_bodies(),
        'state': state
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print('Client disconnected')


@socketio.on('request_update')
def handle_update_request():
    """Handle manual update request from client."""
    with simulation_lock:
        positions = simulator.get_all_positions()
    
    emit('position_update', {
        'positions': positions,
        'time': simulator.time,
        'paused': simulator.paused
    })


if __name__ == '__main__':
    print("Starting Solar System API Server...")
    print("API available at: http://localhost:5000")
    print("WebSocket available at: ws://localhost:5000")
    print("Using threading mode with polling transport")
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, use_reloader=False)
