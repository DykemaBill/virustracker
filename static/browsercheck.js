// Web browser check

let IE11 = navigator.userAgent.toUpperCase().indexOf("TRIDENT/");
console.log("The IE11 check returns: " + IE11);
let IE11orOlder = navigator.userAgent.toUpperCase().indexOf("MSIE");
console.log("The IE11orOlder check returns: " + IE11orOlder);

if ( IE11 == -1 && IE11orOlder == -1 ) {
  console.log("You're not using IE 11 or older");
} else {
  console.log("You are using IE");
  window.location = "ienotice";
}