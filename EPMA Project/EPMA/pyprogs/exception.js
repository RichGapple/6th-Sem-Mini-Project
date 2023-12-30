// This program pushes exceptions
const io = require("socket.io-client")
const io30001 = io.connect("http://localhost:3000");

io30001.emit("exception_",process.argv[2]);

io30001.on("die_",(data)=>{
    process.exit();
});