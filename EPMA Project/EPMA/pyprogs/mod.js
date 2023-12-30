// This program pushes notifications
const io = require("socket.io-client")
const io3000 = io.connect("http://localhost:3000");

io3000.emit("_mod.js",process.argv[2]);

io3000.on("die",(data)=>{
    process.exit();
});