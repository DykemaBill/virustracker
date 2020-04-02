// When item is clicked display hidden content
function setFilter(selectedRegion, selectedCountry) {
    
    console.log("You selected " + selectedRegion + " in the " + selectedCountry);

    if ( selectedRegion === "All" ) {
        // If user selects All display all regions
        console.log("You have selected All!");
        let countries = document.getElementsByClassName(selectedCountry);
        for (var i=0; i < countries.length; i++) {
            countries[i].style.display = "grid";
        }
    } else {
        // If user selects a region, hide all and display that region
        console.log("You have selected " + selectedRegion + "!");
        let countries = document.getElementsByClassName(selectedCountry);
        for (var i=0; i < countries.length; i++) {
            countries[i].style.display = "none";
        }
        let regionItem = document.getElementsByClassName(selectedRegion);
        for (var i=0; i < regionItem.length; i++) {
            regionItem[i].style.display = "grid";
        }
    }

}