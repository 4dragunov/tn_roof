$('.part').hover (
	function() {
		$('.description_svg').html($(this).attr('description-data'));
		$('.description_svg').fadeIn();
	},
	function() {
		$('.description_svg').fadeOut(50);
	}
)
