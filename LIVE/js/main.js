$(document).ready(function () {
    "use strict";

    /* =======================
       Smooth Scrolling
    ======================== */
    if ($.fn.smoothScroll) {
        $('html').smoothScroll(800);
    }

    /* =======================
       WOW Animations
    ======================== */
    if (typeof WOW !== 'undefined') {
        new WOW().init({ mobile: true });
    }

    /* =======================
       Portfolio (Isotope)
    ======================== */
    (function initIsotopePortfolio() {
        var $grid = $('.grid');

        // Pastikan "Semua" mengarah ke .show-in-all
        // <button data-filter=".show-in-all" class="active">Semua</button>

        // Tunggu gambar ter-load supaya layout rapi
        if ($.fn.imagesLoaded && $.fn.isotope) {
            $grid.imagesLoaded(function () {
                // Init Isotope
                $grid.isotope({
                    itemSelector: '.grid-item',
                    layoutMode: 'fitRows'
                });

                // Default: hanya tampilkan 1 thumbnail per kategori
                $grid.isotope({ filter: '.show-in-all' });

                // Filter buttons
                $('.filter-button-group').on('click', 'button', function () {
                    var filterValue = $(this).attr('data-filter');
                    $grid.isotope({ filter: filterValue });

                    // tombol active state
                    $(this).addClass('active').siblings().removeClass('active');

                    // jaga-jaga re-layout
                    setTimeout(function(){ $grid.isotope('layout'); }, 0);
                });
            });

            // Relayout saat window resize (opsional tapi membantu)
            $(window).on('resize', function () {
                if ($grid.data('isotope')) {
                    $grid.isotope('layout');
                }
            });
        }
    })();



    /* =======================
       Loader
    ======================== */
    $('.se-pre-con').fadeOut('slow');

    /* =======================
       Navbar background on scroll
    ======================== */
    $(window).on('scroll', function () {
        var top = $(window).scrollTop();
        if (top >= 100) {
            $('.navbar').css({
            'background': 'rgba(10, 15, 20, 0.75)',
            'backdrop-filter': 'blur(16px)',
            '-webkit-backdrop-filter': 'blur(16px)',
            'box-shadow': '0 10px 30px rgba(0,0,0,0.25)'
        });
        } else {
            // Kembalikan ke transparan/gradient semula
            $('.navbar').css({
            'background': 'rgba(10, 15, 20, 0.45)',
            'box-shadow': 'none'
        });
        }
    });
});

// Refresh gambar otomatis setiap 10 detik
setInterval(function() {
    var img = document.getElementById('allsky-cam');
    // Tambahkan timestamp agar browser tidak memuat cache lama
    img.src = 'image.jpg?t=' + new Date().getTime();
}, 3000);

/* =======================
   Archive Tabs
======================== */

const archiveButtons =
    document.querySelectorAll('.archive-btn');

const archiveContents =
    document.querySelectorAll('.archive-content');

archiveButtons.forEach(button => {

    button.addEventListener('click', () => {

        const target =
            button.getAttribute('data-target');

        archiveButtons.forEach(btn => {
            btn.classList.remove('active');
        });

        archiveContents.forEach(content => {
            content.classList.remove('active');
        });

        button.classList.add('active');

        document
            .getElementById(target)
            .classList
            .add('active');

    });

});

document.addEventListener("DOMContentLoaded", function () {
    // Logika Perpindahan Tab Menu
    const tabButtons = document.querySelectorAll(".archive-btn");
    const tabContents = document.querySelectorAll(".archive-content");

    tabButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-target");
            tabButtons.forEach(btn => btn.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));
            button.classList.add("active");
            document.getElementById(targetId).classList.add("active");
        });
    });

    // Logika Pop-up Pemutar Video & Gambar Pintar
    const modal = document.getElementById("videoPopupModal");
    const modalVideo = document.getElementById("popupVideoPlayer");
    const modalImage = document.getElementById("popupImageViewer");
    const closeBtn = document.querySelector(".video-popup-close");
    const videoCards = document.querySelectorAll(".video-item-card");

    videoCards.forEach(card => {
        card.addEventListener("click", () => {
            const fileSrc = card.getAttribute("data-file-src"); // Wajib data-file-src
            const fileType = card.getAttribute("data-file-type"); // Wajib data-file-type
            
            if (fileSrc) {
                modalVideo.style.display = "none";
                modalImage.style.display = "none";

                if (fileType === "video") {
                    modalVideo.src = fileSrc;
                    modalVideo.load();
                    modalVideo.style.display = "block";
                    modal.classList.add("show");
                    modalVideo.play().catch(err => console.log("Autoplay blocked"));
                } else if (fileType === "image") {
                    modalImage.src = fileSrc;
                    modalImage.style.display = "block";
                    modal.classList.add("show");
                }
            }
        });
    });

    function closeModal() {
        modal.classList.remove("show");
        modalVideo.pause();
        modalVideo.src = "";
        modalImage.src = "";
    }

    closeBtn.addEventListener("click", closeModal);
    modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });
});

// Logika Perpindahan Tab Menu Otomatis (Mendukung Pagination Reload)
const tabButtons = document.querySelectorAll(".archive-btn");
const tabContents = document.querySelectorAll(".archive-content");

// Cek dulu dari URL, variabel halaman mana yang aktif saat ini
const urlParams = new URLSearchParams(window.location.search);
let activeTabId = "timelapse-content"; // Default awal

if (urlParams.has('p_startrail')) {
    activeTabId = "startrail-content";
} else if (urlParams.has('p_keogram')) {
    activeTabId = "keogram-content";
}

// Set tab aktif secara otomatis sesuai halaman yang sedang dibuka
tabButtons.forEach(btn => {
    if(btn.getAttribute("data-target") === activeTabId) {
        btn.classList.add("active");
    } else {
        btn.classList.remove("active");
    }
});

tabContents.forEach(content => {
    if(content.getAttribute("id") === activeTabId) {
        content.classList.add("active");
    } else {
        content.classList.remove("active");
    }
});

// Jalankan fungsi klik manual seperti biasa agar tombol navigasi tab tetap bisa diklik bebas
tabButtons.forEach(button => {
    button.addEventListener("click", () => {
        const targetId = button.getAttribute("data-target");
        tabButtons.forEach(btn => btn.classList.remove("active"));
        tabContents.forEach(content => content.classList.remove("active"));
        button.classList.add("active");
        document.getElementById(targetId).classList.add("active");
    });
});

// --- AUTO GENERATE VIDEO THUMBNAIL VIA CANVAS ---
const imagesNeedThumb = document.querySelectorAll(".need-thumb");

imagesNeedThumb.forEach(img => {
    const videoUrl = img.getAttribute("data-video");
    
    // Buat objek video bayangan di memori browser
    const video = document.createElement("video");
    video.src = videoUrl;
    video.preload = "metadata";
    video.muted = true;
    video.playsInline = true;

    // Saat browser berhasil membaca info frame video
    video.addEventListener("loadeddata", function () {
        // Lompat ke detik ke-1 agar covernya tidak menangkap layar hitam/gelap di detik ke-0
        video.currentTime = 1; 
    });

    // Setelah browser berhasil menggeser timeline video ke detik 1
    video.addEventListener("seeked", function () {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Mengubah gambar canvas menjadi format gambar URL (Base64)
        const imageUrl = canvas.toDataURL("image/jpeg");
        
        // Suntikkan gambarnya langsung menggantikan img/livecam/keogram.jpg
        img.src = imageUrl;
        img.classList.remove("need-thumb"); // Hapus class penanda agar tidak terjadi loop berulang
    });
});