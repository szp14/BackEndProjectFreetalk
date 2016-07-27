
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

var href = window.location.href;
var pos1 = href.indexOf('tagadmin/');
href = href.substr(pos1 + 9);
var pos2 = href.indexOf('/');
var loc = parseInt(href.substring(0, pos2));
var total = parseInt($("#nowpage").text().substr(1, 1));

$("#prepage").click(function() {
	if(loc == 1)
		alert("已经是第一页了，无法继续向前翻页！")
	else {
		window.location.href = "../" + (loc - 1);
	}
});

$("#nextpage").click(function() {
	if(loc == total)
		alert("已经是最后一页了，无法继续向后翻页！")
	else {
		window.location.href = "../" + (loc + 1);
	}
});

$("#turnpage").click(function() {
	var page = $("#page").val()
	if($.isNumeric(page)) {
		page = parseInt(page);
		if(page < 1 || page > total)
			alert("输入的页数超出范围，请重新输入！");
		else {
			window.location.href = "../" + page;
			alert("跳转成功！");
		}
	}
	else 
		alert("没有输入纯数字！")
});