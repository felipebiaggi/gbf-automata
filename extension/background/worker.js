import './lib/socket.io.js';

const socket = io('127.0.0.1:65432', {
  jsonp: false,
});

socket.on('connect', ()=>{
  console.log("Connection successful")
});

socket.on("connect_error", (error) => {
  console.log(`Connection error: <${error}>`)
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log(socket);
    socket.emit("Teste")
  });
