var login_user = function (login_url) {

  /* Function that handles the post login request changes. */
  var process_login_response = function (raw_data) {
    /* We expect an exception when login fails. Read comment with catch. */
    try {
      data = $.parseJSON(raw_data);
      if (data.authentication == "success") {
        /* Login succeeded */
        if (data.markup) {
          /* Replace the HTML with the user actions since
           * the request came from a URL other than logout page */
          $("div#useraction").replaceWith(data.markup);
        } else if (data.redirect) {
          /* Reload the page to the pytask home page since
           * the login request came from logout page. This
           * is done because the logout text says you have
           * been logged out, which will be awkward after
           * user re-logs in. */
          window.location.href=data.redirect;
        }
      }
    } catch (e) {
      /* Login failed so the login view returned to the same view as
       * the existing page from which the call was made and thus we
       * get html. So let us display the error. */
      $('div #loginform #error').show();
    }
  }


  /* Attach a handler which does the form post upon the submit
   * button is pressed on the login form. */
  $(document).ready(function () {
    $('#form_login').submit(function() {
      $.post(
        login_url,
        $("#form_login").serialize(),
        process_login_response);
      return false;
    });
  });
}