function sendMsg(msg){
  chrome.runtime.sendMessage({
    message: msg
  })
}

const target = document.querySelector('.img-load');

const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (target.style.cssText === 'display: none;'){ 
        sendMsg("Loading Finished.")
      }
    });

});

const config = { attributes: true, attributeOldValue: true };

observer.observe(target, config);

