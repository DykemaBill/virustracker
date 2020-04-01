// When item is clicked display hidden content
function clickExpand(element) {
    element.classList.toggle("active");
    var content;
    content = element.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
    element.nextElementSibling.nextElementSibling.classList.toggle("active");
    content = element.nextElementSibling.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }

}