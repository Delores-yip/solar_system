"""
Solar System Simulation Engine
Handles orbital mechanics and position calculations.
"""

import math
import time
from data import SolarSystemData


class OrbitSimulator:
    """Simulates orbital motion of celestial bodies."""
    
    def __init__(self):
        self.data = SolarSystemData()
        self.time = 0.0
        self.paused = False
        self.time_scale = 1.0  # Speed multiplier
        self.dt = 0.016  # Time step (~60 fps)
        self.last_update = time.time()
    
    def calculate_position(self, body_name, current_time=None):
        """
        Calculate the 3D position of a body at a given time.
        Uses simple circular orbital motion.
        
        Args:
            body_name: Name of the celestial body
            current_time: Time value (uses self.time if None)
        
        Returns:
            dict with x, y, z coordinates
        """
        if current_time is None:
            current_time = self.time
        
        body = self.data.bodies_data.get(body_name)
        if not body:
            return None
        
        orbital_radius = body['orbital_radius']
        orbital_period = body['orbital_period']
        
        # Sun stays at origin
        if orbital_radius == 0 or orbital_period == 0:
            return {'x': 0, 'y': 0, 'z': 0}
        
        # Calculate angle based on time and orbital period
        # Complete orbit = 2π radians
        angle = (2 * math.pi * current_time) / orbital_period
        
        # Circular orbit in XZ plane (Y is up)
        x = orbital_radius * math.cos(angle)
        z = orbital_radius * math.sin(angle)
        y = 0  # Keep orbits flat for simplicity
        
        return {'x': x, 'y': y, 'z': z}
    
    def get_all_positions(self):
        """Get current positions of all bodies."""
        positions = {}
        for body_name in self.data.bodies_data.keys():
            positions[body_name] = self.calculate_position(body_name)
        return positions
    
    def update(self, delta_time=None):
        """
        Update simulation by one time step.
        
        Args:
            delta_time: Optional time delta (uses self.dt if None)
        
        Returns:
            dict of all current positions
        """
        if self.paused:
            return self.get_all_positions()
        
        if delta_time is None:
            delta_time = self.dt
        
        # Advance time
        self.time += delta_time * self.time_scale
        
        return self.get_all_positions()
    
    def toggle_pause(self):
        """Toggle pause state."""
        self.paused = not self.paused
        return self.paused
    
    def set_pause(self, paused):
        """Set pause state explicitly."""
        self.paused = paused
        return self.paused
    
    def reset(self):
        """Reset simulation to time zero."""
        self.time = 0.0
        self.paused = False
        return self.get_all_positions()
    
    def set_time_scale(self, scale):
        """Set the simulation speed multiplier."""
        if scale > 0:
            self.time_scale = scale
        return self.time_scale
    
    def get_state(self):
        """Get complete simulation state."""
        return {
            'time': round(self.time, 2),
            'paused': self.paused,
            'time_scale': self.time_scale,
            'positions': self.get_all_positions()
        }
