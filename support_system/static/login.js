(function (jq) {
    jq.extend({
        "lg": function () {
            jq(".btn").on("click", function () {
                jq(".form-control").each(function () {
                    jq(this).parent().removeClass("has-error");
                    jq(this).next().html("");
                    console.log(jq(this));
                    if (jq(this).val().length === 0) {
                        console.log(jq(this));
                        jq(this).parent().addClass("has-error");
                        var name = jq(this).prev().text();
//                jq(this).next().html("<small><font color=\"red\">用户名不能为空</font></small>");
                        jq(this).next().text(name + "不能为空");
                        return false;
                    }
                });
                return false;
            });
        }
})
})(jQuery);