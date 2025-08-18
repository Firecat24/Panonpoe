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

document.getElementById("confirmDelete").onclick = function(event) {
    event.preventDefault();
    var result = confirm("Apakah Anda yakin ingin menghapus postingan ini?");
    if (result) {
        let post_id = this.getAttribute("post_id");
        window.location.href =`/hapus_postingan/${post_id}`;
        alert("Hapus berhasil");
    } else {
        alert("Tidak jadi dihapus");
    }
}