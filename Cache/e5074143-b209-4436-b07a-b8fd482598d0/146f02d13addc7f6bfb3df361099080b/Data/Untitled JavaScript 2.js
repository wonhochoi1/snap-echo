// @input Component component;
//@input string text = ""

function updateText(llm) {
    script.component.text = llm;
    print("Updated text: " + llm);
}

// Make updateTextWithGeminiResult globally accessible
global.updateTextWithGeminiResult = function(llmResponse) {
    updateText(llmResponse);  // Update the text with LLM response
};

var updateEvent = script.createEvent('UpdateEvent');
updateEvent.bind(function() {
    
});
