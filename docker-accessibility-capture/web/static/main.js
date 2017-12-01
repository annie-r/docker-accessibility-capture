$(document).ready(function() {
	$('.screenshot').click(function(e){
		target = e.target;
		screenshot_id = target.getAttribute("id")
		click_coords = JSON.stringify({ x: e.clientX, y: e.clientY, id: screenshot_id });

		$.ajax({
			url: '/click', 
			data: click_coords, 
			type: 'POST', 
			contentType: 'application/json;charset=UTF-8',
			success: function(data) {
				// Success
				window.location = data; 
			}
		});
	});
});