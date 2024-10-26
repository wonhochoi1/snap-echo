

// String Display
// @input Component component;
// @input string text = ""

function updateText(utterance) {
    script.component.text = utterance;
    //print("updated!");
}

var lastUtterance = "";
var updateEvent = script.createEvent('UpdateEvent');

// HTTP Request Part
/** @type {RemoteServiceModule} */
var remoteServiceModule = script.remoteServiceModule;

var intervalDuration = 3000;


function sendRequest() {
    var httpRequest = RemoteServiceHttpRequest.create();

    httpRequest.url = '';   //address to flask

    httpRequest.method = RemoteServiceHttpRequest.HttpRequestMethod.Get;

    //print('Sending request!');

    remoteServiceModule.performHttpRequest(httpRequest, function(response) {
        print('Request response received');
        print('Status code: ' + response.statusCode);
        print('Content type: ' + response.contentType);
        
        var responseBody = response.body;
        print('Body: ' + responseBody);

        var utterancesArray = JSON.parse(responseBody);

   
        if (utterancesArray.length > 0) {
            lastUtterance = utterancesArray[utterancesArray.length - 1].utterance;

            updateEvent.bind(function() {
                updateText(lastUtterance);
            });

            // Display the last utterance
            print('Last Utterance: ' + lastUtterance);
        } else {
            print('No utterances found');
        }
    });
}


function onUpdateEvent(eventData) {
    sendRequest();
}

// Initial request
sendRequest();

// Schedule a repeating event every 5 minutes
var event = script.createEvent("UpdateEvent");
event.bind(onUpdateEvent);
event.enabled = true;

// Use a timer to limit the execution to your interval (in seconds)
var elapsed = 0;
event.onUpdate = function(eventData) {
    elapsed += 1;
    if (elapsed >= (intervalDuration / 1000)) {
        elapsed = 0;
        onUpdateEvent(eventData);
    }
};

//// String Display
//// @input Component component;
//// @input string text = ""
//
//function updateText(utterance) {
//    script.component.text = utterance;
//    //print("updated!");
//}
//
//var updateEvent = script.createEvent('UpdateEvent');
//
//// HTTP Request Part
//
//// @input Asset.RemoteServiceModule remoteServiceModule
///** @type {RemoteServiceModule} */
//var remoteServiceModule = script.remoteServiceModule;
//
//// Interval in milliseconds (30 seconds)
//var intervalDuration = 3000;
//
//// Function to send HTTP request to Flask server
//function sendRequest() {
//    var httpRequest = RemoteServiceHttpRequest.create();
//
//    // Update the URL to point to your Flask server
//    httpRequest.url = 'https://snaptranscription-dacbce1f45d3.herokuapp.com/getData';
//
//    // Set your Flask endpoint
//    httpRequest.method = RemoteServiceHttpRequest.HttpRequestMethod.Get;
//
//    print('Sending request!');
//
//    remoteServiceModule.performHttpRequest(httpRequest, function(response) {
//        print('Request response received');
//        print('Status code: ' + response.statusCode);
//        print('Content type: ' + response.contentType);
//        
//        var responseBody = response.body;
//        print('Body: ' + responseBody);
//
//        // Parse the body as JSON to extract utterances
//        var utterancesArray = JSON.parse(responseBody);
//
//        // Display the last three utterances
//        if (utterancesArray.length > 0) {
//            // Get the last three utterances (or fewer if there are less than 3)
//            var lastThreeUtterances = utterancesArray.slice(-3).map(function(item) {
//                return item.utterance;
//            }).join('\n\n');
//            
//            updateEvent.bind(function() {
//                updateText(lastThreeUtterances);
//            });
//
//            // Display the last three utterances
//            print('Last Three Utterances: \n' + lastThreeUtterances);
//        } else {
//            print('No utterances found');
//        }
//    });
//}
//
//// Function to handle time-based execution
//function onUpdateEvent(eventData) {
//    // Send the request on every updateEvent trigger
//    sendRequest();
//}
//
//// Initial request
//sendRequest();
//
//// Schedule a repeating event every 5 minutes
//var event = script.createEvent("UpdateEvent");
//event.bind(onUpdateEvent);
//event.enabled = true;
//
//// Use a timer to limit the execution to your interval (in seconds)
//var elapsed = 0;
//event.onUpdate = function(eventData) {
//    elapsed += 1;
//    if (elapsed >= (intervalDuration / 1000)) {
//        elapsed = 0;
//        onUpdateEvent(eventData);
//    }
//};
print("check to see if we get here");
function onDisableEvent(eventData) {
   sendToGoogleGemini(lastUtterance);
}
// Schedule a repeating event every 5 minutes
var event = script.createEvent("OnDisableEvent");
event.bind(onDisableEvent);
event.enabled = true;

event.onDisable = function(eventData) {
    onDisableEvent(eventDatat);
}



// Function to send the last utterance to Google Gemini API and handle the response
function sendToGoogleGemini(utterance) {
    var geminiRequest = RemoteServiceHttpRequest.create();
    
    // Google Gemini API endpoint (make sure this is correct)
    geminiRequest.url = '';  // Replace with actual URL and key
    geminiRequest.method = RemoteServiceHttpRequest.HttpRequestMethod.Post;

    // Set request body
    geminiRequest.body = JSON.stringify({

       contents: [{

           parts: [{

               text: "Can you define this in one sentence: " + utterance

           }]

       }]

   });
    
    // Set content type to JSON
    geminiRequest.setHeader("Content-Type", "application/json");
    
    print('Sending request to Google Gemini API with utterance: ' + utterance);
    
    remoteServiceModule.performHttpRequest(geminiRequest, function(geminiResponse) {
        print('Received response from Google Gemini API');
        print('Response status code: ' + geminiResponse.statusCode);
        print('Response content: ' + geminiResponse.body);

        var responseJson = JSON.parse(geminiResponse.body);

        // Extract the "text" part from the first candidate
        var geminiText = responseJson.candidates[0].content.parts[0].text;

        // Now call the function to update the UI with this extracted text
        global.updateTextWithGeminiResult(geminiText);
        });
}

// Function to update the text with the Gemini API result
function updateTextWithGeminiResult(llmResponse) {
    // Directly update the text component with the Gemini API response
    updateText(llmResponse);
}
