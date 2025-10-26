"""
Solar System Data Module
Contains all celestial body information and relationships.
"""

class SolarSystemData:
    """Manages solar system body data and relationships."""
    
    def __init__(self):
        self.bodies_data = {
            'Sun': {
                'info': 'The Sun is about 4.6 billion years old. It has no rotation period like planets (differential rotation: 25-35 days). Composition: Mostly hydrogen (74%) and helium (24%).',
                'radius': 10,
                'color': '#ffff00',  # yellow
                'pos': [0, 0, 0],
                'orbital_radius': 0,
                'orbital_period': 0
            },
            'Mercury': {
                'info': 'Mercury is about 4.5 billion years old. Orbital period: 88 days. Rotation period: 59 days. Composition: Iron core, silicate mantle.',
                'radius': 0.4,
                'color': '#808080',  # gray
                'pos': [20, 0, 0],
                'orbital_radius': 20,
                'orbital_period': 88
            },
            'Venus': {
                'info': 'Venus is about 4.5 billion years old. Orbital period: 225 days. Rotation period: 243 days (retrograde). Composition: Rocky, with thick CO2 atmosphere.',
                'radius': 0.9,
                'color': '#ffa500',  # orange
                'pos': [30, 0, 0],
                'orbital_radius': 30,
                'orbital_period': 225
            },
            'Earth': {
                'info': 'Earth is about 4.5 billion years old. Orbital period: 365 days. Rotation period: 24 hours. Composition: Iron core, silicate mantle, water, nitrogen-oxygen atmosphere.',
                'radius': 1,
                'color': '#0000ff',  # blue
                'pos': [40, 0, 0],
                'orbital_radius': 40,
                'orbital_period': 365
            },
            'Mars': {
                'info': 'Mars is about 4.5 billion years old. Orbital period: 687 days. Rotation period: 25 hours. Composition: Iron core, silicate mantle, thin CO2 atmosphere.',
                'radius': 0.5,
                'color': '#ff0000',  # red
                'pos': [60, 0, 0],
                'orbital_radius': 60,
                'orbital_period': 687
            },
            'Jupiter': {
                'info': 'Jupiter is about 4.6 billion years old. Orbital period: 4333 days (12 years). Rotation period: 10 hours. Composition: Mostly hydrogen and helium gas giant.',
                'radius': 5,
                'color': '#ffa500',  # orange
                'pos': [100, 0, 0],
                'orbital_radius': 100,
                'orbital_period': 4333
            },
            'Saturn': {
                'info': 'Saturn is about 4.5 billion years old. Orbital period: 10759 days (29 years). Rotation period: 11 hours. Composition: Hydrogen, helium, with rings of ice/rock.',
                'radius': 4,
                'color': '#ffff00',  # yellow
                'pos': [150, 0, 0],
                'orbital_radius': 150,
                'orbital_period': 10759
            },
            'Uranus': {
                'info': 'Uranus is about 4.5 billion years old. Orbital period: 30687 days (84 years). Rotation period: 17 hours (retrograde). Composition: Ice giant with hydrogen, helium, methane.',
                'radius': 3,
                'color': '#00ffff',  # cyan
                'pos': [200, 0, 0],
                'orbital_radius': 200,
                'orbital_period': 30687
            },
            'Neptune': {
                'info': 'Neptune is about 4.5 billion years old. Orbital period: 60190 days (165 years). Rotation period: 16 hours. Composition: Ice giant with hydrogen, helium, methane.',
                'radius': 3,
                'color': '#0000ff',  # blue
                'pos': [250, 0, 0],
                'orbital_radius': 250,
                'orbital_period': 60190
            }
        }
        
        self.relationships = {
            ('Earth', 'Sun'): 'The average distance between Earth and the Sun is about 149.6 million km (1 AU). The Sun provides energy for life on Earth.',
            ('Venus', 'Earth'): 'Venus and Earth are similar in size and composition (both rocky planets), but Venus has a runaway greenhouse effect making it much hotter.',
            ('Mars', 'Earth'): 'Mars and Earth share similarities like polar ice caps and seasons, but Mars has a thinner atmosphere and is colder.',
            ('Jupiter', 'Sun'): 'Jupiter orbits the Sun at an average distance of about 778 million km (5.2 AU). Its massive size helps protect inner planets by deflecting comets and asteroids.',
            ('Saturn', 'Jupiter'): 'Saturn and Jupiter are both gas giants with massive atmospheres primarily composed of hydrogen and helium, but Saturn has a more prominent ring system and lower density.'
        }
        
        # Normalize relationships for bidirectional lookup
        self.relationships_map = {}
        for (body1, body2), text in self.relationships.items():
            key = frozenset([body1, body2])
            self.relationships_map[key] = text
    
    def get_all_bodies(self):
        """Return all body data."""
        return self.bodies_data
    
    def get_body_info(self, name):
        """Get information about a specific body."""
        if name in self.bodies_data:
            return {
                'name': name,
                'info': self.bodies_data[name]['info'],
                'data': self.bodies_data[name]
            }
        return None
    
    def get_relationship(self, body1, body2):
        """Get relationship text between two bodies (order independent)."""
        key = frozenset([body1, body2])
        return self.relationships_map.get(key, None)
    
    def calculate_distance(self, body1, body2, positions):
        """Calculate distance between two bodies given their current positions."""
        if body1 not in positions or body2 not in positions:
            return None
        
        pos1 = positions[body1]
        pos2 = positions[body2]
        
        # Calculate Euclidean distance
        dx = pos2['x'] - pos1['x']
        dy = pos2['y'] - pos1['y']
        dz = pos2['z'] - pos1['z']
        
        distance = (dx**2 + dy**2 + dz**2) ** 0.5
        return round(distance, 2)
