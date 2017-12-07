$(document).ready(function() {
	$('.screenshot').click(function(e){
		let target = e.target;
		let screenshot_id = target.getAttribute("id")

		// Get selected radio button 
		let text = document.getElementById("text"); 
		let textField = document.getElementById("text-value"); 
		let textValue = undefined; ;
		if(text && text.checked && textField) {
			textValue = textField.value; 
		}

		let inputs = { type: "click", x: e.clientX, y: e.clientY, id: screenshot_id };
		if(textValue != undefined && textValue.length) { 
			inputs.type = "text", 
			inputs.text = textValue
		}

		$.ajax({
			url: '/click', 
			data: JSON.stringify(inputs), 
			type: 'POST', 
			contentType: 'application/json;charset=UTF-8',
			success: function(data) {
				// Success
				window.location = data; 
			}
		});
	});
});