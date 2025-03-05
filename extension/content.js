function sendMsg(msg) {
  chrome.runtime.sendMessage({
    message: msg,
  });
}

// const target = document.querySelector(".wrapper").querySelector(".contents");

// const observer_load = new MutationObserver(function (mutations) {
//  mutations.forEach(function () {
//    if (target.style.cssText === "display: none;") {
//      sendMsg("block");
//    }

//    if (target.style.cssText === "display: block;") {
//      sendMsg("none");
//    }
//  });
// });

// const config = { attributes: true, attributeOldValue: true };

// observer_load.observe(target, config);

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

      let last_state = null;

      const checkState = () => {
        const current_class = btn_attack.className;
        const is_display_on = current_class.includes("display-on");
        const is_display_off = current_class.includes("display-off");

        if (last_state === null) {
          last_state = is_display_on
            ? "on"
            : is_display_off
              ? "off"
              : "unknown";
          if (last_state === "on") {
            sendMsg("🟢 Estado inicial: ATIVADO (display-on).");
          } else if (last_state === "off") {
            sendMsg("🔴 Estado inicial: DESATIVADO (display-off).");
          } else {
            sendMsg(`ℹ️ Estado inicial desconhecido: ${current_class}`);
          }
          return;
        }

        if (last_state === "off" && is_display_on) {
          sendMsg(
            "🟢 Botão mudou de DESATIVADO (display-off) para ATIVADO (display-on).",
          );
          last_state = "on";
        } else if (last_state === "on" && is_display_off) {
          sendMsg(
            "🔴 Botão mudou de ATIVADO (display-on) para DESATIVADO (display-off).",
          );
          last_state = "off";
        }
      };

      checkState();

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
