/**
 * Solar System 3D Scene Manager
 * Handles Three.js rendering, camera, and interactions.
 */

class SolarSystemScene {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.bodies = new Map(); // Map of body name -> {mesh, label, ring}
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        this.selectedBodies = [];
        this.onBodyClick = null; // Callback for click events
    }

    initialize() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x000011);

        // Create camera
        this.camera = new THREE.PerspectiveCamera(
            60,
            window.innerWidth / window.innerHeight,
            0.1,
            10000
        );
        this.camera.position.set(0, 150, 300);
        this.camera.lookAt(0, 0, 0);

        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: this.canvas,
            antialias: true 
        });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);

        // Add lights
        const ambientLight = new THREE.AmbientLight(0x404040, 2);
        this.scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0xffffff, 2, 0);
        pointLight.position.set(0, 0, 0);
        this.scene.add(pointLight);

        // Add orbit controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.minDistance = 50;
        this.controls.maxDistance = 800;

        // Add stars background
        this.createStarField();

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());

        // Handle clicks
        this.canvas.addEventListener('click', (event) => this.handleClick(event));

        console.log('Scene initialized');
    }

    createStarField() {
        const starsGeometry = new THREE.BufferGeometry();
        const starsMaterial = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 2,
            sizeAttenuation: false
        });

        const starsVertices = [];
        for (let i = 0; i < 2000; i++) {
            const x = (Math.random() - 0.5) * 2000;
            const y = (Math.random() - 0.5) * 2000;
            const z = (Math.random() - 0.5) * 2000;
            starsVertices.push(x, y, z);
        }

        starsGeometry.setAttribute('position', 
            new THREE.Float32BufferAttribute(starsVertices, 3));
        
        const starField = new THREE.Points(starsGeometry, starsMaterial);
        this.scene.add(starField);
    }

    createBodies(bodiesData) {
        console.log('Creating bodies:', Object.keys(bodiesData));

        for (const [name, data] of Object.entries(bodiesData)) {
            // Create sphere geometry
            const geometry = new THREE.SphereGeometry(data.radius, 32, 32);
            
            // Create material with color
            const material = new THREE.MeshStandardMaterial({
                color: data.color,
                emissive: name === 'Sun' ? data.color : 0x000000,
                emissiveIntensity: name === 'Sun' ? 0.5 : 0
            });

            // Create mesh
            const mesh = new THREE.Mesh(geometry, material);
            mesh.userData.name = name;
            
            // Set initial position
            if (data.current_position) {
                mesh.position.set(
                    data.current_position.x,
                    data.current_position.y,
                    data.current_position.z
                );
            }

            this.scene.add(mesh);

            // Create text label (using sprite with canvas texture)
            const label = this.createTextLabel(name);
            label.position.copy(mesh.position);
            label.position.y += data.radius + 2;
            this.scene.add(label);

            // Store references
            this.bodies.set(name, {
                mesh: mesh,
                label: label,
                ring: null,
                data: data
            });
        }

        console.log('Bodies created:', this.bodies.size);
    }

    createTextLabel(text) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 64;

        // Draw text
        context.fillStyle = 'white';
        context.font = 'Bold 32px Arial';
        context.textAlign = 'center';
        context.textBaseline = 'middle';
        context.fillText(text, 128, 32);

        // Create texture from canvas
        const texture = new THREE.CanvasTexture(canvas);
        const spriteMaterial = new THREE.SpriteMaterial({ 
            map: texture,
            transparent: true
        });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.scale.set(10, 2.5, 1);

        return sprite;
    }

    updatePositions(positionsData) {
        for (const [name, position] of Object.entries(positionsData)) {
            const bodyObj = this.bodies.get(name);
            if (bodyObj) {
                // Update mesh position
                bodyObj.mesh.position.set(position.x, position.y, position.z);
                
                // Update label position
                bodyObj.label.position.copy(bodyObj.mesh.position);
                bodyObj.label.position.y += bodyObj.data.radius + 2;

                // Update selection ring if present
                if (bodyObj.ring) {
                    bodyObj.ring.position.copy(bodyObj.mesh.position);
                }
            }
        }
    }

    handleClick(event) {
        // Calculate mouse position in normalized device coordinates
        const rect = this.canvas.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        // Update raycaster
        this.raycaster.setFromCamera(this.mouse, this.camera);

        // Get all body meshes
        const meshes = Array.from(this.bodies.values()).map(b => b.mesh);
        
        // Check for intersections
        const intersects = this.raycaster.intersectObjects(meshes);

        if (intersects.length > 0) {
            const clickedBody = intersects[0].object.userData.name;
            const isShiftClick = event.shiftKey;

            console.log('Clicked:', clickedBody, 'Shift:', isShiftClick);

            // Call callback if set
            if (this.onBodyClick) {
                this.onBodyClick(clickedBody, isShiftClick);
            }
        }
    }

    highlightBody(name, color = 0x00ff00) {
        const bodyObj = this.bodies.get(name);
        if (!bodyObj) return;

        // Remove existing ring if any
        if (bodyObj.ring) {
            this.scene.remove(bodyObj.ring);
        }

        // Create selection ring
        const radius = bodyObj.data.radius * 1.5;
        const geometry = new THREE.RingGeometry(radius, radius + 0.3, 64);
        const material = new THREE.MeshBasicMaterial({ 
            color: color,
            side: THREE.DoubleSide 
        });
        const ring = new THREE.Mesh(geometry, material);
        
        // Position ring around body
        ring.position.copy(bodyObj.mesh.position);
        ring.rotation.x = Math.PI / 2;

        this.scene.add(ring);
        bodyObj.ring = ring;
    }

    removeHighlight(name) {
        const bodyObj = this.bodies.get(name);
        if (bodyObj && bodyObj.ring) {
            this.scene.remove(bodyObj.ring);
            bodyObj.ring = null;
        }
    }

    clearAllHighlights() {
        for (const [name, bodyObj] of this.bodies.entries()) {
            if (bodyObj.ring) {
                this.scene.remove(bodyObj.ring);
                bodyObj.ring = null;
            }
        }
        this.selectedBodies = [];
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Update controls
        this.controls.update();
        
        // Render scene
        this.renderer.render(this.scene, this.camera);
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    setBodyClickCallback(callback) {
        this.onBodyClick = callback;
    }
}
