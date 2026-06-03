/*
	Template  Name: Prohub - Multipurpose $ Corporate Product Landing Page Template
	Template URI: static.crazycafe.net/crazycafe/prohub
	Description: This is a Multipurpose $ Corporate Product Landing Page Template
	Author: CrazyCafe
	Author URI: support@crazycafe.net
	Version: 1.0  
*/
/*================================================
[  Table of contents  ]
================================================
	01. jQuery MeanMenu Active
	02. Drone Testimonial
	03. Bike Testimonial
	04. Headphone Testimonial Carousel
	05. Headphone Gallery area
	06. Live cam Testimonial Carousel
	07. App Testimonial Carousel
	08. App Logo Carousel
	09. Watch hero Carousel
	10. App Screenshot
	11. one page js active
	12. Venobox Active
	13. Sticky Header
	14. Wow Active
/*

/*

======================================
[ End table content ]
======================================*/

(function ($) {
 "use strict";

    jQuery(document).ready(function($){
		
		/* ==== 01. jQuery MeanMenu Active ==== */
		if ($.fn.meanmenu) {
			$('.bizes-nav').meanmenu({
				meanMenuContainer: '.mobile-menu-area', // render menu mobile di sini
				meanScreenWidth:  '991',                 // aktif di <= 991px
				meanRevealPosition: 'right',             // burger di kanan
				meanDisplay: 'block',
				removeElements: '' ,
				meanMenuClose: '✕',
				// ikon burger: 3 bar
				meanMenuOpen: '<span></span><span></span><span></span>'
			});
		}
		
		/* ==== 02. Drone Testimonial ==== */
		 if ($.fn.owlCarousel) {
		 	$('.drone-testimonial-wrap').owlCarousel({
		 		autoplay:false,
		 		items:1,
		 		loop:true,
		 		autoplayHoverPause: false,
				smartSpeed: 500,
		 		margin:0,
				nav:true,
		 		navText:['<i class="fa fa-long-arrow-left"></i>','<i class="fa fa-long-arrow-right"></i>'],
			dots:true,
		 	}) 

		 	/* ==== 03. Bike Testimonial ==== */
			$('.bike-testimonial-carousle').owlCarousel({
				autoplay:false,
				items:1,
				loop:true,
				autoplayHoverPause: false,
				smartSpeed: 500,
				margin:0,
				nav:true,
				navText:['<i class="fa fa-long-arrow-left"></i>','<i class="fa fa-long-arrow-right"></i>'],
				dots:true,
			}) 

			/* ==== 04. Headphone Testimonial Carousel ==== */
			
				$('.music-testimonial-wrap').owlCarousel({
					autoplay:false,
					items:2,
					loop:true,
					autoplayHoverPause: false,
					smartSpeed: 500,
					margin:30,
					nav:true,
					navText:['<i class="fa fa-long-arrow-left"></i>','<i class="fa fa-long-arrow-right"></i>'],
					dots:true,
					responsiveClass:true,
					responsive:{
						0:{
							items:1,
						},
						600:{
							items:2,
						},
						768:{
							items:2,
						},
						1000:{
							items:2,
						}
					}
				}) 
		/* ==== 05. Headphone Gallery area ==== */
			$('.music-gallery-wrap').owlCarousel({
				autoplay:false,
				items:4,
				loop:true,
				autoplayHoverPause: false,
				smartSpeed: 500,
				margin:30,
				center:true,
				nav:false,
				navText:['<i class="fa fa-long-arrow-left"></i>','<i class="fa fa-long-arrow-right"></i>'],
				dots:false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					600:{
						items:2,
					},
					768:{
						items:3,
					},
					1000:{
						items:4,
					}
				}
			})

		/* ==== 06. Live cam Testimonial Carousel ==== */
			$('.cam-testimonial-wrap').owlCarousel({
				autoplay:false,
				items:3,
				loop:true,
				autoplayHoverPause: false,
				smartSpeed: 500,
				margin:30,
				nav:false,
				navText:['<i class="fa fa-long-arrow-left"></i>','<i class="fa fa-long-arrow-right"></i>'],
				dots:false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					600:{
						items:2,
					},
					768:{
						items:2,
					},
					1000:{
						items:3,
					}
				}
			}) 

			/* ==== 07. App Testimonial Carousel ==== */
			$('.apptestimonial-wrap').owlCarousel({
				autoplay:false,
				items:1,
				loop:true,
				autoplayHoverPause: false,
				smartSpeed: 500,
				margin:30,
				nav:true,
				navText:['<i class="fa fa-long-arrow-left"></i>','<i class="fa fa-long-arrow-right"></i>'],
				dots:false,
			}) 


			/* ==== 08. App Logo Carousel ==== */
			$('.app-logocarousel-wrap').owlCarousel({
				autoplay:false,
				items:4,
				loop:true,
				autoplayHoverPause: false,
				smartSpeed: 500,
				margin:30,
				nav:false,
				navText:['<i class="fa fa-long-arrow-left"></i>','<i class="fa fa-long-arrow-right"></i>'],
				dots:false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					600:{
						items:2,
					},
					768:{
						items:3,
					},
					1000:{
						items:4,
					}
				}
			}) 

			/* ==== 09. Watch hero ==== */
			$('.watch-img-carousel-wrap').owlCarousel({
				autoplay:true,
				items:1,
				loop:true,
				autoplayHoverPause: false,
				smartSpeed: 500,
				margin:0,
				nav:false,
				dots:false,
			}) 

			/* ==== 10. App Screenshot ==== */
			$('.screenshot-wrap').owlCarousel({
				autoplay:false,
				items:4,
				loop:true,
				autoplayHoverPause: false,
				smartSpeed: 500,
				autoWidth: false,
				margin:5,
				center:true,
				nav:true,
				navText:['<i class="fa fa-long-arrow-left"></i>','<i class="fa fa-long-arrow-right"></i>'],
				dots:false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					600:{
						items:2,
					},
					768:{
						items:3,
					},
					1000:{
						items:4,
					}
				}
			}) 

		 }

		/*====  11. one page js active (desktop + mobile) =====*/
		$('.main-menu-wrap > .bizes-nav > ul.menu > li > a, .mean-nav ul li a').on("click", function(e) {
			//Toggle Class (khusus desktop)
			$(".active").removeClass("active");
			$(this).closest('li').addClass("active");

			var href = $(this).attr('href');
			if (href && href.startsWith('#') && $(href).length) {
				e.preventDefault();
				$('html, body').stop().animate({
				scrollTop: $(href).offset().top - 100
				}, 1000);
			}

			// tutup menu mobile setelah klik
			if ($('.meanmenu-reveal').is(':visible')) {
				$('.meanmenu-reveal').trigger('click');
			}
		});

		// Tambahan khusus untuk logo
		$('.logo a[href^="#"]').on("click", function(event) {
			event.preventDefault();
			var target = $(this).attr("href");
			if ($(target).length) {
				$('html, body').stop().animate({
					scrollTop: $(target).offset().top - 100
				}, 1000);
			}
		});
		
		$('nav.bizes-nav').meanmenu({
		meanMenuContainer: '.mobile-menu-area',   // tempat render menu mobile
		meanRevealPosition: 'right',              // dari awal di kanan
		meanRevealPositionDistance: '12px',       // jarak dari tepi kanan
		meanMenuClose: '×',                       // simbol close
		meanMenuCloseSize: '28px'
		});

		/* ==== 12. Venobox Active ==== */	
			$('.venobox').venobox(); 

		/* ==== 11. ScrollUp ==== */
		$.scrollUp({
			scrollText: '<i class="fa fa-arrow-up"></i>',
			easingType: 'linear',
			scrollSpeed: 900,
			animation: 'fade'
		}); 
	
    });
	
	/* ==== 13. Sticky Header ==== */
	$(window).on('scroll',function() {
		var header_ = $(".header-area.primary-header");

	  if ($(this).scrollTop() > 1){  
		header_.addClass("scroll-header");
	    }
	  else{
		header_.removeClass("scroll-header");
	    }
	}); 
	
	/* ==== 14. Preloader ==== */
	$(window).on('load',function(){
		jQuery(".preloader-wrap").fadeOut(500);
		/* ==== 15. Wow active ==== */
		new WOW().init();
	});
	
	
})(jQuery); 

document.addEventListener("DOMContentLoaded", function() {
// ----------------------------------------------------
// FITUR 1: SLIDESHOW RANDOM
// ----------------------------------------------------
const images = document.querySelectorAll('.slideshow-img');

images.forEach(imgElement => {
	const imgUrls = JSON.parse(imgElement.getAttribute('data-images'));

	if (imgUrls && imgUrls.length > 1) {
	let currentIndex = 0;
	
	function changeImageRandomly() {
		const randomTime = Math.floor(Math.random() * (3000 - 1000 + 1)) + 1000;

		setTimeout(() => {
		currentIndex = (currentIndex + 1) % imgUrls.length;
		imgElement.src = imgUrls[currentIndex];
		changeImageRandomly();
		}, randomTime);
	}
	changeImageRandomly();
	}
});

// ----------------------------------------------------
// FITUR 2: POPUP/MODAL KETIKA DIKLIK
// ----------------------------------------------------
const modal = document.getElementById("imageModal");
const modalImg = document.getElementById("modalImage");
const modalLink = document.getElementById("modalLink");
const modalText = document.getElementById("modalCaption");
const closeBtn = document.querySelector(".close-modal");

// Ambil semua tag <a> yang memiliki class popup-trigger
const triggers = document.querySelectorAll('.popup-trigger');

triggers.forEach(trigger => {
	trigger.addEventListener('click', function(e) {
	// Mencegah halaman langsung pindah ke link tujuan
	e.preventDefault(); 
	
	// Cari gambar yang ADA di dalam link yang diklik
	const currentImg = this.querySelector('img');
	
	// Tampilkan modal (Ubah display menjadi flex)
	modal.style.display = "flex";
	
	// Tembak src gambar yang SEDANG TAMPIL SAAT INI ke dalam popup
	modalImg.src = currentImg.src; 
	
	// Isi teks dan link-nya
	modalText.innerText = this.getAttribute('data-name');
	modalLink.href = this.getAttribute('data-url');
	});
});

// Fitur untuk menutup popup ketika tombol X diklik
closeBtn.addEventListener('click', () => {
	modal.style.display = "none";
});

// Fitur untuk menutup popup ketika mengklik area gelap di luar gambar
window.addEventListener('click', (e) => {
	if (e.target === modal) {
	modal.style.display = "none";
	}
});
});