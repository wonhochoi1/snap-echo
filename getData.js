//@input Asset.RemoteServiceModule remoteServiceModule
/** @type {RemoteServiceModule} */
var remoteServiceModule = script.remoteServiceModule;

var httpRequest = RemoteServiceHttpRequest.create();

// Update the URL to point to your Flask server
httpRequest.url = 'http://127.0.0.1:5000/getData';  // Set your Flask endpoint
httpRequest.method = RemoteServiceHttpRequest.HttpRequestMethod.Get;

print('Sending request!');

remoteServiceModule.performHttpRequest(httpRequest, function (response) {
  print('Request response received');
  print('Status code: ' + response.statusCode);
  print('Content type: ' + response.contentType);
  print('Body: ' + response.body);
  print('Headers: ' + response.headers);
});
