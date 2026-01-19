// Array of json objects
var statesRates = [{
	"State": "New Work",
	"Rate": 100
}, {
	"State": "Delhi",
	"Rate": 150
}, {
	"State": "California",
	"Rate": 125
}, {
	"State": "Perth",
	"Rate": 170
}]

// Create the Dropdown with State Names / Values

function createList() {

	// Loop through each object in json array
	for (var i = 0; i < statesRates.length; i++) {

		// Define variables for key / value pairing
		var stateName = statesRates[i].State;
		var stateRate = statesRates[i].Rate;

		// Create <option> element with dropdown 
		jQuery("#state").append('<option value="' + stateRate + '">' + stateName + '</option>');

	}
}



// Calculate Cost function

function calculateCost() {

	// Get Values of Inputs
	var squareFeet = $("#square-feet").val();
	var state = $("#state").val();
	var totalCost = state;

	if (squareFeet > 375) {
		$("#shipping-estimate").html("Sorry, we only allow online order estimates for one pallet product (300 KG). Please contact us for more information.");
	} else {
		$("#shipping-estimate").html("The shipping estimate to this state is $" + totalCost);
	}
}

// Calculate Cost when button is clicked
createList();

jQuery("#calculate").click(function() {
	calculateCost;
});