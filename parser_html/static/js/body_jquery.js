$('#back').click(function() {
      history.go(-1);
});
function changeTitle(){
document.title = "update";
}

//slider javascript

jssor_slider1_starter = function (containerId) {
      var options = {
          $AutoPlay: true,

          $PauseOnHover: true,                               //[Optional] Whether to pause when mouse over if a slideshow is auto playing, default value is false

          $ArrowKeyNavigation: true,   			            //Allows arrow key to navigate or not
          $SlideWidth: 600,                                   //[Optional] Width of every slide in pixels, the default is width of 'slides' container
          //$SlideHeight: 300,                                  //[Optional] Height of every slide in pixels, the default is width of 'slides' container
          $SlideSpacing: 0, 					                //Space between each slide in pixels
          $DisplayPieces: 2,                                  //Number of pieces to display (the slideshow would be disabled if the value is set to greater than 1), the default value is 1
          $ParkingPosition: 100,                                //The offset position to park slide (this options applys only when slideshow disabled).

          $ArrowNavigatorOptions: {                       //[Optional] Options to specify and enable arrow navigator or not
              $Class: $JssorArrowNavigator$,              //[Requried] Class to create arrow navigator instance
              $ChanceToShow: 2,                               //[Required] 0 Never, 1 Mouse Over, 2 Always
              $AutoCenter: 2,                                 //[Optional] Auto center arrows in parent container, 0 No, 1 Horizontal, 2 Vertical, 3 Both, default value is 0
              $Steps: 1                                       //[Optional] Steps to go for each navigation request, default value is 1
          }
      };

      var jssor_slider1 = new $JssorSlider$(containerId, options);
      //responsive code begin
      //you can remove responsive code if you don't want the slider scales while window resizes
      function ScaleSlider() {
          var parentWidth = jssor_slider1.$Elmt.parentNode.clientWidth;
          if (parentWidth)
              jssor_slider1.$SetScaleWidth(Math.min(parentWidth, 800));
          else
              $JssorUtils$.$Delay(ScaleSlider, 30);
      }

      ScaleSlider();
      $JssorUtils$.$AddEvent(window, "load", ScaleSlider);


      if (!navigator.userAgent.match(/(iPhone|iPod|iPad|BlackBerry|IEMobile)/)) {
          $JssorUtils$.$OnWindowResize(window, ScaleSlider);
      }

      //if (navigator.userAgent.match(/(iPhone|iPod|iPad)/)) {
      //    $JssorUtils$.$AddEvent(window, "orientationchange", ScaleSlider);
      //}
      //responsive code end
  };

  TweenMax.to("#tasksvg", 1, {rotation:360, repeat:-1, transformOrigin:"50% 50%", ease:Linear.easeNone});

  function loadmodal(str1,str2){
   var head = str1;
   var body = str2;
   document.getElementById('modalhead').innerHTML = head;
   document.getElementById('modalbody').innerHTML = body;
   $('#sumModal').modal('show');
  }
