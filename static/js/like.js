$(document).ready(function(){

  var clicked;

  $(".like").click(function(){

    clicked = $(this).attr("id");

    req = $.ajax({
      type : 'POST',
      url : "/like",
      data : {'data':clicked}
    });

    req.done(function (data) {
      document.getElementById(clicked).textContent="Like "+data.like_count;
    });

  });

});