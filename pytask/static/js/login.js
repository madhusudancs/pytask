var login_user = function (login_url) {
  $(document).ready(function () {
    $('#form_login').submit(function() {
      $.post(
        login_url,
        $("#form_login").serialize(),
        function (raw_data) {
          data = $.parseJSON(raw_data);
          alert(data);
          if (data.authentication == "success") {
            $("div#useraction").replaceWith(data.markup);
            alert(data.markup);
          }
        });
      return false;
    });
  });
}