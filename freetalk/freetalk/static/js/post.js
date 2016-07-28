
function response() {
	var content = $("#new_post_content").val();
	var content1 = $.trim(content);
	if(content1 == "")
		alert("回复内容不能为空！");
	else {
		var img = $("#img").val();
		if (img != "") {
			var list1 = img.split(".");
			var type = list1[1];
			if (type == "gif" || type == "GIF" || type == "jpg" || type == "JPG" || type == "png" || type == "PNG")
				$("#new_respond").submit();
			else
				alert("图片格式错误，只能为gif、jpg和png三种格式！");
		}
		else
			$("#new_respond").submit();
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
				data = JSON.parse(data);
				alert(data['res']);
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

$(".upvote").click(function() {
	var id = $(this).attr("id").substr(4);
	var post_data = {
		'upvote': id,
	};
	$.ajax({
		type: "POST",
		data: post_data,
		success: function (data) {
			data = JSON.parse(data);
			location.reload();
		}
	});
});

$("#vote").click(function() {
	var post_data = {
		'vote': true,
	};
	$.ajax({
		type: "POST",
		data: post_data,
		success: function (data) {
			data = JSON.parse(data);
			location.reload();
		}
	});
});

$("#givecoin").click(function() {
	coin = $("#coin").val();
	if($.isNumeric(coin)) {
		coin = parseInt(coin);
		var post_data = {
			'coin': coin,
		};
		$.ajax({
			type: "POST",
			data: post_data,
			success: function (data) {
				data = JSON.parse(data);
				alert(data['res']);
			}
		});
	}
	else 
		alert("没有输入纯数字！")
});
var href = window.location.href;
var pos1 = href.indexOf('post/');
href = href.substr(pos1 + 5);
var pos2 = href.indexOf('/');
var loc = parseInt(href.substring(pos2 + 1, href.length - 1));
var total = parseInt($("#nowpage").text().substr(1, 1));

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
			window.location.href = "../" + 1;
		}
	});
});

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