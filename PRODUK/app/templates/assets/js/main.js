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
			jQuery('.bizes-nav').meanmenu();	
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

    	/*====  11. one page js active =====*/
        $('.main-menu-wrap > .bizes-nav > ul.menu > li > a').on("click", function() {
            //Toggle Class
            $(".active").removeClass("active");
            $(this).closest('li').addClass("active");
            var theClass = $(this).attr("class");
            $('.' + theClass).parent('li').addClass('active');
            //Animate
            $('html, body').stop().animate({
                scrollTop: $($(this).attr('href')).offset().top - 100
            }, 1000);
            return false;
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