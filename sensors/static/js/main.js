$('.part').hover (
	function() {
		$('.description_svg ').html($(this).attr('description-data'));
		$('.description_svg ').css({'display':'block'});
		// $('.description_svg ').fadeIn();

	},
	function() {
		$('.description_svg ').css({'display':'none'});
		// $('.description_svg ').fadeOut(100);
	}
)


