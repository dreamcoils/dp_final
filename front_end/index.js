$(document).ready(function () {	
    var user_query = location.search;
    if (user_query.indexOf("?") != -1) {
        console.log(user_query);
        userId = decodeURIComponent(user_query.replace("?user_id=",""));
        var recommend = 'http://39.101.165.8:9500/graph/recommend/';
        $.ajax({
            url: recommend,
            dataType: 'json',
            type: "GET",
            crossDomain: true,
            data: {
                user_id: userId
            },
            success: function(res) {
                // console.log(res);
                // console.log(typeof(res[0]));
                // console.log(res[0].name);
                // console.log(res.length)

                if (res != null) {
                    $('#title_h2').text('猜您喜欢：');
                    var res_html = "<ul>";
                    for(var i = 0; i < res.length; ++i) {
                        res_html += "<li>" + 
                                        "<div class='pro-img'>" + 
                                            "<a href='" + res[i].image_url + "' target='_blank'>" + 
                                                "<img src='" + res[i].image_url + "'>" + 
                                            "</a>" + 
                                        "</div>" + 
                                        "<p style='font-size: 19px; font-weight: bold;'>" + res[i].name + "</p>" + 
                                        "<p class='desc1', style='font-size: 15px;'>菜系：" + res[i].cuisine + " / 口味：" + res[i].taste + "</p>" + 
                                        "<p class='desc2', style='font-size: 15px;'>烹饪方式：" + res[i].cooking_method + "</p>" +
                                    "</li>";
                        if (i == 0)
                            console.log(res_html);
                    }
                    res_html += "</ul>"
                    $("#product").html(res_html);
                }
            },
            error: function(res) {
                alert('请求出错，请使用0-999之间的ID！');
            }
        })

    }

    $("#search").click(function(){
        // var food = document.getElementById("search_text")
        var food = $("#search_text").val();
        console.log(2, food)
        var _url = 'http://39.101.165.8:9500/es/query/';
        // document.getElementById("title_h2").innerHTML = '为您检索到如下美食：';
        $.ajax({
            url: _url,
            dataType:'json',
            type:"GET",
            crossDomain:true,
            data: {
                q: food
            },
            success: function(res) {
                console.log(res);
                $('#title_h2').text('为您检索到如下美食：');
                
                if (res != null) {
                    var res_html = "<ul>";
                    for(var i = 0; i < res.length; ++i) {
                        res_html += "<li>" + 
                                        "<div class='pro-img'>" + 
                                            "<a href='" + res[i].image_url + "'>" + 
                                                "<img src='" + res[i].image_url + "'>" + 
                                            "</a>" + 
                                        "</div>" + 
                                        "<p style='font-size: 19px; font-weight: bold;'>" + res[i].name + "</p>" + 
                                        "<p class='desc1', style='font-size: 15px;'>菜系：" + res[i].cuisine + " / 口味：" + res[i].taste + "</p>" + 
                                        "<p class='desc2', style='font-size: 15px;'>烹饪方式：" + res[i].cooking_method + "</p>" +
                                    "</li>";
                        if (i == 0)
                            console.log(res_html);
                    }
                    res_html += "</ul>"
                    $("#product").html(res_html);
                }
            },
            error: function(res) {
                alert('抱歉~服务器繁忙，检索失败！请联系开发者~~');
            }
        });
    });

    
    $("#inputImage").on('change', doUpload);

    function doUpload(){
        // var file = this.file[0];
        // if(!/image\/\w+/.test(file.type)) {
        //     alert("文件必须为图片！");
        //     return false;
        // }
        var formData = new FormData($("#uploadForm")[0]);
        $.ajax({
            // url: 'http://127.0.0.1:8000/uploadImg' ,
            url: 'http://39.101.165.8:7002/uploadImg',
            type: 'POST',
            data: formData, // 请求数据
            dataType: "JSON", // 返回数据格式
            // crossDomain: true,
            async:false,
            contentType: false, //表示不处理数据
            processData: false,
            cache: false,
            success: function (data) {
                // if (data === 1) { 
                //     alert("上传成功");
                // }else if (data === 0) {
                //     alert("上传失败");
                // }
                // alert("图片上传成功");
                console.log(data)
            },
            error: function (data) {
                alert("抱歉~服务器繁忙，图片上传失败！请联系开发者~~");
                console.log(data);
            }
        });

        $.ajax({
            url: 'http://39.101.165.8:8081/main/' ,
            type: 'POST',
            dataType:'json',
            contentType:'application/json',
            crossDomain:true,
            data: JSON.stringify({
                data: 'http://39.101.165.8/media/upload/picture.jpg'
            }),
            success: function (res) {
                console.log(res);
                $('#title_h2').text('为您检索到与您上传图片相关的美食：');
                
                if (res != null) {
                    var res_html = "<ul>";
                    for(var i = 0; i < res.length; ++i) {
                        res_html += "<li>" + 
                                        "<div class='pro-img'>" + 
                                            "<a href='" + res[i].image_url + "'>" + 
                                                "<img src='" + res[i].image_url + "'>" + 
                                            "</a>" + 
                                        "</div>" + 
                                        "<p style='font-size: 19px; font-weight: bold;'>" + res[i].name + "</p>" + 
                                        "<p class='desc1', style='font-size: 15px;'>菜系：" + res[i].cuisine + " / 口味：" + res[i].taste + "</p>" + 
                                        "<p class='desc2', style='font-size: 15px;'>烹饪方式：" + res[i].cooking_method + "</p>" +
                                    "</li>";
                        if (i == 0)
                            console.log(res_html);
                    }
                    res_html += "</ul>"
                    $("#product").html(res_html);
                }
            },
            error: function (res) {
                alert("抱歉~服务器繁忙，暂无法提供此服务。请联系开发者~~")
                console.log(res);
            }
        })
    }
});


$(document).keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    var text = document.getElementById("search_text");
    if(keycode == '13' & text == document.activeElement){
        $("#search").click();
    }
});

