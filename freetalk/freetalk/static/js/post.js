
function response() {
	var content = $("#new_post_content").val();
	var content1 = $.trim(content);
	var post_data = {
		'content': content
	};
	if(content1 == "")
		alert("回复内容不能为空！");
	else {
		$.ajax({
			type: "POST",
			data: post_data,
			success: function (data) {
				alert("回复成功！");
				location.reload();
			}
		});
	}
}

$(".rere").click(function() {
	var id = $(this).attr("id").substr(4);
	var recon = $("#recon" + id).val();
	var recon1 = $.trim(recon);
	if(recon1 == "")
		alert("回复内容不能为空！");
	else {
		var post_data = {
			'recon': recon,
			"id": id
		};
		$.ajax({
			type: "POST",
			data: post_data,
			success: function (data) {
				alert("回复成功！");
				location.reload();
			}
		});
	}
});

$(".rerespond_btn").click(function() {
	var rereid = $(this).attr("class").substr(19), reid = $(this).parent().parent().parent().attr("id").substr(3);
	var post_data = {
		'rereid': rereid,
		'reid': reid
	};
	$.ajax({
		type: "POST",
		data: post_data,
		success: function (data) {
			data = JSON.parse(data);
			alert(data['res']);
			location.reload();
		}
	});
});

$(".delre").click(function() {
	var delreid = $(this).attr("id").substr(5);
	var post_data = {
		'delreid': delreid,
	};
	$.ajax({
		type: "POST",
		data: post_data,
		success: function (data) {
			data = JSON.parse(data);
			alert(data['res']);
			location.reload();
		}
	});
});