setTimeout(function() {
    var alertElements = document.querySelectorAll('.alert');
    alertElements.forEach(function(alertElement) {
        alertElement.classList.remove('show');
        alertElement.classList.add('d-none');
        setTimeout(function() { alertElement.remove(); }, 1000);
    });
}, 5000);