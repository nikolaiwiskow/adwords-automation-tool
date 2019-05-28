// will show loading animation
$(document).on('submit', 'form', function(e) {
	$(".overlay").show();
});


//will display the overlay on final-selection screen
function overlay() {
	if ($('#id_outputs_1').is(":checked")) {
		$('#confirmation-overlay').fadeIn(100);

	} else {
		$('form').trigger('submit');
	}
}