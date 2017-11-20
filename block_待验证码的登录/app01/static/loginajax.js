    $("#btn").click(function () {
    $.ajax({
       url:"/login/",
       type:"POST",
       data:{
           "csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val(),
           "username":$("#id_user").val(),
           "pwd":$("#id_pwd").val(),
           "validCode":$("#id_validCode").val()
       },
       success:function (data) {
           var response=JSON.parse(data);
           if(!response["is_login"]){
               $(".login_error").html(response["error_msg"]).css("color","red")
           }
           else {
               window.location.href='/blog/'
           }
       }
   })
});