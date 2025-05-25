// server.js
const express = require("express");
const http = require("http");
const app = express();
const server = http.createServer(app);
const io = require("socket.io")(server, { cors: { origin: "*" } });

io.on("connection", socket => {
  socket.on("join", roomID => {
    socket.join(roomID);
    socket.to(roomID).emit("user-joined", socket.id);
    socket.on("signal", data => {
      io.to(data.to).emit("signal", { from: socket.id, signal: data.signal });
    });
  });
});

server.listen(5000, () => console.log("Server running on http://localhost:5000"));
