$(document).ready(function() {

	// Pagination
	// Change active page number
	$(".page-number").click(function() {
		$(".active").removeClass("active");
		$(this).addClass("active");
	});

	$(".pagination-prev").click(function() {
		$(".active").removeClass("active");
		$(this).addClass("active");
	});

	$(".pagination-next").click(function() {
		$(".active").removeClass("active");
		$(this).addClass("active");
	});
});