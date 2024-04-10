import * as THREE from "three";
// 'https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.module.js';
import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.160.1/examples/jsm/controls/OrbitControls.js';
// import {FBXLoader} from 'https://cdn.jsdelivr.net/npm/three@0.124/examples/jsm/loaders/FBXLoader.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.1/examples/jsm/loaders/GLTFLoader.js';
import { SelectionBox } from 'https://cdn.jsdelivr.net/npm/three@0.160.1/examples/jsm/interactive/SelectionBox.js';
import { SelectionHelper } from 'https://cdn.jsdelivr.net/npm/three@0.160.1/examples/jsm/interactive/SelectionHelper.js';
var cube;

var food=0;
var stone=0;
var gold=0;
var wood=0;
var CitizenCount=0;
var housing=0;
var IdleCitizens=[]

class Citizen{
	constructor(state,health){
		this.state=state;//states are idle, moving, each of the respective resources
		this.health=health;
	}

	setState(newState){
		this.state=newState;
	}
	getState(){
		return this.state;
	}
	adjustHealth(adjustment){
		this.health=this.health-adjustment;
	}
	getHealth(){
		return this.health
	}

	Work(expression){
		switch(expression) {
			case "food":
				setInterval(function () {food+=10;console.log(food);document.getElementById("food").innerHTML=food}, 1000);
				// String(food);
				break;
			case "wood":
				setInterval(function () {wood+=10;console.log(wood);document.getElementById("wood").innerHTML=wood}, 1000);
				break;
			case "gold":
				setInterval(function () {gold+=10;console.log(food);document.getElementById("gold").innerHTML=gold}, 1000);
				break;
			case "stone":
				setInterval(function () {stone+=10;console.log(food);document.getElementById("stone").innerHTML=stone}, 1000);
				break;
			default:
				break;
		}
	}

}

const scene = new THREE.Scene();
scene.background=new THREE.Color("#ADD8E6");

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.getElementById("container").insertBefore(renderer.domElement, document.getElementById("container").firstChild)

const camera = new THREE.PerspectiveCamera( 75, renderer.domElement.width/renderer.domElement.height, 0.1, 10000 );//window.innerWidth / window.innerHeight
camera.position.z = 5;
camera.position.y = 1;
camera.lookAt(new THREE.Vector3(0,0,0))

const controls = new OrbitControls( camera, renderer.domElement );

let ambientLight = new THREE.AmbientLight(new THREE.Color('hsl(0, 0%, 100%)'), 3);
scene.add(ambientLight);

{//the cube that shows closest vertice to pointer
const geometry = new THREE.BoxGeometry( 0.02, 0.02, 0.02 );
const material = new THREE.MeshLambertMaterial({color: 0x0000ff, transparent: true, opacity: 0.5}) 
cube = new THREE.Mesh( geometry, material );
scene.add( cube );
}

//recieve the image to generate 9 grids from
const texMap=new Image()
const DispMap=new Image()
texMap.src="threejsFold/TextureMap.png"
DispMap.src="threejsFold/heightmapTexture.png"

var manyCanvas=[]
var manyGrids=[]
var manyPlanes=[]
function GenerateGrids(){//generate 9 grids for the image
	for(var i=0;i<9;i++){
		var PlaneGeometry = new THREE.PlaneGeometry( 4,4,200, 200 );//12/3, 600/3
		manyGrids.push(PlaneGeometry)
	}
}
GenerateGrids()

texMap.onload=function(){
	// var textureCanvas=document.createElement('canvas');
	// textureCanvas.height=texMap.height/3
	// textureCanvas.width=texMap.width/3
	// textureCanvas.style.zIndex="100000"
	// textureCanvas.getContext('2d').drawImage(texMap, 0, 0,texMap.width,texMap.height)
	{
	// textureCanvas.getContext('2d').restore();
	// document.body.appendChild(textureCanvas)
	// Grassmaterial.update()
	
	// Grassmaterial=new THREE.MeshLambertMaterial( { map: Grassmaterial,displacementMap:dispMap,wireframe:false } )
	// Grassmaterial.map.needsUpdate=true
	// Grassmaterial.material.map.needsUpdate = true;

	// const vertex = new THREE.Vector3(); // create once and reuse
	// const attribute = plane.geometry.getAttribute( 'position' );
	// vertex.fromBufferAttribute( attribute, 0 );
	// // vertices=plane.geometry.attributes.position.array
	// console.log(plane.localToWorld( vertex ))
	}
	// for(var i=0;i<3;i++){
	// 	for(var j=0;j<3;j++){
	// 		textureCanvas.getContext('2d').drawImage(texMap, (texMap.width/3)*i, (texMap.height/3)*j,texMap.width,texMap.height)
	// 	}
	// }
	var relax=0;
	var bingus=0;

	manyGrids.forEach((element) => {
		var textureCanvas=document.createElement('canvas');
		textureCanvas.height=texMap.height/3
		textureCanvas.width=texMap.width/3
		textureCanvas.style.zIndex="100000"
		// element.position.set(-4+bingus*4,0,-4+relax*4)//4-4*x,0,4-4*y)	
		textureCanvas.getContext('2d').drawImage(texMap, (texMap.width/3)*bingus-bingus, (texMap.height/3)*relax-relax,texMap.width/3,texMap.height/3,0,0,texMap.width/3,texMap.height/3)	
		manyCanvas.push(textureCanvas)
		if(relax>1){
			relax=0
			bingus++
		}else{
			relax++
		}
		console.log(element)
		var Grassmaterial = new THREE.CanvasTexture(textureCanvas)
		Grassmaterial=new THREE.MeshLambertMaterial( { map: Grassmaterial,wireframe:false } )
		var plane = new THREE.Mesh( element, Grassmaterial );
		plane.rotation.x -= Math.PI/2;
		plane.matrixAutoUpdate = true;
		manyPlanes.push(plane)
		}
	)
		
}
DispMap.onload=function(){
	// var DisplacementCanvas=document.createElement('canvas');
	// DisplacementCanvas.height=DispMap.height/3
	// DisplacementCanvas.width=DispMap.width/3
	// DisplacementCanvas.style.zIndex="100000"
	// DisplacementCanvas.getContext('2d',{willReadFrequently:true}).drawImage(DispMap, 0, 0,DispMap.width,DispMap.height)
	var i=0
	var relax=0;
	var bingus=0;
	manyPlanes.forEach((element) => {

		//get image starts at 0, hence, when image is 600, the final here is 599, causing image data at 600 to be 0, creating the drop
		//need to go from the start to the beginning of the next, so the final one doesnt need the +1 in the loop...
		var DisplacementCanvas=document.createElement('canvas');
		DisplacementCanvas.height=DispMap.height/3
		DisplacementCanvas.width=DispMap.width/3
		DisplacementCanvas.style.zIndex="100000"
		// console.log(relax,"RELAX")
		DisplacementCanvas.getContext('2d',{willReadFrequently:true}).drawImage(DispMap, (DispMap.width/3)*bingus-bingus, (DispMap.height/3)*relax-relax,DispMap.width/3,DispMap.height/3,0, 0,DispMap.width/3,DispMap.height/3)
		element.material.displacementMap = new THREE.CanvasTexture(DisplacementCanvas) //new THREE.Texture(DisplacementCanvas);
		// console.log("HEIGHT",DispMap.height/3,element.geometry.parameters.widthSegments)
		// for(var y=1;y<=DispMap.height/3+1;y++){//+1//so 200 pixel blocks per grid
		// 	console.log("YIPEE",y)
		// 	for(var x=1;x<=DispMap.width/3+1;x++){//+1
				
		// 		var data=DisplacementCanvas.getContext('2d').getImageData((x-1)+(DispMap.width/3)*bingus,(y-1)+(DispMap.height/3)*relax,1,1).data
		// 		//plane is replaced by element
		// 		i = ((y-1) * (element.geometry.parameters.widthSegments+1)) + (x-1);
		// 		element.geometry.attributes.position.setZ(i, data[0]/255);
				
		// 	}
		// }	
		element.position.set(-4+bingus*4,0,-4+relax*4)//4-4*x,0,4-4*y)		
		if(relax>1){
			relax=0
			bingus++
		}else{
			relax++
		}
		// element.geometry.attributes.position.needsUpdate = true;
		// element.geometry.computeVertexNormals();
		// element.matrixAutoUpdate = true;
		
		scene.add( element );
	})
	
	{
	// plane.geometry.attributes.position.setZ(0, 1);
	// var widthStep=DispMap.width/plane.geometry.parameters.widthSegments+1
	// var heightStep=DispMap.height/plane.geometry.parameters.heightSegments+1
	// for (var h = 0; h < plane.geometry.parameters.heightSegments+1; h++) {
	// 	for (var w = 0; w < plane.geometry.parameters.widthSegments+1; w++) {
	// 	  var imgData = DisplacementCanvas.getContext('2d').getImageData(600-Math.round(w * widthStep), 600-Math.round(h * heightStep), 1, 1).data;
	// 	  var displacementVal = imgData[0] / 255.0;
	// 	  displacementVal *= 2;
	// 	  var idx = (h * plane.geometry.parameters.widthSegments+1) + w;
	// 	  plane.geometry.attributes.position.setZ(idx, displacementVal);
	// 	}
	//   }
	}





	// console.log(plane.geometry.getAttribute("position"))
	// console.log(vertex.fromBufferAttribute( vertices, 500 ))
	// .set(vertex.x,data[0]/255,vertex.y);
	// scene.add( plane );
}


function FindPixelPositionForVertexPosition(position){//adjustX,adjustY
	//each grid is 12 by 12 in world size, 600 by 600 in pixels, 
	//center chunk is centered on the world so + 6 x and +6 y  
	
	var posX=position.x+6
	var posz=position.y+6
	
	posX=posX/12
	posz=posz/12
	
	const pixelX=Math.round(posX*600)
	const pixelY=600-Math.round(posz*600)
	// console.log(Math.round(pixelX),pixelY)
	return [pixelX,pixelY]//new THREE.Vector2(pixelX,pixelY)
}





const loader = new GLTFLoader();
loader.load(
	// resource URL
	'./threejsFold/basicAssets.glb',
	// called when the resource is loaded
	function ( gltf ) {

		scene.add( gltf.scene );
		gltf.scene.scale.set(0.02,0.02,0.02)
		gltf.animations; // Array<THREE.AnimationClip>
		gltf.scene; // THREE.Group
		gltf.scenes; // Array<THREE.Group>
		gltf.cameras; // Array<THREE.Camera>
		gltf.asset; // Object

	},
	// called while loading is progressing
	function ( xhr ) {

		console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );

	},
	// called when loading has errors
	function ( error ) {

		console.log( 'An error happened' );

	}
);

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
raycaster.setFromCamera( pointer, camera );
var vertexA = new THREE.Vector3(); // create once and reuse
var vertexB = new THREE.Vector3(); // create once and reuse
var vertexC = new THREE.Vector3(); // create once and reuse

function onPointerMove( event ) {
	// console.log("heheheheheh")
	// calculate pointer position in normalized device coordinates
	// (-1 to +1) for both components

	pointer.x = (event.offsetX / renderer.domElement.clientWidth)* 2 - 1//( event.clientX / window.innerWidth ) * 2 - 1;
	pointer.y = -(event.offsetY / renderer.domElement.clientHeight) * 2 + 1//- ( event.clientY / window.innerHeight ) * 2 + 1;	
	
	raycaster.setFromCamera( pointer, camera );
	try{
		const intersects = raycaster.intersectObjects( scene.children );
		if(intersects.length>0){
			// console.log(intersects[0].object.geometry.type)
			var attribute = plane.geometry.getAttribute( 'position' );
			// attribute.needsUpdate=true
			var terrainPlane=null
			var index=0
			while(terrainPlane==null && index<intersects.length){
				if(intersects[index].object.geometry.type=="PlaneGeometry"){
					terrainPlane=intersects[index]
					index=intersects.length
					
				}
				index++
			}
			
			const rayHit=terrainPlane.point
			// intersects[0].point

			vertexA.fromBufferAttribute( attribute, terrainPlane.face.a );
			vertexB.fromBufferAttribute( attribute, terrainPlane.face.b );
			vertexC.fromBufferAttribute( attribute, terrainPlane.face.c );

			const disA=vertexA.distanceTo(rayHit)
			const disB=vertexB.distanceTo(rayHit)
			const disC=vertexC.distanceTo(rayHit)
			var adjustmentX=0
			var adjustmentY=1
			if(disA>disB){
				// minAB=disB			
				if(disB>disC){
					if(rayHit.x>vertexC.x){adjustmentX=1}else{adjustmentX=-1}
					// if(rayHit.y>vertexC.y){adjustmentY=-1}else{adjustmentY=1}
					cube.position.set(vertexC.x+0.01*adjustmentX,vertexC.z+0.01,-vertexC.y-0.01*adjustmentY)
				}else{
					if(rayHit.x>vertexB.x){adjustmentX=1}else{adjustmentX=-1}
					if(rayHit.y>vertexB.y){adjustmentY=-1}else{adjustmentY=1}
					cube.position.set(vertexB.x+0.01*adjustmentX,vertexB.z+0.01,-vertexB.y-0.01*adjustmentY)
				}
			}else{
				// minAB=disA
				if(disA>disC){
					// minABC=disC
					if(rayHit.x>vertexC.x){adjustmentX=1}else{adjustmentX=-1}
					// if(rayHit.y>vertexC.y){adjustmentY=-1}else{adjustmentY=1}
					cube.position.set(vertexC.x+0.01*adjustmentX,vertexC.z+0.01,-vertexC.y-0.01*adjustmentY)
				}else{
					if(rayHit.x>vertexA.x){adjustmentX=1}else{adjustmentX=-1}
					// if(rayHit.y>vertexA.y){adjustmentY=-1}else{adjustmentY=1}
					cube.position.set(vertexA.x+0.01*adjustmentX,vertexA.z+0.01,-vertexA.y-0.01*adjustmentY)
				}
			}
		}
	}catch(err){
		console.log(err)
	}

	// for ( let i = 0; i < intersects.length; i ++ ) {

	// 	intersects[ i ].object.material.color.set( 0xff0000 );

	// }

}
// const mouseoverEvent = new Event('mouseover')
// renderer.domElement.onmouseover=function(){console.log("heheh")}
renderer.domElement.addEventListener( 'mousemove',onPointerMove  );//onPointerMove
// renderer.domElement
const selectionBox = new SelectionBox( camera, scene );
const helper = new SelectionHelper(renderer, 'selectBox' );

// renderer.domElement.addEventListener( 'pointerdown', function ( event ) {

// 	for ( const item of selectionBox.collection ) {

// 		item.material.emissive.set( 0x000000 );

// 	}

// 	selectionBox.startPoint.set(
// 		( event.clientX / window.innerWidth ) * 2 - 1,
// 		- ( event.clientY / window.innerHeight ) * 2 + 1,
// 		0.5 );

// } );

// renderer.domElement.addEventListener( 'pointermove', function ( event ) {
// 	// document.elementFromPoint(e.clientX, e.clientY)
// 	// console.log(document.elementFromPoint(event.clientX, event.clientY),"HEYYY")
// 	if ( helper.isDown ) {

// 		for ( let i = 0; i < selectionBox.collection.length; i ++ ) {

// 			selectionBox.collection[ i ].material.emissive.set( 0x000000 );

// 		}

// 		selectionBox.endPoint.set(
// 			( event.clientX / window.innerWidth ) * 2 - 1,
// 			- ( event.clientY / window.innerHeight ) * 2 + 1,
// 			0.5 );

// 		const allSelected = selectionBox.select();

// 		for ( let i = 0; i < allSelected.length; i ++ ) {

// 			allSelected[ i ].material.emissive.set( 0xffffff );

// 		}

// 	}

// } );

// renderer.domElement.addEventListener( 'pointerup', function ( event ) {

// 	selectionBox.endPoint.set(
// 		( event.clientX / window.innerWidth ) * 2 - 1,
// 		- ( event.clientY / window.innerHeight ) * 2 + 1,
// 		0.5 
// 		);

// 	const allSelected = selectionBox.select();

// 	for ( let i = 0; i < allSelected.length; i ++ ) {

// 		allSelected[ i ].material.emissive.set( 0xffffff );

// 	}
// });



// var imagedata = getImageData( imgTexture.image );
// var color = getPixel( imagedata, 10, 10 );

function changePathTexture(){}

function changeDisplacementTexture(){
	
}

function addBuilding(){

}
// function addVilToResource(which){
//     console.log(which)
// 	document.getElementById("food").setAttribute("data-value",Number(document.getElementById('food').getAttribute('data-value'))+1)
// 	console.log(Number(document.getElementById('food').getAttribute('data-value')))
// 	document.getElementById("food").innerHTML=Number(document.getElementById('food').getAttribute('data-value'))
// }

const selected=document.querySelectorAll('button')
for (let i = 0; i < selected.length; i++) {
	// Do stuff
	// console.log(selected[i].value)
	switch(selected[i].value) {
		case "Food":
			selected[i].addEventListener('click', (e) => {
				try{
					console.log("TRIGGERING WORK")
					const worker=IdleCitizens.pop()
					worker.Work('food')
				}catch(err){
					console.log("no idle Citizens")
				}
			});
			break;			
		case "Wood":
			selected[i].addEventListener('click', (e) => {
				try{
					console.log("TRIGGERING WORK")
					const worker=IdleCitizens.pop()
					worker.Work('wood')
				}catch(err){
					console.log("no idle Citizens")
				}
			});
			break;
		case "Gold":
			selected[i].addEventListener('click', (e) => {
				try{
					console.log("TRIGGERING WORK")
					const worker=IdleCitizens.pop()
					worker.Work('gold')
				}catch(err){
					console.log("no idle Citizens")
				}
			});
			break;
		case "Stone":
			selected[i].addEventListener('click', (e) => {
				try{
					console.log("TRIGGERING WORK")
					const worker=IdleCitizens.pop()
					worker.Work('stone')
				}catch(err){
					console.log("no idle Citizens")
				}
			});
			break;
		case "createCitizen":
			selected[i].addEventListener('click', (e) => {
				try{			
					var newCit=new Citizen('idle',100)
					IdleCitizens.push(newCit)
					CitizenCount+=1;

				}catch(err){
					console.log("mm")
				}
			});

			break;
		case "House":
			break
		default:
			break;
	}
	// .addEventListener('click', (e) => {
	// 	// console.log(e.target.value)
	// 	switch(e.target.value) {
	// 		case "Food":
	// 			try{
	// 				console.log("TRIGGERING WORK")
	// 				const worker=IdleCitizens.pop()
	// 				worker.Work('food')
	// 			}catch(err){
	// 				console.log("no idle Citizens")
	// 			}
	// 			break;			
	// 		case "Wood":
	// 			break;
	// 		case "Gold":
	// 			break;
	// 		case "Stone":
	// 			break;
	// 		case "createCitizen":
	// 			var newCit=new Citizen('idle',100)
	// 			IdleCitizens.push(newCit)
	// 			break;
	// 		default:
	// 			break;
	// 	}

	// 	console.log("hi")
	// 	// document.getElementById("food").setAttribute("data-value",Number(document.getElementById('food').getAttribute('data-value'))+1)
	// 	// console.log(Number(document.getElementById('food').getAttribute('data-value')))
	// 	// document.getElementById("food").innerHTML=Number(document.getElementById('food').getAttribute('data-value'))
	// });
  }


function animate() {
    // console.log("heheh")

	

	raycaster.setFromCamera( pointer, camera );
	requestAnimationFrame( animate );
	controls.update();
	renderer.render( scene, camera );
}
animate();

const socket=new WebSocket('ws://localhost:5000')

socket.addEventListener("open",function (event){
	console.log()
	socket.send("hello server")
	sendMessage()
})

socket.addEventListener("message",function (event){
	// console.log()
	// const text = await event.data.text();
	// if(event.data.type)
	try{
		console.log("message from server"+event.data[0])
		// var newCube = new THREE.Mesh( geometry, material );
		// newCube.position.x=event.data.split(",")[0]
		// newCube.position.y=event.data.split(",")[1]
		// newCube.position.z=event.data.split(",")[2]
		// scene.add(newCube)
	}catch (err){
		console.log("mmm")
	}
})

const sendMessage=()=>{
	// socket.send("hello from client")
	console.log(cube.position)
	socket.send([cube.position.x,cube.position.y,cube.position.z])
}
