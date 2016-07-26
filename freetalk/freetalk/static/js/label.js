
function addTag() {
	var tagname = $("#addTag").val();
	var content1 = $.trim(tagname);
	var post_data = {
		'tag': tagname
	};
	if(content1 == "")
		alert("类标名不能为空！");
	else {
		$.ajax({
		type: "POST",
		data: post_data,
		success: function (data) {
			alert("增加类标成功！");
			location.reload();
		}
	});
	}
}