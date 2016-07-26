
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
})
