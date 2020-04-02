// When item is clicked display hidden content
function setFilter(selectedRegion, selectedCountry) {
    
    console.log("You selected " + selectedRegion + " in the " + selectedCountry);

    if ( selectedRegion === "All" ) {
        console.log("You have selected All!");
        let countries = document.getElementsByClassName(selectedCountry);
        countries.display = "grid";
    } else {
        console.log("You have selected " + selectedRegion + "!");
        let countries = document.getElementsByClassName(selectedCountry);
        countries.display = "none";
        let region = document.getElementById(selectedRegion);
        region.style.display = "grid";
    }

}