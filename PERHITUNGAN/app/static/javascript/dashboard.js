function closeNavbar() {
    var navbarToggler = document.querySelector('.navbar-toggler');
    navbarToggler.classList.add('collapsed');
    
    var navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.remove('show');
}
function fetchImage() {
    fetch('/get_image')
        .then(response => response.json())
        .then(data => {
            document.getElementById('dynamicImage').src = '/static/gambar_upload/' + data.gambar;
        })
        .catch(error => console.error('Error:', error));
}

setInterval(fetchImage, 5000);

fetchImage();

document.getElementById("logout_user").onclick = function(event) {
    event.preventDefault();
    var validasi = confirm("Apakah kamu ingin logout ?")
    if (validasi) {
    window.location.href = '/logout';
    alert("Logout berhasil")
    }else{
    alert("Selamat datang kembali")
    }
}
setTimeout(function() {
    var alertElement = document.getElementById('alert');
    if (alertElement) {
        alertElement.classList.remove('show');
        alertElement.classList.add('hide');
        setTimeout(function() { alertElement.remove(); }, 500);
    }
}, 3000);