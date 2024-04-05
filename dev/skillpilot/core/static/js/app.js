// make flash messages disappear after a given time delay

let message = document.querySelector('#flash-message')

// make each flash message disappear after 5 seconds
setTimeout(function() {
    message.style.display = "none";
}, 3000);
