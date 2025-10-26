# To quick start the solar system simulation please read the QUICKSTART.md file

# Solar System Simulation - Web Application

A modern web-based solar system simulation with interactive 3D visualization, real-time orbital mechanics, and educational content about celestial bodies.

## Architecture

This application uses a **frontend-backend architecture**:

- **Backend**: Python Flask server with WebSocket support
- **Frontend**: HTML/CSS/JavaScript with Three.js for 3D rendering
- **Communication**: REST API + WebSocket for real-time position updates

## Project Structure

```
solar_system_web/
├── backend/
│   ├── app.py              # Flask server with REST API and WebSocket
│   ├── data.py             # Solar system data management
│   ├── simulation.py       # Orbital physics simulation engine
│   └── requirements.txt    # Python dependencies
│
└── frontend/
    ├── index.html          # Main HTML page
    ├── css/
    │   └── styles.css      # Application styles
    └── js/
        ├── api.js          # API client for backend communication
        ├── scene.js        # Three.js 3D scene management
        └── app.js          # Main application logic
```

## Features

### Interactive 3D Visualization
- Real-time 3D rendering of the solar system using Three.js
- Smooth orbital animations
- Interactive camera controls (rotate, zoom, pan)
- Visual selection indicators

### Educational Content
- Click any planet to view detailed information
- Compare two planets by Shift+clicking to see their relationship
- Real-time distance calculations between bodies

### Simulation Controls
- Play/Pause animation
- Adjustable simulation speed (0.1x to 100x)
- Reset to initial state
- Real-time time display

### Real-time Updates
- WebSocket connection for live position streaming
- ~60 FPS update rate
- Connection status indicator

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Modern web browser with WebGL support

### Backend Setup

1. Navigate to the backend directory:
```bash
cd solar_system_web/backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Start the Flask server:
```bash
python app.py
```

The server will start at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd solar_system_web/frontend
```

2. Open `index.html` in a modern web browser, or use a local server:

**Option A: Python HTTP Server**
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

**Option B: VS Code Live Server**
- Install the "Live Server" extension
- Right-click `index.html` and select "Open with Live Server"

## Usage

### Controls

**Mouse:**
- **Click**: View information about a planet
- **Shift+Click**: Select planets for comparison (max 2)
- **Drag**: Rotate camera view
- **Scroll**: Zoom in/out

**Keyboard Shortcuts:**
- **P**: Pause/Play simulation
- **R**: Reset simulation
- **C**: Clear selections

**UI Controls:**
- **Pause/Play Button**: Toggle animation
- **Reset Button**: Return to initial state
- **Speed Slider**: Adjust simulation speed (0.1x - 5x)

### Viewing Planet Information

1. Click on any planet to see:
   - Age and composition
   - Orbital and rotation periods
   - Physical properties

### Comparing Planets

1. Hold **Shift** and click the first planet
2. While holding **Shift**, click the second planet
3. View their relationship and current distance

## API Documentation

### REST Endpoints

**GET /api/bodies**
- Returns all celestial bodies with current positions

**GET /api/body/<name>**
- Returns detailed information about a specific body

**GET /api/relationship/<body1>/<body2>**
- Returns relationship information between two bodies

**POST /api/simulation/pause**
- Toggles pause state

**POST /api/simulation/reset**
- Resets simulation to time zero

**GET /api/simulation/state**
- Returns complete simulation state

**POST /api/simulation/speed**
- Sets simulation speed multiplier
- Body: `{"speed": 1.5}`

### WebSocket Events

**Client → Server:**
- `connect`: Establish WebSocket connection
- `request_update`: Request immediate position update

**Server → Client:**
- `initial_state`: Sent on connection with full state
- `position_update`: Continuous position updates (~60 FPS)

## Technical Details

### Physics Simulation
- Uses simple circular orbital motion
- Position calculated using: `angle = (2π × time) / orbital_period`
- Coordinates in XZ plane (Y-up coordinate system)

### Performance
- WebSocket updates at ~60 FPS
- Three.js rendering with hardware acceleration
- Efficient position streaming (only sends changes)

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check all dependencies are installed: `pip install -r requirements.txt`
- Verify port 5000 is not in use

### Frontend shows "Disconnected"
- Ensure backend server is running
- Check browser console for errors
- Verify WebSocket connection at `ws://localhost:5000`

### 3D scene doesn't render
- Check browser WebGL support: visit `https://get.webgl.org/`
- Update graphics drivers
- Try a different browser

### Planets don't move
- Click the Play button (might be paused)
- Check connection status indicator
- Verify WebSocket is connected (green indicator)

## Future Enhancements

Potential features for future versions:
- Planetary moons
- Asteroid belt
- Realistic elliptical orbits
- Planet textures and details
- Multiple camera views
- Time travel (fast forward/rewind)
- Recording and playback
- Mobile touch controls
- Multi-user synchronization

## Credits

- **VPython**: Original monolithic implementation
- **Three.js**: 3D rendering library
- **Flask**: Python web framework
- **Socket.IO**: Real-time WebSocket communication

## License

This project is for educational purposes.

---

**Enjoy exploring the solar system! 🌍🪐🌟**
