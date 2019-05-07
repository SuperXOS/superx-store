$(document).ready(function () {

			$('.multi-item-carousel').carousel({
		  interval: false
		});

		// for every slide in carousel, copy the next slide's item in the slide.
		// Do the same for the next, next item.
		$('.multi-item-carousel .item').each(function(){
		  var next = $(this).next();
		  if (!next.length) {
		    next = $(this).siblings(':first');
		  }
		  next.children(':first-child').clone().appendTo($(this));

		  if (next.next().length>0) {
		    next.next().children(':first-child').clone().appendTo($(this));
		  } else {
		  	$(this).siblings(':first').children(':first-child').clone().appendTo($(this));
		  }
		});

  var trigger = $('.hamburger'),
      overlay = $('.overlay'),
     isClosed = false;

    trigger.click(function () {
      hamburger_cross();
    });

    function hamburger_cross() {

      if (isClosed == true) {
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        isClosed = false;
      } else {
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        isClosed = true;
      }
  }

  $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
  });

});

function getApplicationDetails(str1,str2){
  document.getElementById("description").innerHTML = str1;
}



function showRefreshAnimation(str){
if(str=="stop"){
 $('#loader').css("display", "none");
 $('#main').css("display", "block");
 }
 else if(str=="start"){
 $('#loader').css("display", "block");
 $('#main').css("display", "none");
 }
}
$('#back').click(function() {
      history.go(-1);
});
$('#forw').click(function() {
      history.go(1);
});
function changeTitle(){
document.title = "update";
}

function installApp(str){
  document.title = "install->"+str;
  //  $('#install').css("display", "none");
  //  $('#cancel').css("display", "block");
  //  $('#installprogress').css("display", "block");
  console.log(str);
}



function cancelInstallApp(str){
document.title = "pkcon->-y->-p->cancel->"+str;
 $('#install').css("display", "block");
 $('#installprogress').css("display", "none");
 $('#cancel').css("display", "none");
}
function updateButtons(str){
  if(str=="installed"){
 $('#install').css("display", "none");
 $('#remove').css("display", "block");
 $('#open').css("display", "block");
  }
  else if(str == "update"){
 $('#install').css("display", "none");
 $('#remove').css("display", "block");
 $('#open').css("display", "none");
 $('#update').css("display", "block");
  }
}

function setStatus(str){
document.getElementById("statusprogress").innerHTML= str;
}
