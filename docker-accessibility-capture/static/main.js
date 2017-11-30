$(document).ready(function() {
	$('#screenshot').click(function(e){
		target = e.target;
		click_coords = { x: e.clientX, y: e.clientY };

		$.post("click", click_coords, function(data) {
			// Success
			window.location = data; 
		});
	});
});