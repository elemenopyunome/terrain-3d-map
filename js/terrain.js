import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { TerrainManager } from "./terrainManager.js";


const scene = new THREE.Scene();

scene.background = new THREE.Color(0xbfd1e5);


const camera = new THREE.PerspectiveCamera(
60,
window.innerWidth/window.innerHeight,
1,
100000
);


const renderer = new THREE.WebGLRenderer({antialias:true});

renderer.setSize(window.innerWidth,window.innerHeight);

document.body.appendChild(renderer.domElement);


const controls = new OrbitControls(camera,renderer.domElement);

controls.enableDamping = true;

camera.position.set(0,400,600);


/* LIGHTING */

const ambient = new THREE.AmbientLight(0xffffff,0.4);
scene.add(ambient);

const sun = new THREE.DirectionalLight(0xffffff,1);

sun.position.set(300,500,200);

scene.add(sun);


/* TERRAIN */

const terrain = new TerrainManager(scene,camera);


/* LOOP */

function animate(){

requestAnimationFrame(animate);

controls.update();

terrain.update();

renderer.render(scene,camera);

}

animate();


window.addEventListener("resize",()=>{

camera.aspect = window.innerWidth/window.innerHeight;

camera.updateProjectionMatrix();

renderer.setSize(window.innerWidth,window.innerHeight);

});