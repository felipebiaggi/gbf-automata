function sendMsg(msg) {
  chrome.runtime.sendMessage({ message: msg });
}

const target = document.querySelector(".wrapper")?.querySelector(".contents");

if (target) {
  let inactivityTimeout;
  let lastState = null;
  let lastDisplay = target.style.display || "";

  const sendIfChanged = (state) => {
    if (lastState !== state) {
      lastState = state;
      sendMsg(state);
    }
  };

  const observerLoad = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (mutation.attributeName === "style") {
        const currentDisplay = target.style.display;

        if (currentDisplay !== lastDisplay) {
          lastDisplay = currentDisplay;
          sendIfChanged("none");

          clearTimeout(inactivityTimeout);
          inactivityTimeout = setTimeout(() => {
            sendIfChanged("block");
          }, 1000);
        }
      }
    }
  });

  observerLoad.observe(target, {
    attributes: true,
    attributeFilter: ["style"],
  });
}

function observeRaidSelector() {
  const raidSelector = document
    .querySelector(".wrapper")
    ?.querySelector(".contents")
    ?.querySelector(".cnt-raid");

  if (!raidSelector) return false;

  const btnAttack = raidSelector
    .querySelector(".cnt-raid-information")
    ?.querySelector(".btn-attack-start");

  if (btnAttack) {
    let isDisplayOn = null;

    const checkState = () => {
      const currentClass = btnAttack.className;
      const hasDisplayOn = currentClass.includes("display-on");
      const hasDisplayOff = currentClass.includes("display-off");

      if (isDisplayOn === null) {
        isDisplayOn = hasDisplayOn;

        if (hasDisplayOn) sendMsg("display-on");
        if (hasDisplayOff) sendMsg("display-off");
        return;
      }

      if (hasDisplayOn && !isDisplayOn) {
        sendMsg("display-on");
        isDisplayOn = true;
      } else if (hasDisplayOff && isDisplayOn) {
        sendMsg("display-off");
        isDisplayOn = false;
      }
    };

    const observerAttack = new MutationObserver(checkState);

    observerAttack.observe(btnAttack, {
      attributes: true,
      attributeFilter: ["class"],
    });
  }

  const btnEnd = raidSelector.querySelector(".prt-command-end");

  if (btnEnd) {
    const observerEnd = new MutationObserver(() => {
      if (btnEnd.style.cssText === "display: block;") {
        sendMsg("end-battle");
      }
    });

    observerEnd.observe(btnEnd, {
      attributes: true,
      attributeOldValue: true,
    });
  }

  return true;
}

if (!observeRaidSelector()) {
  const waitForRaidSelector = new MutationObserver(() => {
    if (observeRaidSelector()) {
      waitForRaidSelector.disconnect();
    }
  });

  waitForRaidSelector.observe(document.body, {
    childList: true,
    subtree: true,
  });
}

const resultObserver = new MutationObserver(() => {
  const resultSelector = document
    .querySelector(".wrapper")
    ?.querySelector(".contents")
    ?.querySelector(".cnt-result")
    ?.querySelector("#pop")
    ?.querySelector(".pop-usual")
    ?.querySelector(".prt-popup-footer")
    ?.querySelector(".btn-usual-ok");

  if (resultSelector) {
    requestAnimationFrame(() => {
      sendMsg("content-result");
    });
  }
});

resultObserver.observe(document.body, {
  childList: true,
  subtree: true,
});
