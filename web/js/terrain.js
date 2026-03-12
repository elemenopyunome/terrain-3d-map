const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    1,
    100000
);

const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);

document.body.appendChild(renderer.domElement);


camera.position.set(0, 300, 500);



const light = new THREE.DirectionalLight(0xffffff, 1);

light.position.set(200, 400, 200);

scene.add(light);



const loader = new THREE.TextureLoader();



loader.load("assets/heightmap.png", function(texture) {

    const img = texture.image;

    const canvas = document.createElement("canvas");

    canvas.width = img.width;
    canvas.height = img.height;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(img, 0, 0);

    const imgData = ctx.getImageData(0,0,img.width,img.height).data;


    const geometry = new THREE.PlaneGeometry(
        1000,
        1000,
        img.width-1,
        img.height-1
    );


    const vertices = geometry.attributes.position.array;


    for(let i=0;i<img.width*img.height;i++){

        const height = imgData[i*4] / 255;

        vertices[i*3 + 2] = height * 200;

    }


    geometry.computeVertexNormals();


    const material = new THREE.MeshStandardMaterial({

        color:0x88aa88,
        wireframe:false

    });


    const terrain = new THREE.Mesh(geometry,material);

    terrain.rotation.x = -Math.PI/2;

    scene.add(terrain);

});


function animate(){

    requestAnimationFrame(animate);

    renderer.render(scene,camera);

}

animate();