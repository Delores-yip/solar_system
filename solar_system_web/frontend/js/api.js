/**
 * API Client for Solar System Backend
 * Handles HTTP requests and WebSocket communication.
 */

class SolarSystemAPI {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
        this.socket = null;
        this.onPositionUpdate = null;
        this.onInitialState = null;
        this.onConnectionChange = null;
    }

    // REST API Methods

    async fetchBodies() {
        try {
            const response = await fetch(`${this.baseURL}/api/bodies`);
            if (!response.ok) throw new Error('Failed to fetch bodies');
            return await response.json();
        } catch (error) {
            console.error('Error fetching bodies:', error);
            throw error;
        }
    }

    async fetchBodyInfo(name) {
        try {
            const response = await fetch(`${this.baseURL}/api/body/${encodeURIComponent(name)}`);
            if (!response.ok) throw new Error('Failed to fetch body info');
            return await response.json();
        } catch (error) {
            console.error('Error fetching body info:', error);
            throw error;
        }
    }

    async fetchRelationship(body1, body2) {
        try {
            const response = await fetch(
                `${this.baseURL}/api/relationship/${encodeURIComponent(body1)}/${encodeURIComponent(body2)}`
            );
            if (!response.ok) throw new Error('Failed to fetch relationship');
            return await response.json();
        } catch (error) {
            console.error('Error fetching relationship:', error);
            throw error;
        }
    }

    async togglePause() {
        try {
            const response = await fetch(`${this.baseURL}/api/simulation/pause`, {
                method: 'POST'
            });
            if (!response.ok) throw new Error('Failed to toggle pause');
            return await response.json();
        } catch (error) {
            console.error('Error toggling pause:', error);
            throw error;
        }
    }

    async resetSimulation() {
        try {
            const response = await fetch(`${this.baseURL}/api/simulation/reset`, {
                method: 'POST'
            });
            if (!response.ok) throw new Error('Failed to reset simulation');
            return await response.json();
        } catch (error) {
            console.error('Error resetting simulation:', error);
            throw error;
        }
    }

    async getSimulationState() {
        try {
            const response = await fetch(`${this.baseURL}/api/simulation/state`);
            if (!response.ok) throw new Error('Failed to fetch simulation state');
            return await response.json();
        } catch (error) {
            console.error('Error fetching simulation state:', error);
            throw error;
        }
    }

    async setSpeed(speed) {
        try {
            const response = await fetch(`${this.baseURL}/api/simulation/speed`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ speed })
            });
            if (!response.ok) throw new Error('Failed to set speed');
            return await response.json();
        } catch (error) {
            console.error('Error setting speed:', error);
            throw error;
        }
    }

    // WebSocket Methods

    connectWebSocket() {
        console.log('Connecting to WebSocket...');
        
        this.socket = io(this.baseURL);

        this.socket.on('connect', () => {
            console.log('WebSocket connected');
            if (this.onConnectionChange) {
                this.onConnectionChange(true);
            }
        });

        this.socket.on('disconnect', () => {
            console.log('WebSocket disconnected');
            if (this.onConnectionChange) {
                this.onConnectionChange(false);
            }
        });

        this.socket.on('initial_state', (data) => {
            console.log('Received initial state');
            if (this.onInitialState) {
                this.onInitialState(data);
            }
        });

        this.socket.on('position_update', (data) => {
            if (this.onPositionUpdate) {
                this.onPositionUpdate(data);
            }
        });

        this.socket.on('connect_error', (error) => {
            console.error('WebSocket connection error:', error);
            if (this.onConnectionChange) {
                this.onConnectionChange(false);
            }
        });
    }

    disconnectWebSocket() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
    }

    requestUpdate() {
        if (this.socket && this.socket.connected) {
            this.socket.emit('request_update');
        }
    }

    setPositionUpdateCallback(callback) {
        this.onPositionUpdate = callback;
    }

    setInitialStateCallback(callback) {
        this.onInitialState = callback;
    }

    setConnectionChangeCallback(callback) {
        this.onConnectionChange = callback;
    }
}
