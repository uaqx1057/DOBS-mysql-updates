/* -----------------------------------------------------------------------------
File:           JS Core
Version:        1.0
Last change:    00/00/00 
-------------------------------------------------------------------------------- */
(function($) {

	"use strict";

	/**
	 * Logistic Sticky Header
	 */
	jQuery(window).on('scroll', function() {
		if (jQuery(window).scrollTop() > 250) {
			jQuery('.tl-thx-header-section').addClass('sticky-on')
		} else {
			jQuery('.tl-thx-header-section').removeClass('sticky-on')
		}
	});

	/**
	 * Logistic Sidebar Nav
	 */
	jQuery(document).ready(function (o) {
		0 < o(".navSidebar-button").length &&
		o(".navSidebar-button").on("click", function (e) {
			e.preventDefault(), e.stopPropagation(), o(".info-group").addClass("isActive");
		}),
		0 < o(".close-side-widget").length &&
		o(".close-side-widget").on("click", function (e) {
			e.preventDefault(), o(".info-group").removeClass("isActive");
		}),
		o("body").on("click", function (e) {
			o(".info-group").removeClass("isActive"), o(".cart-group").removeClass("isActive");
		}),
		o(".xs-sidebar-widget").on("click", function (e) {
			e.stopPropagation();
		})
	});

	/**
	 * Logistic Background Contorl
	 * @param {*} $scope 
	 * @param {*} $ 
	 */
	function logisticsBackgroundLoad($scope, $) {
        $('[data-background]').each(function() {
            $(this).css('background-image', 'url('+ $(this).attr('data-background') + ')');
        });
    }

	/**
	 * Logistic Testimonial Control
	 * @param {*} $scope 
	 * @param {*} $ 
	 */
	function logisticTestimonial($scope, $) {
		$('.tl-thx-testimonial-slider').slick({
			infinite: true,
			slidesToShow: 1,
			autoplay: false,
			slidesToScroll: 1,
			dots: false,
			nav: true,
			autoplaySpeed: 5000,
			prevArrow: ".testi-left_arrow",
			nextArrow: ".testi-right_arrow",
		});
	}

		

		$(window).on('elementor/frontend/init', function () {
			elementorFrontend.hooks.addAction('frontend/element_ready/fastrance_trans_logi_banner.default', logisticsBackgroundLoad);
			elementorFrontend.hooks.addAction('frontend/element_ready/fastrance_trans_video_banner.default', logisticsBackgroundLoad);
			elementorFrontend.hooks.addAction('frontend/element_ready/fastrans_logistic_testimonials.default', logisticTestimonial);
			elementorFrontend.hooks.addAction('frontend/element_ready/fastrans_logistic_testimonials.default', logisticsBackgroundLoad);
		});

})(window.jQuery);