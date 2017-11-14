(function (ind) {
    ind.extend({

    })
})(jQuery);

 //    左侧菜单实现闭合
    $(".head").on("click", function () {
        $(this).parent().siblings().children("ul").slideUp();
        $(this).next().slideToggle();
    });

    //    实现删除的功能，添加了on方法的事件委派
    $("tbody").on("click", ".del", function () {
        console.log($(this));
        var tmp_tr = $(this).parent().parent();
        console.log($(tmp_tr));
        $(tmp_tr).remove();
    });

    //    实现增加的功能，用字符串实现
    //找到input标签


    $(".confrimBtn").on("click", function () {
        $("#myModal").modal("hide");

        var username = $("#name").val();
        var sex = $("#sex").val();
        var age = $("#age").val();

        var tds = $("#myModal").data("tds");

        if (tds === undefined) {
            var trTmp = document.createElement("tr");
            $(trTmp).append("<td>" + ($("tbody tr").size() + 1) + "</td>td>");
            $(trTmp).append("<td>" + username + "</td>");
            $(trTmp).append("<td>" + sex + "</td>");
            $(trTmp).append("<td>" + age + "</td>");

            $(trTmp).append($("tbody tr:first").find("td").last().clone());
            $("tbody").append(trTmp);
        } else {
            tds.eq(1).text(username);
            tds.eq(2).text(sex);
            tds.eq(3).text(age);

            $("#myModal").removeData("tds");
        }
    });

    $(".panel-body .btn-success").on("click", function () {
        $("#myModal :input").val("");
    });

    //    实现编辑功能
    $("tbody").on("click", ".edit", function () {
        $("#myModal").modal("show");
        var tds = $(this).parent().parent().children();
        var username = tds.eq(1).text();
        var sex = tds.eq(2).text();
        var age = tds.eq(3).text();

        $("#name").val(username);
        $("#sex").val(sex);
        $("#age").val(age);

        $("#myModal").data("tds", tds);
    });