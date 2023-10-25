function sendMsg(msg){
  chrome.runtime.sendMessage({
    message: msg
  })
}

const target = document.querySelector('.img-load');

const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function() {
      if (target.style.cssText === 'display: none;'){ 
        sendMsg("none")
      }
      
      if (target.style.cssText === 'display: block;'){
        sendMsg("block")
      }

    });
});

const config = { attributes: true, attributeOldValue: true };

observer.observe(target, config);

