import * as THREE from "three";
import { TerrainTile } from "./terrainTile.js";

export class TerrainManager {

constructor(scene,camera){

this.scene = scene;
this.camera = camera;

this.tileSize = 500;

this.loadedTiles = {};

this.viewDistance = 2;

}


update(){

const cx = Math.floor(this.camera.position.x / this.tileSize);
const cy = Math.floor(this.camera.position.z / this.tileSize);


for(let x=cx-this.viewDistance;x<=cx+this.viewDistance;x++){

for(let y=cy-this.viewDistance;y<=cy+this.viewDistance;y++){

const key = `${x}_${y}`;

if(!this.loadedTiles[key]){

this.loadTile(x,y);

}

}

}


for(const key in this.loadedTiles){

const tile = this.loadedTiles[key];

const dx = tile.x - cx;
const dy = tile.y - cy;

if(Math.abs(dx)>this.viewDistance || Math.abs(dy)>this.viewDistance){

this.scene.remove(tile.mesh);

delete this.loadedTiles[key];

}

}

}


loadTile(x,y){

const heightLoader = new THREE.TextureLoader();
const textureLoader = new THREE.TextureLoader();

heightLoader.load("assets/heightmap.png",(heightmap)=>{

textureLoader.load("assets/imagery_texture.png",(texture)=>{

const tile = new TerrainTile(
x,
y,
this.tileSize,
heightmap.image,
texture
);

this.scene.add(tile.mesh);

this.loadedTiles[`${x}_${y}`] = tile;

});

});

}

}