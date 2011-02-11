/* Copyright 2011 Authors of PyTask.
*
* This file is part of PyTask.
*
* PyTask is free software: you can redistribute it and/or modify it
* under the terms of the GNU Affero General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* PyTask is distributed in the hope that it will be useful, but WITHOUT
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
* for more details.
*
* You should have received a copy of the GNU General Public License
* along with PyTask.  If not, see <http://www.gnu.org/licenses/>.
*
* Original code from http://davidwalsh.name/persistent-header-opacity#bottom
* Authors = [
*    '"Madhusudan.C.S" <madhusudancs@fossee.in>',
*    ]
*
*/


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
