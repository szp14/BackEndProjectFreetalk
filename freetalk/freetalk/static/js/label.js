
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
				data = JSON.parse(data);
				alert(data["res"]);
				location.reload();
			}
		});
	}
}

$(".optag").click(function() {
	var type = $(this).val(), id = $(this).attr("id").substr(6);
	var post_data;
	if (type == "删除类标") {
		post_data = {
			'deltag': id
		};
		$.ajax({
			type: "POST",
			data: post_data,
			success: function (data) {
				data = JSON.parse(data);
				alert(data["res"]);
				location.reload();
			}
		});
	}
	else {
		var tagname = $("#tagname" + id).val();
		if($.trim(tagname) == "")
			alert("新的类标名不能为空！");
		else {
			post_data = {
				'chatag': id,
				'tagname': tagname
			};
			$.ajax({
				type: "POST",
				data: post_data,
				success: function (data) {
					data = JSON.parse(data);
					alert(data["res"]);
					location.reload();
				}
			});
		}
	}
});