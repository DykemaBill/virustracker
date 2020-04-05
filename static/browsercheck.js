// Web browser check

if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)) { //test for MSIE x.x;
  let ieversion=new Number(RegExp.$1) // capture x.x portion and store as a number
  if (ieversion>=8) {
   console.log("You're using IE8 or above");
   ieNotice();
  } else if (ieversion>=7) {
   console.log("You're using IE7.x");
   ieNotice();
  } else if (ieversion>=6) {
   console.log("You're using IE6.x");
   ieNotice();
  } else if (ieversion>=5) {
   console.log("You're using IE5.x");
   ieNotice();
  }
 }

 function ieNotice() {
  window.location = "ienotice";
 }