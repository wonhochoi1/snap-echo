// //@input Asset.RemoteServiceModule remoteServiceModule
///** @type {RemoteServiceModule} */
//var remoteServiceModule = script.remoteServiceModule;
//
//var httpRequest = RemoteServiceHttpRequest.create();
//
//// Update the URL to point to your Flask server
//httpRequest.url = '';  // Set your Flask endpoint
//httpRequest.method = RemoteServiceHttpRequest.HttpRequestMethod.Get;
//
//print('Sending request!');
//
//remoteServiceModule.performHttpRequest(httpRequest, function (response) {
//  print('Request response received');
//  print(response)
//  print('Status code: ' + response.statusCode);
//  print('Content type: ' + response.contentType);
//  print('Body: ' + response.body);
//  print('Headers: ' + response.headers);
//});

////@input Asset.RemoteServiceModule remoteServiceModule
///** @type {RemoteServiceModule} */
//var remoteServiceModule = script.remoteServiceModule;
//
//// Interval in milliseconds (5 minutes)
////var intervalDuration = 300000;
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
//        // Create a string to display all the utterances
//        var utterancesString = utterancesArray.map(function(item) {
//            return item.utterance;
//        }).join('\n');
//
//        // Display the utterances string
//        print('Utterances:\n' + utterancesString);
//
//        // Optional: you can manipulate or display this string in the UI of your application
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
//    
//};