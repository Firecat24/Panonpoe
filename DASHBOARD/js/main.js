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
            $('.navbar').css('background', '#212529');
        } else {
            // Kembalikan ke transparan/gradient semula
            $('.navbar').css(
                'background',
                'linear-gradient(135deg, rgba(44, 51, 56, 0) 0%, rgba(44, 51, 56, 0) 100%)'
            );
        }
    });
});