function sendMsg(msg) {
  chrome.runtime.sendMessage({
    message: msg,
  });
}

const target = document.querySelector(".wrapper").querySelector(".contents");

const observer_load = new MutationObserver(function (mutations) {
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

observer_load.observe(target, config);

function observeRaidSelector() {
  const raid_selector = document
    .querySelector(".wrapper")
    ?.querySelector(".contents")
    ?.querySelector(".cnt-raid")
    ?.querySelector(".cnt-raid-information");

  if (!raid_selector) {
    sendMsg("cnf-raid-information not loaded");
    return false;
  } else {
    const btn_attack = raid_selector.querySelector(".btn-attack-start");
    if (!btn_attack) {
      sendMsg("btn-attack-start not loaded");
    } else {
      sendMsg("btn-attack-start loaded");

      let initial_state = null;
      let is_display_on = null;

      const checkState = function () {
        const current_class = btn_attack.className;
        const has_display_on = current_class.includes("display-on");
        const has_display_off = current_class.includes("display-off");

        if (initial_state === null) {
          initial_state = current_class;
          is_display_on = has_display_on;

          if (has_display_on) {
            sendMsg("display-on");
          } else if (has_display_off) {
            sendMsg("display-off");
          }
          return;
        }

        if (has_display_on && !is_display_on) {
          sendMsg("display-on");
          is_display_on = true;
        } else if (has_display_off && is_display_on) {
          sendMsg("display-off");
          is_display_on = false;
        }

        initial_state = current_class;
      };

      const observer_attack = new MutationObserver(checkState);

      observer_attack.observe(btn_attack, {
        attributes: true,
        attributeFilter: ["class"],
      });
    }
  }
  sendMsg("cnf-raid-information loaded");

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
