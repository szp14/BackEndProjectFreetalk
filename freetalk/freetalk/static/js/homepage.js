
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
			window.location.href = '../';
		}
	});
}

function checkPost() {
	var title = $("#new_post_title").val(), content = $("#new_post_content").val();
	var title1 = $.trim(title), content1 = $.trim(content);
	if (title1 == '') {
		alert("标题不能为空！");
	}
	else if (content1 == '') {
		alert("内容不能为空！");
	}
	else {
		$("#new_post").submit();
		alert("发帖成功！");
	}
}



