# Quick Start Guide

## Easiest Way to Run (Windows)

### Option 1: Automatic Launch (Recommended)
1. Open File Explorer
2. Navigate to: `solar_system_web/`
3. Double-click: `launch.bat`
4. Wait for the browser to open automatically

That's it! The script will:
- Create a virtual environment
- Install all dependencies
- Start both backend and frontend servers
- Open your browser to the application

### Option 2: Manual Launch

**Terminal 1 - Backend:**
```bash
cd solar_system_web
start_backend.bat
```

**Terminal 2 - Frontend:**
```bash
cd solar_system_web
start_frontend.bat
```

Then open: `http://localhost:8000`

## For macOS/Linux Users

**Terminal 1 - Backend:**
```bash
cd solar_system_web/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd solar_system_web/frontend
python3 -m http.server 8000
```

Then open: `http://localhost:8000`

## Stopping the Application

- Close the backend terminal window (or press Ctrl+C)
- Close the frontend terminal window (or press Ctrl+C)

## Troubleshooting

**"Python is not installed or not in PATH"**
- Install Python 3.8+ from python.org
- Make sure to check "Add Python to PATH" during installation

**Port already in use**
- Backend (5000): Change port in `backend/app.py` (line 188)
- Frontend (8000): Use different port: `python -m http.server 8080`

**Browser shows "Cannot connect"**
- Wait a few more seconds for servers to start
- Check both terminal windows for errors
- Ensure firewall isn't blocking connections

## First Time Use

When you first run the application:
1. Backend will install dependencies (takes ~30 seconds)
2. Both servers will start
3. Browser will open automatically
4. You'll see "Connecting..." briefly, then "Connected"

## Controls Quick Reference

- **Click** a planet → View info
- **Shift+Click** two planets → Compare
- **Drag** mouse → Rotate view
- **Scroll** → Zoom
- **P** key → Pause/Play
- **R** key → Reset
- **C** key → Clear selection

Enjoy exploring the solar system! 🌍🪐
