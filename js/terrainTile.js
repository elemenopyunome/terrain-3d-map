import * as THREE from "three";

export class TerrainTile {

constructor(x,y,size,heightmap,texture){

this.x = x;
this.y = y;

this.mesh = this.createMesh(size,heightmap,texture);

this.mesh.position.set(
x*size,
0,
y*size
);

}


createMesh(size,heightmap,texture){

const geometry = new THREE.PlaneGeometry(
size,
size,
heightmap.width-1,
heightmap.height-1
);


const canvas = document.createElement("canvas");

canvas.width = heightmap.width;
canvas.height = heightmap.height;

const ctx = canvas.getContext("2d");

ctx.drawImage(heightmap,0,0);

const data = ctx.getImageData(
0,
0,
heightmap.width,
heightmap.height
).data;


const vertices = geometry.attributes.position.array;


for(let i=0;i<heightmap.width*heightmap.height;i++){

const height = data[i*4]/255;

vertices[i*3+2] = height*200;

}


geometry.computeVertexNormals();


const material = new THREE.MeshStandardMaterial({
map:texture
});


const mesh = new THREE.Mesh(geometry,material);

mesh.rotation.x = -Math.PI/2;

return mesh;

}

}