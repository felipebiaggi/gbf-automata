let webSocket = null;
let keepAliveIntervalId = null;

const MessageType = Object.freeze({
  INTERNAL: "INTERNAL",
  EXTERNAL: "EXTERNAL",
});

const MessageAction = Object.freeze({
  STOP: "STOP",
  MOVE: "MOVE",
  UPDATE: "UPDATE",
});

class Message {
  constructor({ message_type, message_action, extra }) {
    this.messageType = message_type;
    this.messageAction = message_action;
    this.extra = extra;
  }

  static fromJson(jsonString) {
    try {
      const object = JSON.parse(jsonString);

      if (!Object.values(MessageType).includes(object.message_type)) {
        throw new Error(`Invalid message_type: ${object.message_type}`);
      }

      if (!Object.values(MessageAction).includes(object.message_action)) {
        throw new Error(`Invalid message_action: ${object.message_action}`);
      }

      return new Message(object);
    } catch (err) {
      throw new Error("Invalid JSON format.");
    }
  }
}

function connect() {
  if (webSocket && webSocket.readyState !== WebSocket.CLOSED) {
    console.log("WebSocket já conectado.");
    return;
  }

  webSocket = new WebSocket("ws://localhost:12000");

  webSocket.onopen = () => {
    console.log("Connection Open.");
    keepAlive();
  };

  webSocket.onclose = () => {
    console.log("Connection Closed.");
    webSocket = null;
  };

  webSocket.onmessage = (event) => {
    const message = Message.fromJson(event.data);
    console.log("WebSocket received message:", message);

    if (message.messageAction === MessageAction.MOVE) {
      console.log("ACTION.MOVE");
      chrome.tabs.update({ url: message.extra });
    }
  };
}

function disconnect() {
  if (!webSocket) return;
  webSocket.close();
}

function keepAlive() {
  if (keepAliveIntervalId) {
    return;
  }

  keepAliveIntervalId = setInterval(() => {
    if (webSocket && webSocket.readyState === WebSocket.OPEN) {
      webSocket.send("keepalive");
    } else {
      clearInterval(keepAliveIntervalId);
      keepAliveIntervalId = null;
    }
  }, 5000);
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => { 
  if (!webSocket || webSocket.readyState !== WebSocket.OPEN) {
    connect();
  }

  if(["none", "block", "display-on", "display-off", "end-battle"].includes(message.message)){
    webSocket.send(message.message)
  }

  console.log(`Message: <${message.message}>`)
});
