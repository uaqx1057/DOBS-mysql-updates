(function($) {
	
	"use strict";
	

	//Tabs Box
	if($('.tabs-box').length){
		$('.tabs-box .tab-buttons .tab-btn').on('click', function(e) {
			e.preventDefault();
			var target = $($(this).attr('data-tab'));
			
			if ($(target).is(':visible')){
				return false;
			}else{
				target.parents('.tabs-box').find('.tab-buttons').find('.tab-btn').removeClass('active-btn');
				$(this).addClass('active-btn');
				target.parents('.tabs-box').find('.tabs-content').find('.tab').fadeOut(0);
				target.parents('.tabs-box').find('.tabs-content').find('.tab').removeClass('active-tab');
				$(target).fadeIn(300);
				$(target).addClass('active-tab');
			}
		});
	}

	function headerStyle11StickyHeader() {
		if($('.ft11-main-header').length){
			var windowpos = $(window).scrollTop();
			var siteHeader = $('.ft11-main-header');
			var scrollLink = $('.scroll-to-top');

			var HeaderHight = $('.ft11-main-header').height();
			if (windowpos >= HeaderHight) {
				siteHeader.addClass('fixed-header');
				scrollLink.fadeIn(300);
			} else {
				siteHeader.removeClass('fixed-header');
				scrollLink.fadeOut(300);
			}

		}
	}

	function home11StickyAndMobileMenu(){
		//Submenu Dropdown Toggle
		if($('.ft11-main-header .navigation li.dropdown').length){
			$('.ft11-main-header .navigation li.dropdown').append('<div class="dropdown-btn"><span class="fa fa-angle-down"></span></div>');

			//Dropdown Button
			$('.ft11-main-header li.dropdown .dropdown-btn').on('click', function() {
				$(this).prev('ul').slideToggle(500);
			});

			//Megamenu Toggle
			$('.ft11-main-header .main-menu li.dropdown .dropdown-btn').on('click', function() {
				$(this).prev('.mega-menu').slideToggle(500);
			});

			//Disable dropdown parent link
			$('.ft11-main-header .navigation li.dropdown > a,.hidden-bar .side-menu li.dropdown > a').on('click', function(e) {
				e.preventDefault();
			});
		}

		//Mobile Nav Hide Show
		if($('.mobile-menu').length){

		$('.mobile-menu .menu-box').mCustomScrollbar();

		var mobileMenuContent = $('.ft11-main-header .nav-outer .main-menu').html();
		$('.mobile-menu .menu-box .menu-outer').append(mobileMenuContent);
		$('.sticky-header .main-menu').append(mobileMenuContent);

		//Dropdown Button
		$('.mobile-menu li.dropdown .dropdown-btn').on('click', function() {
			$(this).toggleClass('open');
			$(this).prev('ul').slideToggle(500);
		});
		//Menu Toggle Btn
		$('.mobile-nav-toggler').on('click', function() {
			$('body').addClass('mobile-menu-visible');
		});

		//Menu Toggle Btn
		$('.mobile-menu .menu-backdrop,.mobile-menu .close-btn').on('click', function() {
			$('body').removeClass('mobile-menu-visible');
		});

	}
	}
	


/* ==========================================================================
   When document is Scrollig, do
   ========================================================================== */
	
	$(window).on('scroll', function() {
		headerStyle11StickyHeader();

	});
	
/* ==========================================================================
   When document is loading, do
   ========================================================================== */
	
	$(window).on('load', function() {
		home11StickyAndMobileMenu();
	});	

})(window.jQuery);