// make flash messages disappear after a given time delay

let message = document.querySelector('#flash-message')

// make each flash message disappear after 5 seconds
setTimeout(function() {
    message.style.display = "none";
}, 5000);


// bootstrap client-side form validation
(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
        }

        form.classList.add('was-validated')
    }, false)
    })
})()