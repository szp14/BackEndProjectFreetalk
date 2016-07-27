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
	var title = $("#new_post_title").val(), content = $("#rel_post_content").text();
	var title1 = $.trim(title), content1 = $.trim(content);
	if (title1 == '') {
		alert("标题不能为空！");
	}
	else if(title.length > 20)
		alert("标题长度不能大于二十！");
	else if (content1 == '') {
		alert("内容不能为空！");
	}
	else {
		var post_data = {
			'title': title,
			'content': content,
			'tag1': $("#tag1").val(),
			'tag2': $("#tag2").val(),
			'tag3': $("#tag3").val(),
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
	}
}

$(".postlick").click(function(){
	//alert($(this).attr("id").substr(4));
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
			window.location.href = "";
		}
	});
});

function addImg(value){
	alert(value);//调试用
	var txt = document.getElementById("new_post_content")
	o = document.createElement("IMG");
	o.className = "new_post_img";
	o.src = "/static/images/mengbi.jpg";//这里需要先上传图片再拿到上传图片的地址
	txt.appendChild(o);
}

$("#sortbtn").click(function() {
	alert("排序成功！")
	window.location.href = "../../" + $("#sort").val() + "/1/";
});

var href = window.location.href;
var pos1 = href.indexOf('homepage/');
href = href.substr(pos1 + 9);
var pos2 = href.indexOf('/');
var loc = parseInt(href.substring(pos2 + 1, href.length - 1));
var type = href.substring(0, pos2);
var total = parseInt($("#nowpage").text().substr(1, 1));

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



