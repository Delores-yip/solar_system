from vpython import *
import time
import math

# Solar system data (basic facts)
bodies_data = {
    'Sun': {
        'info': 'The Sun is about 4.6 billion years old. It has no rotation period like planets (differential rotation: 25-35 days). Composition: Mostly hydrogen (74%) and helium (24%).',
        'radius': 10,  # Scaled for visualization
        'color': color.yellow,
        'pos': vector(0, 0, 0),
        'orbital_radius': 0,
        'orbital_period': 0  # Days
    },
    'Mercury': {
        'info': 'Mercury is about 4.5 billion years old. Orbital period: 88 days. Rotation period: 59 days. Composition: Iron core, silicate mantle.',
        'radius': 0.4,
        'color': color.gray(0.5),
        'pos': vector(20, 0, 0),
        'orbital_radius': 20,
        'orbital_period': 88
    },
    'Venus': {
        'info': 'Venus is about 4.5 billion years old. Orbital period: 225 days. Rotation period: 243 days (retrograde). Composition: Rocky, with thick CO2 atmosphere.',
        'radius': 0.9,
        'color': color.orange,
        'pos': vector(30, 0, 0),
        'orbital_radius': 30,
        'orbital_period': 225
    },
    'Earth': {
        'info': 'Earth is about 4.5 billion years old. Orbital period: 365 days. Rotation period: 24 hours. Composition: Iron core, silicate mantle, water, nitrogen-oxygen atmosphere.',
        'radius': 1,
        'color': color.blue,
        'pos': vector(40, 0, 0),
        'orbital_radius': 40,
        'orbital_period': 365
    },
    'Mars': {
        'info': 'Mars is about 4.5 billion years old. Orbital period: 687 days. Rotation period: 25 hours. Composition: Iron core, silicate mantle, thin CO2 atmosphere.',
        'radius': 0.5,
        'color': color.red,
        'pos': vector(60, 0, 0),
        'orbital_radius': 60,
        'orbital_period': 687
    },
    'Jupiter': {
        'info': 'Jupiter is about 4.6 billion years old. Orbital period: 4333 days (12 years). Rotation period: 10 hours. Composition: Mostly hydrogen and helium gas giant.',
        'radius': 5,
        'color': color.orange,
        'pos': vector(100, 0, 0),
        'orbital_radius': 100,
        'orbital_period': 4333
    },
    'Saturn': {
        'info': 'Saturn is about 4.5 billion years old. Orbital period: 10759 days (29 years). Rotation period: 11 hours. Composition: Hydrogen, helium, with rings of ice/rock.',
        'radius': 4,
        'color': color.yellow,
        'pos': vector(150, 0, 0),
        'orbital_radius': 150,
        'orbital_period': 10759
    },
    'Uranus': {
        'info': 'Uranus is about 4.5 billion years old. Orbital period: 30687 days (84 years). Rotation period: 17 hours (retrograde). Composition: Ice giant with hydrogen, helium, methane.',
        'radius': 3,
        'color': color.cyan,
        'pos': vector(200, 0, 0),
        'orbital_radius': 200,
        'orbital_period': 30687
    },
    'Neptune': {
        'info': 'Neptune is about 4.5 billion years old. Orbital period: 60190 days (165 years). Rotation period: 16 hours. Composition: Ice giant with hydrogen, helium, methane.',
        'radius': 3,
        'color': color.blue,
        'pos': vector(250, 0, 0),
        'orbital_radius': 250,
        'orbital_period': 60190
    }
}

# Relationships (pre-defined pairs; expand as needed)
relationships = {
    ('Earth', 'Sun'): 'The average distance between Earth and the Sun is about 149.6 million km (1 AU). The Sun provides energy for life on Earth.',
    ('Venus', 'Earth'): 'Venus and Earth are similar in size and composition (both rocky planets), but Venus has a runaway greenhouse effect making it much hotter.',
    ('Mars', 'Earth'): 'Mars and Earth share similarities like polar ice caps and seasons, but Mars has a thinner atmosphere and is colder.',
    # Add more pairs, e.g., ('Jupiter', 'Saturn'): '...'
}

# Create scene
scene = canvas(title='Solar System Model', width=800, height=600)
scene.autoscale = True
scene.forward = vector(0, -0.5, -1)  # Initial camera view

# Create bodies as spheres
bodies = {}
for name, data in bodies_data.items():
    # Disable trails to avoid clutter during interaction
    bodies[name] = sphere(pos=data['pos'], radius=data['radius'], color=data['color'], make_trail=False)
    # Label for name (optional) - attach to the sphere so we can update its position
    bodies[name].label = label(pos=bodies[name].pos + vector(0, data['radius']*1.2, 0), text=name, height=10, color=color.white, box=False)

# Info display: use the caption area under the canvas (works reliably in vpython)
# Pause control and caption helper
paused = False

def set_caption(msg: str):
    """Set the scene caption while preserving paused state marker.

    Use styled HTML so the info area is always readable regardless of the
    scene/browser background (white-on-dark panel with padding).
    """
    prefix = '[PAUSED] ' if paused else ''
    safe_msg = (prefix + msg)
    # Use an inline-styled div so the caption is visible on dark or light themes.
    scene.caption = f"<div style='background: rgba(0,0,0,0.65); color: #fff; padding: 8px; border-radius:6px; font-family: sans-serif; font-size:14px'>{safe_msg}</div>"

# Initial caption
set_caption('Click a body for info. Shift+Click two for relationship.')

# Simulation parameters
dt = 0.1  # Time step (accelerated for visualization)
time_scale = 100  # Speed up orbits

# Key handling: toggle pause with 'p' and keep caption state
def on_keydown(evt):
    """Toggle pause when pressing 'p'."""
    global paused
    key = getattr(evt, 'key', '')
    if not key:
        return
    # Normalize to lowercase for alphabetic keys
    k = key.lower()
    if k == 'p':
        paused = not paused
        state = 'Paused' if paused else 'Running'
        set_caption(f'{state}. Click a body for info. Shift+Click two for relationship.')

# Bind keydown event so user can press 'p' to pause/resume
scene.bind('keydown', on_keydown)

# Click handling
selected = []  # Track selected bodies for Shift-click

def on_click(evt):
    global selected
    # Diagnostic: show event type and pick target for debugging when paused
    pick_info = getattr(evt, 'pick', None)
    evt_name = getattr(evt, 'event', None) or getattr(evt, 'type', None) or getattr(evt, 'name', None)
    print(f'on_click fired: event={evt_name!r}, pick={pick_info!r}, paused={paused}')
    set_caption(f'DEBUG event={evt_name!r} pick={type(pick_info).__name__}:{getattr(pick_info, "text", "")}')

    # Determine the object that should be considered "picked".
    pick_obj = pick_info
    if pick_obj is None:
        # Fallback to proximity-based pick using scene.mouse.pos (may be None in some contexts)
        try:
            mp = scene.mouse.pos
        except Exception:
            mp = None
        if mp is not None:
            min_name = None
            min_dist = float('inf')
            for name, body in bodies.items():
                d = mag(body.pos - mp)
                if d < min_dist:
                    min_dist = d
                    min_name = name
            if min_name is not None and min_dist <= max(bodies[min_name].radius * 2.5, 1.0):
                pick_obj = bodies[min_name]
        # If still no pick_obj, try using the camera->mouse ray and compute perpendicular distance
        if pick_obj is None:
            try:
                ray = getattr(scene.mouse, 'ray', None)
                origin = scene.camera.pos
            except Exception:
                ray = None
                origin = None
            if ray is not None and origin is not None:
                # ray is a direction vector; compute perpendicular distance from ray to each body
                min_name = None
                min_dist = float('inf')
                for name, body in bodies.items():
                    # cross(origin->body, ray) magnitude divided by |ray| gives perpendicular distance
                    vec = body.pos - origin
                    d_perp = mag(cross(vec, ray)) / mag(ray)
                    if d_perp < min_dist:
                        min_dist = d_perp
                        min_name = name
                # Use a threshold relative to visual radius; ray-based distances are more accurate across camera angles
                if min_name is not None and min_dist <= max(bodies[min_name].radius * 2.0, 0.8):
                    pick_obj = bodies[min_name]

    # If we have a pick_obj, find which body it corresponds to and handle selection
    if pick_obj is None:
        return

    for name, body in bodies.items():
        picked = False
        if pick_obj == body:
            picked = True
        else:
            picked_label = getattr(body, 'label', None)
            if picked_label is not None and pick_obj == picked_label:
                picked = True
        if not picked:
            continue

        # Now handle Shift+click (relationship) or single click (show info)
        if getattr(evt, 'shift', False):
            selected.append(name)
            if len(selected) == 2:
                pair = tuple(sorted(selected))
                rel = relationships.get(pair, f'No specific relationship defined for {selected[0]} and {selected[1]}.')
                dist = mag(bodies[selected[0]].pos - bodies[selected[1]].pos) * 1.5e8 / 40
                set_caption(f'Relationship: {rel}  Distance: ~{dist:.2e} km')
                selected = []
        else:
            set_caption(f'{name}: {bodies_data[name]["info"]}')
            selected = []
        break

scene.bind('click', on_click)
# Also bind mousedown and mouseup to improve responsiveness when paused
scene.bind('mousedown', on_click)
scene.bind('mouseup', on_click)

# Main loop: Simulate orbits
t = 0
while True:
    rate(60)  # Frame rate
    # Only advance the simulation when not paused
    if not paused:
        for name, data in bodies_data.items():
            if data['orbital_radius'] > 0:
                angle = 2 * math.pi * t / (data['orbital_period'] / time_scale)
                bodies[name].pos = vector(data['orbital_radius'] * math.cos(angle), 0, data['orbital_radius'] * math.sin(angle))
                # Move the label with the body so it stays above the sphere
                if hasattr(bodies[name], 'label'):
                    bodies[name].label.pos = bodies[name].pos + vector(0, data['radius']*1.2, 0)
        t += dt