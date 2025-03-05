function sendMsg(msg) {
  chrome.runtime.sendMessage({
    message: msg,
  });
}

const target = document.querySelector("#loading").querySelector(".img-load");

let lastDisplay = target.style.display || "";

const observer_load = new MutationObserver(function () {
  const currentDisplay = target.style.display;

  if (currentDisplay !== lastDisplay) {
    lastDisplay = currentDisplay;

    if (currentDisplay === "none") {
      sendMsg("block");
    } else if (currentDisplay === "block") {
      sendMsg("none");
    }
  }
});

const config = { attributes: true, attributeOldValue: true };

observer_load.observe(target, config);

function observeRaidSelector() {
  const raid_selector = document
    .querySelector(".wrapper")
    ?.querySelector(".contents")
    ?.querySelector(".cnt-raid");

  if (!raid_selector) {
    sendMsg("cnf-raid-information not loaded");
    return false;
  } else {
    const btn_attack = raid_selector
      .querySelector(".cnt-raid-information")
      .querySelector(".btn-attack-start");
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

    const btn_end = raid_selector.querySelector(".prt-command-end");

    if (!btn_end) {
      sendMsg("prt-command-end not loaded");
    } else {
      sendMsg("prt-command-end loaded");

      const observer_end = new MutationObserver(function (mutations) {
        if (btn_end.style.cssText === "display: block;") {
          sendMsg("end-battle");
        }
      });

      observer_end.observe(btn_end, {
        attributes: true,
        attributeOldValue: true,
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

(function () {
  let logCount = 1;
  let ultimoElementoAlterado = null;
  let observerTimeout;

  // ✅ Criação do painel visual fixo
  const painel = document.createElement("div");
  painel.id = "meuConsole";
  painel.style.position = "fixed";
  painel.style.top = "10px";
  painel.style.right = "10px";
  painel.style.width = "1000px";
  painel.style.maxHeight = "600px";
  painel.style.overflowY = "auto";
  painel.style.background = "#111";
  painel.style.color = "#0f0";
  painel.style.padding = "10px";
  painel.style.fontFamily = "monospace";
  painel.style.fontSize = "14px";
  painel.style.zIndex = "9999";
  painel.style.border = "2px solid #0f0";
  document.body.appendChild(painel);

  // ✅ Botão de limpar
  const btnClear = document.createElement("button");
  btnClear.textContent = "🧹 Limpar Logs";
  btnClear.style.position = "fixed";
  btnClear.style.top = "10px";
  btnClear.style.right = "1020px";
  btnClear.style.padding = "5px 10px";
  btnClear.style.background = "#0f0";
  btnClear.style.color = "#111";
  btnClear.style.border = "none";
  btnClear.style.cursor = "pointer";
  document.body.appendChild(btnClear);

  btnClear.onclick = () => {
    painel.innerHTML = "✅ Console limpo.\n";
    logCount = 1;
  };

  // ✅ Função para logar e enviar mensagens
  function logPainel(message) {
    sendMsg(message);
    const now = new Date().toLocaleTimeString();
    const linha = document.createElement("div");
    linha.textContent = `${logCount++}. [${now}] ${message}`;
    painel.appendChild(linha);
    painel.scrollTop = painel.scrollHeight;
  }

  function descreverElemento(elemento) {
    if (!elemento.tagName) return "nó de texto";
    const tag = elemento.tagName.toLowerCase();
    const id = elemento.id ? `#${elemento.id}` : "";
    const classe = elemento.className
      ? `.${elemento.className.trim().replace(/\s+/g, ".")}`
      : "";
    return `<${tag}${id}${classe}>`;
  }

  function ehElementoDoPainel(elemento) {
    return painel.contains(elemento) || btnClear.contains(elemento);
  }

  // ✅ MutationObserver para detectar estabilidade do DOM
  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (ehElementoDoPainel(mutation.target)) continue;

      if (mutation.type === "childList") {
        mutation.addedNodes.forEach((node) => {
          if (
            node.nodeType === Node.ELEMENT_NODE &&
            !ehElementoDoPainel(node)
          ) {
            ultimoElementoAlterado = node;
            logPainel(
              `➕ Adicionado ${descreverElemento(node)} com conteúdo: "${node.textContent.trim().slice(0, 200)}"`,
            );
          }
        });
        mutation.removedNodes.forEach((node) => {
          if (
            node.nodeType === Node.ELEMENT_NODE &&
            !ehElementoDoPainel(node)
          ) {
            ultimoElementoAlterado = node;
            logPainel(
              `➖ Removido ${descreverElemento(node)} com conteúdo: "${node.textContent.trim().slice(0, 200)}"`,
            );
          }
        });
      } else if (mutation.type === "attributes") {
        ultimoElementoAlterado = mutation.target;
        const attributeName = mutation.attributeName;
        const oldValue = mutation.oldValue;
        const newValue = mutation.target.getAttribute(attributeName);
        logPainel(
          `🔄 Alterado atributo "${attributeName}" em ${descreverElemento(mutation.target)} de "${oldValue}" para "${newValue}"`,
        );
      } else if (mutation.type === "characterData") {
        const parent = mutation.target.parentNode;
        if (parent && !ehElementoDoPainel(parent)) {
          ultimoElementoAlterado = parent;
          logPainel(
            `✏️ Texto alterado em ${descreverElemento(parent)} de "${mutation.oldValue}" para "${mutation.target.data}"`,
          );
        }
      }
    }

    clearTimeout(observerTimeout);
    observerTimeout = setTimeout(() => {
      logPainel("✅ DOM estabilizado, sem alterações por 2 segundos.");
    }, 2000);
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
    characterData: true,
    attributeOldValue: true,
    characterDataOldValue: true,
  });

  logPainel("✅ Monitoramento de alterações no DOM iniciado.");
})();
