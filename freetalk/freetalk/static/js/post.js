
function response() {
	var content = $("#new_post_content").val();
	var content1 = $.trim(content);
	if(content1 == "")
		alert("回复内容不能为空！");
	else {
		$("#new_respond").submit();
		alert("回复成功！");
	}
}
