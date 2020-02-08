document.addEventListener("DOMContentLoaded", function(){
//   setTimeout(function(){
//     window.location.reload(1);
//  }, 5000);

});

function add_log_listeners() {
  var nodes = [...document.querySelectorAll('.log-button')]
  nodes.forEach(function(item){item.addEventListener('click', on_click_log, false)})
}

function on_click_log(event) {
  var thread_id = event.target.getAttribute('value');
  console.log("get log for "+thread_id);
}
