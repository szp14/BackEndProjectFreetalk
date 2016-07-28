﻿
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
			window.location.href = '../../../';
		}
	});
}

function checkPost() {
	var title = $("#new_post_title").val(), content = $("#new_post_content").val();
	var title1 = $.trim(title), content1 = $.trim(content);
	//var check = $("#highlight").attr("checked");
	//alert(check);
	//return;
	if (title1 == '') {
		alert("标题不能为空！");
	}
	else if(title.length > 20)
		alert("标题长度不能大于二十！");
	else if (content1 == '') {
		alert("内容不能为空！");
	}
	else {
		var img = $("#img").val();
		if (img != "") {
			var list1 = img.split(".");
			var type = list1[1];
			if (type == "gif" || type == "GIF" || type == "jpg" || type == "JPG" || type == "png" || type == "PNG")
				$("#new_post").submit();
			else
				alert("图片格式错误，只能为gif、jpg和png三种格式！");
		}
		else
			$("#new_post").submit();
	}
}

$("#searchbtn").click(function() {
	var sertag = $("#search_label").val(), sercon = $("#menu_block_content").val();
	if(sertag == "无" && sercon == '')
		alert("您未输入实际的搜索内容，请重新输入！");
	else {
		con = sertag + " " + sercon;
		window.location.href = "../../" + con + "/1/";
	}
});

$(".postlick").click(function(){
	var id = $(this).attr("id").substr(4);
	var post_data = {
		'postid': id,
	};
	$.ajax({
		type: "POST",
		data: post_data,
	});
});

$(".opTag").click(function () {
	var cliid = $(this).attr("id");
	cliid = cliid.substring(2);
	var add1 = $("#addTag" + cliid).val(), del1 = $("#delTag" + cliid).val();
	if(add1 == '无' && del1 == '无')
		alert('您未进行实际的修改类标操作,修改类标失败！');
	else {
		var opTag = {
			'addTag': add1,
			'delTag': del1,
			'id': cliid,
		}
		$.ajax({
			type: "POST",
			data: opTag,
			success: function (data) {
				data = JSON.parse(data);
				alert(data['tip']);
				if(data['type'] == 1)
					window.location.href = "";
			}
		});
	}
});


$("#sortbtn").click(function() {
	window.location.href = "../../" + $("#sort").val() + "/1/";
});

var href = window.location.href;
var pos1 = href.indexOf('homepage/');
href = href.substr(pos1 + 9);
var pos2 = href.indexOf('/');
var loc = parseInt(href.substring(pos2 + 1, href.length - 1));
var type = href.substring(0, pos2);
var total = parseInt($("#nowpage").text().substr(1, 1));

$(".opPost").click(function () {
	var cliid = $(this).attr("id");
	cliid = cliid.substring(7);
	var op = {
		'delPost': cliid,
	}
	$.ajax({
		type: "POST",
		data: op,
		success: function (data) {
			data = JSON.parse(data);
			alert("该帖子已被成功删除！");
			window.location.href = "../../" + type + '/' + 1;
		}
	});
});

$("#prepage").click(function() {
	if(loc == 1)
		alert("已经是第一页了，无法继续向前翻页！")
	else {
		window.location.href = "../../" + type + '/' + (loc - 1);
	}
});

$("#nextpage").click(function() {
	if(loc == total)
		alert("已经是最后一页了，无法继续向后翻页！")
	else {
		window.location.href = "../../" + type + '/' + (loc + 1);
	}
});

$("#turnpage").click(function() {
	var page = $("#page").val()
	if($.isNumeric(page)) {
		page = parseInt(page);
		if(page < 1 || page > total)
			alert("输入的页数超出范围，请重新输入！");
		else {
			window.location.href = "../../" + type + '/' + page;
			alert("跳转成功！");
		}
	}
	else 
		alert("没有输入纯数字！")
});



