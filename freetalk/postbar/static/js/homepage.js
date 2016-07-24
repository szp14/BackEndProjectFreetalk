
function logout() {
	var post_data = {
		'logout': true
	};
	$.ajax({
		type: "POST",
		data: post_data,
		success: function (data) {
			data = JSON.parse(data);
			alert(data['res']);
			window.location.href = '../log/'
		}
	});
}



