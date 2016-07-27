﻿﻿

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
	var title = $("#new_post_title").val(), content = $("#rel_post_content").text();
	var title1 = $.trim(title), content1 = $.trim(content);
	if (title1 == '') {
		alert("标题不能为空！");
	}
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

