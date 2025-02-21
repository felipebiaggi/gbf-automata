function sendMsg(msg) {
  chrome.runtime.sendMessage({
    message: msg,
  });
}

const target = document.querySelector(".wrapper").querySelector(".contents");

const observer = new MutationObserver(function (mutations) {
  mutations.forEach(function () {
    if (target.style.cssText === "display: none;") {
      sendMsg("block");
    }

    if (target.style.cssText === "display: block;") {
      sendMsg("none");
    }
  });
});

const config = { attributes: true, attributeOldValue: true };

observer.observe(target, config);
