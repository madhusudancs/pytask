/* Original code from http://davidwalsh.name/persistent-header-opacity#bottom */
var create_uberbar = function () {
$(document).ready(function() {
    $("#header").css("position", "relative");
    $("#header").css("top", "40px");
    $("#header").css("margin-bottom", "70px");

    //settings
    var fadeSpeed = 200;
    var fadeTo = 0.5;
    var topDistance = 30;
 
    var topbarME = function() {
      $('#uberbar').fadeTo(fadeSpeed,1);
    };

    var topbarML = function() {
      $('#uberbar').fadeTo(fadeSpeed,fadeTo);
    };

    var inside = false;
    //do
    $(window).scroll(function() {
      position = $(window).scrollTop();
      if(position > topDistance && !inside) {
        //add events
        topbarML();
        $('#uberbar').bind('mouseenter',topbarME);
        $('#uberbar').bind('mouseleave',topbarML);
        inside = true;
      }
      else if (position < topDistance){
        topbarME();
        $('#uberbar').unbind('mouseenter',topbarME);
        $('#uberbar').unbind('mouseleave',topbarML);
        inside = false;
      }
    });
  });
}
