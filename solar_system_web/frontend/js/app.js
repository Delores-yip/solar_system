/**
 * Main Application Logic
 * Coordinates scene, API, and user interactions.
 */

class App {
    constructor() {
        this.api = new SolarSystemAPI();
        this.scene = new SolarSystemScene('scene-canvas');
        this.selectedBodies = [];
        this.isPaused = false;
        this.currentSpeed = 1.0;
        
        // UI elements
        this.pauseBtn = document.getElementById('pause-btn');
        this.pauseIcon = document.getElementById('pause-icon');
        this.pauseText = document.getElementById('pause-text');
        this.resetBtn = document.getElementById('reset-btn');
        this.speedSlider = document.getElementById('speed-slider');
        this.speedValue = document.getElementById('speed-value');
        this.timeValue = document.getElementById('time-value');
        this.infoTitle = document.getElementById('info-title');
        this.infoContent = document.getElementById('info-content');
        this.closeInfoBtn = document.getElementById('close-info-btn');
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.connectionStatus = document.getElementById('connection-status');
        this.statusIndicator = document.getElementById('status-indicator');
        this.statusText = document.getElementById('status-text');
    }

    async initialize() {
        console.log('Initializing application...');

        // Initialize scene
        this.scene.initialize();

        // Setup callbacks
        this.setupCallbacks();

        // Setup event listeners
        this.setupEventListeners();

        try {
            // Fetch initial bodies data
            const bodies = await this.api.fetchBodies();
            console.log('Fetched bodies:', Object.keys(bodies));

            // Create 3D bodies in scene
            this.scene.createBodies(bodies);

            // Connect to WebSocket
            this.api.connectWebSocket();

            // Start animation loop
            this.scene.animate();

            // Hide loading overlay
            setTimeout(() => {
                this.loadingOverlay.style.display = 'none';
            }, 500);

            console.log('Application initialized successfully');
        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.showError('Failed to connect to server. Please make sure the backend is running.');
        }
    }

    setupCallbacks() {
        // WebSocket callbacks
        this.api.setPositionUpdateCallback((data) => {
            this.scene.updatePositions(data.positions);
            this.timeValue.textContent = data.time.toFixed(2);
        });

        this.api.setInitialStateCallback((data) => {
            console.log('Initial state received');
            this.scene.updatePositions(data.state.positions);
            this.isPaused = data.state.paused;
            this.updatePauseButton();
        });

        this.api.setConnectionChangeCallback((connected) => {
            if (connected) {
                this.connectionStatus.classList.remove('disconnected');
                this.connectionStatus.classList.add('connected');
                this.statusText.textContent = 'Connected';
            } else {
                this.connectionStatus.classList.remove('connected');
                this.connectionStatus.classList.add('disconnected');
                this.statusText.textContent = 'Disconnected';
            }
        });

        // Scene click callback
        this.scene.setBodyClickCallback((bodyName, isShiftClick) => {
            this.handleBodyClick(bodyName, isShiftClick);
        });
    }

    setupEventListeners() {
        // Pause button
        this.pauseBtn.addEventListener('click', () => {
            this.handlePauseToggle();
        });

        // Reset button
        this.resetBtn.addEventListener('click', () => {
            this.handleReset();
        });

        // Speed slider
        this.speedSlider.addEventListener('input', (e) => {
            const speed = parseFloat(e.target.value);
            this.handleSpeedChange(speed);
        });

        // Close info button
        this.closeInfoBtn.addEventListener('click', () => {
            this.clearSelection();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'p' || e.key === 'P') {
                this.handlePauseToggle();
            } else if (e.key === 'c' || e.key === 'C') {
                this.clearSelection();
            } else if (e.key === 'r' || e.key === 'R') {
                this.handleReset();
            }
        });
    }

    async handleBodyClick(bodyName, isShiftClick) {
        if (isShiftClick) {
            // Selection mode for comparison
            this.handleSelection(bodyName);
        } else {
            // Show info mode
            this.clearSelection();
            await this.showBodyInfo(bodyName);
        }
    }

    async handleSelection(bodyName) {
        const index = this.selectedBodies.indexOf(bodyName);
        
        if (index !== -1) {
            // Deselect if already selected
            this.selectedBodies.splice(index, 1);
            this.scene.removeHighlight(bodyName);
        } else {
            // Add to selection
            if (this.selectedBodies.length >= 2) {
                // Remove oldest selection
                const oldBody = this.selectedBodies.shift();
                this.scene.removeHighlight(oldBody);
            }
            
            this.selectedBodies.push(bodyName);
            this.scene.highlightBody(bodyName, 0x00ff00);
        }

        // If two bodies selected, show relationship
        if (this.selectedBodies.length === 2) {
            await this.showRelationship(this.selectedBodies[0], this.selectedBodies[1]);
        } else if (this.selectedBodies.length === 1) {
            this.updateInfoPanel(
                'Selection Mode',
                `<p><strong>${this.selectedBodies[0]}</strong> selected.</p>
                 <p>Hold <strong>Shift</strong> and click another planet to see their relationship.</p>`
            );
        } else {
            this.resetInfoPanel();
        }
    }

    async showBodyInfo(bodyName) {
        try {
            const info = await this.api.fetchBodyInfo(bodyName);
            
            this.updateInfoPanel(
                bodyName,
                `<p>${info.info}</p>
                 <div class="body-stats">
                     <p><strong>Radius:</strong> ${info.data.radius} units</p>
                     <p><strong>Orbital Radius:</strong> ${info.data.orbital_radius} units</p>
                     <p><strong>Orbital Period:</strong> ${info.data.orbital_period} days</p>
                 </div>`
            );

            // Highlight the body
            this.scene.clearAllHighlights();
            this.scene.highlightBody(bodyName, 0x00ffff);
        } catch (error) {
            console.error('Error showing body info:', error);
        }
    }

    async showRelationship(body1, body2) {
        try {
            const rel = await this.api.fetchRelationship(body1, body2);
            
            this.updateInfoPanel(
                `${body1} & ${body2}`,
                `<p>${rel.relationship}</p>
                 <p><strong>Current Distance:</strong> ${rel.current_distance} units</p>`
            );
        } catch (error) {
            console.error('Error showing relationship:', error);
        }
    }

    async handlePauseToggle() {
        try {
            const result = await this.api.togglePause();
            this.isPaused = result.paused;
            this.updatePauseButton();
        } catch (error) {
            console.error('Error toggling pause:', error);
        }
    }

    async handleReset() {
        try {
            await this.api.resetSimulation();
            this.clearSelection();
            this.timeValue.textContent = '0.00';
        } catch (error) {
            console.error('Error resetting simulation:', error);
        }
    }

    async handleSpeedChange(speed) {
        this.currentSpeed = speed;
        this.speedValue.textContent = `${speed.toFixed(1)}x`;
        
        try {
            await this.api.setSpeed(speed);
        } catch (error) {
            console.error('Error setting speed:', error);
        }
    }

    updatePauseButton() {
        if (this.isPaused) {
            this.pauseIcon.textContent = '▶';
            this.pauseText.textContent = 'Play';
            this.pauseBtn.classList.add('paused');
        } else {
            this.pauseIcon.textContent = '⏸';
            this.pauseText.textContent = 'Pause';
            this.pauseBtn.classList.remove('paused');
        }
    }

    updateInfoPanel(title, content) {
        this.infoTitle.textContent = title;
        this.infoContent.innerHTML = content;
        this.closeInfoBtn.style.display = 'block';
    }

    resetInfoPanel() {
        this.infoTitle.textContent = 'Solar System Simulation';
        this.infoContent.innerHTML = `
            <p>Click on any planet to learn more about it.</p>
            <p>Hold <strong>Shift</strong> and click two planets to see their relationship.</p>
            <p>Use mouse to rotate the camera.</p>
        `;
        this.closeInfoBtn.style.display = 'none';
    }

    clearSelection() {
        this.selectedBodies = [];
        this.scene.clearAllHighlights();
        this.resetInfoPanel();
    }

    showError(message) {
        this.loadingOverlay.innerHTML = `
            <div style="color: #ff4444;">
                <h2>Error</h2>
                <p>${message}</p>
            </div>
        `;
    }
}

// Initialize application when page loads
window.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    app.initialize();
});
