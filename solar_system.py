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

# Normalize relationships so order doesn't matter: map frozenset({a,b}) -> relation string
relationships_map = {frozenset(k): v for k, v in relationships.items()}

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
    # remember original color for highlighting toggles
    bodies[name].orig_color = data['color']

# Info display: use the caption area under the canvas (works reliably in vpython)
# Pause control and caption helper
paused = False
selection_mode = False  # when True, clicks (without Shift) will act as selection

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
    # Toggle selection-mode with 'm' so users can select without using Shift (avoids camera movement conflict)
    global selection_mode
    if k == 'm':
        selection_mode = not selection_mode
        set_caption(f"Selection mode {'ON' if selection_mode else 'OFF'}: click bodies to select (or press 'm' to toggle).")
    # Press 'c' to clear any current selections and their visuals
    if k == 'c':
        # clear selected list and hide any selectors
        for sname in list(selected):
            sb = bodies.get(sname)
            if sb is None:
                continue
            if hasattr(sb, 'selector'):
                try:
                    sb.selector.visible = False
                except Exception:
                    pass
                try:
                    del sb.selector
                except Exception:
                    pass
            if hasattr(sb, 'orig_color'):
                sb.color = sb.orig_color
        selected.clear()
        set_caption('Cleared selections.')
    # Press 's' to enter selection mode that waits for two clicks (legacy synchronous mode)
    if k == 's':
        try:
            select_two_with_wait()
        except Exception as e:
            set_caption(f'Error entering select mode: {e}')

# Bind keydown event so user can press 'p' to pause/resume
scene.bind('keydown', on_keydown)


def pick_obj_from_event_or_mouse(evt):
    """Return the picked object from an event or use proximity/ray fallback.

    This mirrors the logic in on_click but packaged for reuse in synchronous
    wait-for-click selection mode.
    """
    pick_obj = getattr(evt, 'pick', None)
    if pick_obj is not None:
        return pick_obj

    # proximity fallback
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
            return bodies[min_name]

    # ray fallback
    try:
        ray = getattr(scene.mouse, 'ray', None)
        origin = scene.camera.pos
    except Exception:
        ray = None
        origin = None
    if ray is not None and origin is not None:
        min_name = None
        min_dist = float('inf')
        for name, body in bodies.items():
            vec = body.pos - origin
            d_perp = mag(cross(vec, ray)) / (mag(ray) if mag(ray) != 0 else 1.0)
            if d_perp < min_dist:
                min_dist = d_perp
                min_name = name
        if min_name is not None and min_dist <= max(bodies[min_name].radius * 2.0, 0.8):
            return bodies[min_name]

    return None


def select_two_with_wait():
    """Synchronous selection mode: wait for two clicks and show their relationship.

    This uses scene.waitfor('click') so it works even when the main loop is
    paused or the event system behaves differently in paused state.
    """
    set_caption('Selection mode: click two bodies (or click the same to cancel)')
    sel_names = []
    selectors = []
    for i in range(2):
        evt = scene.waitfor('click')
        pickobj = pick_obj_from_event_or_mouse(evt)
        if pickobj is None:
            set_caption('No object picked; try again.')
            return
        # map pickobj to body name
        picked_name = None
        for name, body in bodies.items():
            if pickobj == body or getattr(body, 'label', None) == pickobj:
                picked_name = name
                break
        if picked_name is None:
            set_caption('Picked object not recognized; aborting.')
            return
        # visual feedback
        b = bodies[picked_name]
        try:
            sel = ring(pos=b.pos, axis=vector(0,1,0), radius=b.radius*1.4, thickness=max(b.radius*0.06, 0.05), color=color.cyan)
            selectors.append(sel)
        except Exception:
            # fallback: tint color
            b.color = color.cyan
            selectors.append(('color', b))
        sel_names.append(picked_name)

    # show relationship for the two selected
    pair = tuple(sorted(sel_names))
    rel = relationships.get(pair, f'No specific relationship defined for {sel_names[0]} and {sel_names[1]}.')
    dist = mag(bodies[sel_names[0]].pos - bodies[sel_names[1]].pos) * 1.5e8 / 40
    set_caption(f'Selection: {sel_names[0]} & {sel_names[1]} -> {rel}  Distance: ~{dist:.2e} km')

    # clear selectors and restore colors
    for s in selectors:
        if isinstance(s, tuple) and s[0] == 'color':
            s[1].color = s[1].orig_color
        else:
            try:
                s.visible = False
            except Exception:
                pass

# Click handling
selected = []  # Track selected bodies for Shift-click

def on_click(evt):
    global selected
    # Determine pick target without noisy debug output
    pick_info = getattr(evt, 'pick', None)

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
        # selection is active if user held Shift or toggled selection_mode (press 'm')
        if (selection_mode or getattr(evt, 'shift', False)):
            # Toggle selection: deselect if already selected
            if name in selected:
                # deselect
                selected.remove(name)
                # remove visual selector if exists
                if hasattr(body, 'selector'):
                    try:
                        body.selector.visible = False
                    except Exception:
                        pass
                    try:
                        del body.selector
                    except Exception:
                        pass
                # restore original color if we used color fallback
                if hasattr(body, 'orig_color'):
                    body.color = body.orig_color
                # update caption to reflect deselection
                set_caption(f'Deselected {name}.')
            else:
                # if already two selected, clear previous selection first
                if len(selected) >= 2:
                    # clear existing selectors
                    for sname in list(selected):
                        sb = bodies[sname]
                        if hasattr(sb, 'selector'):
                            try:
                                sb.selector.visible = False
                            except Exception:
                                pass
                            try:
                                del sb.selector
                            except Exception:
                                pass
                    selected.clear()
                # select this body
                selected.append(name)
                # add a visual ring to indicate selection
                try:
                    body.selector = ring(pos=body.pos, axis=vector(0,1,0), radius=body.radius*1.4, thickness=max(body.radius*0.06, 0.05), color=color.green)
                except Exception:
                    # fallback: change color if ring not available
                    body.color = color.green

                # if now two selected, show relationship
                if len(selected) == 2:
                    # Show relationship and keep selectors visible until user clears (press 'c')
                    pair_key = frozenset(selected)
                    rel = relationships_map.get(pair_key, f'No specific relationship defined for {selected[0]} and {selected[1]}.')
                    dist = mag(bodies[selected[0]].pos - bodies[selected[1]].pos) * 1.5e8 / 40
                    set_caption(f'Relationship: {rel}  Distance: ~{dist:.2e} km  (press c to clear)')
        else:
            # single click: show info about the body
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
                # If a selector ring exists for this body, move it with the body so it follows during animation
                if hasattr(bodies[name], 'selector'):
                    try:
                        bodies[name].selector.pos = bodies[name].pos
                    except Exception:
                        pass
        t += dt