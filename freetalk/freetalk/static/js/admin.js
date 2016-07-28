

$(".op").click(function (){
	var name1 = $(this).attr("class");
	var res = name1.substring(0, name1.length - 3);
	var post_data = {
        "op": res
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

var href = window.location.href;
var pos1 = href.indexOf('useradmin/');
href = href.substr(pos1 + 10);
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
	var page = $("#page").val();
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



