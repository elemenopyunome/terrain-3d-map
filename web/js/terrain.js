const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
60,
window.innerWidth/window.innerHeight,
1,
10000
);

const renderer = new THREE.WebGLRenderer({antialias:true});

renderer.setSize(window.innerWidth,window.innerHeight);
document.body.appendChild(renderer.domElement);

camera.position.set(0,200,300);

const light = new THREE.DirectionalLight(0xffffff,1);
light.position.set(100,200,100);

scene.add(light);

const geometry = new THREE.PlaneGeometry(500,500,100,100);

const material = new THREE.MeshStandardMaterial({
color:0x88aa88
});

const terrain = new THREE.Mesh(geometry,material);

terrain.rotation.x = -Math.PI/2;

scene.add(terrain);

function animate(){
requestAnimationFrame(animate);
renderer.render(scene,camera);
}

animate();