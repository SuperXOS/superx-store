

function loadmodal(str1,str2){
 var head = str1;
 var body = str2;
 document.getElementById('modalhead').innerHTML = head;
 document.getElementById('modalbody').innerHTML = body;
 $('#sumModal').modal('show');
}

(function( $ ) {

   //Function to animate slider captions
 function doAnimations( elems ) {
   //Cache the animationend event in a variable
   var animEndEv = 'webkitAnimationEnd animationend';

   elems.each(function () {
     var $this = $(this),
       $animationType = $this.data('animation');
     $this.addClass($animationType).one(animEndEv, function () {
       $this.removeClass($animationType);
     });
   });
 }

 //Variables on page load
 var $myCarousel = $('#carousel-example-generic'),
   $firstAnimatingElems = $myCarousel.find('.item:first').find("[data-animation ^= 'animated']");

 //Initialize carousel
 $myCarousel.carousel();

 //Animate captions in first slide on page load
 doAnimations($firstAnimatingElems);

 //Pause carousel
 $myCarousel.carousel('pause');


 //Other slides to be animated on carousel slide event
 $myCarousel.on('slide.bs.carousel', function (e) {
   var $animatingElems = $(e.relatedTarget).find("[data-animation ^= 'animated']");
   doAnimations($animatingElems);
 });
   $('#carousel-example-generic').carousel({
       interval:3000,
       pause: "false"
   });

})(jQuery);
$(document).ready(function () {
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



function setProgress(str){
$('#progressbar').css("width", str+"%");
document.getElementById("percentageprogress").innerHTML= str;
}
function setStatus(str){
document.getElementById("statusprogress").innerHTML= str;
}
function removestatus(){
$('#display').css("display", "none");
}

function getapps(){
var keyword = document.getElementById('keyword').value;
//alert(keyword);
if(keyword != ""){
$.ajax({
                             //the url to send the data to
                               url: "/superxstore/getapps/",
                               //the data to send to
                               data: {
                                       keyword : keyword,
                                       csrfmiddlewaretoken: '{{ csrf_token }}'
                                     },
                              //type. for eg: GET, POST
                               type: "POST",
                              //datatype expected to get in reply form server
                               dataType: "json",
                             //on success
                             complete: function(data){
                            //do something after something is recieved from php
                               //alert(JSON.stringify(data));
                               document.getElementById('showlist').innerHTML = data.responseText;
                             },
                           //on error
                            error: function(){
                          //bad request
                            }
                          });
}
else{
document.getElementById('showlist').innerHTML = "";
}
}
