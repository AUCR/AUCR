function requiredField(input) {
    // Set values for input validation
    let inputLength = input.value.length;
    let label = input.nextSibling.nextSibling;
    let labelCheck = label.innerText.toLowerCase().indexOf("required");
    /*
      If the input is blank then display a red border
      and red text stating the field is required
    */
    if (inputLength < 1 && labelCheck === -1) {
        label.innerText = label.innerText + " is Required";
        label.style.color = "#e74c3c";
        input.style.borderColor = "#e74c3c";
    }
    /*
       If the user inputs a value then it will return the coloring
       and wording back to normal. No validation of the actual input
       is done at this level
    */
    else if (inputLength > 0 && labelCheck !== -1) {
        label.innerText = label.innerText.replace(" is Required", "");
        input.style.borderColor = "rgba(0, 0, 0, .12)";
        label.style.color = "rgb(33,150,243)";
    }
}