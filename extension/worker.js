let webSocket = null;

function connect() {
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
    console.log(`websocket received message: ${event.data}`);
    if (event.data === "arcarum") {
      chrome.tabs.update({ url: "https://game.granbluefantasy.jp/#replicard" });
    }
  };
}

function disconnect() {
  if (webSocket == null) {
    return;
  }

  webSocket.close();
}

function keepAlive() {
  const keepAliveIntervalId = setInterval(
    () => {
      if (webSocket) {
        webSocket.send("keepalive");
      } else {
        clearInterval(keepAliveIntervalId);
      }
    },
    // Set the interval to 20 seconds to prevent the service worker from becoming inactive.
    5 * 1000,
  );
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (webSocket == null) {
    connect();
  }

  if (webSocket.readyState === 1) {
    if (message.message === "none") {
      webSocket.send("none");
    }

    if (message.message === "block") {
      webSocket.send("block");
    }
  }

  console.log(message.message);
});
