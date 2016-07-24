

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




