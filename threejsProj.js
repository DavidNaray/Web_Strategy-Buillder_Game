const express=require("express")
const path=require("path")
const WebSocket=require("ws")
const app=express()

const server=require("http").createServer(app)

const wss=new WebSocket.Server({server})

wss.on('connection', function connection(ws) {
    console.log("new connection")
    // ws.on('error', console.error);
    ws.send('something');
    ws.emit
    ws.on('message', function message(data,isBinary) {
      console.log('received: %s', data);
      wss.clients.forEach(function each(client) {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(data,{ binary: isBinary });
        }
      });
    });
  
    
});
server.listen(5000)

app.use(express.static("./threejsFold"))

app.get('/',(req,res)=>{
    res.sendFile(path.resolve(__dirname,"./threejsFold/ThreeIndex.html"))
})

app.get('/main.js',(req,res)=>{
    console.log("hiiii")
    res.sendFile(path.join(__dirname,'..','main.js'))
      // path.resolve(__dirname,"../main.js"))
})

app.get('/threejsFold/basicAssets.glb',(req,res)=>{
    // console.log("hiiii")
    res.sendFile(path.resolve(__dirname,"./threejsFold/basicAssets.glb"))
})

// app.get('/about',(req,res)=>{
//     res.send("about page")
// })

// app.all("*",(req,res)=>{
//     res.status(404).send('<h1>not found</h1>')
// })

// app.listen(5000,()=>{
//     console.log("server is up and running")
// })
