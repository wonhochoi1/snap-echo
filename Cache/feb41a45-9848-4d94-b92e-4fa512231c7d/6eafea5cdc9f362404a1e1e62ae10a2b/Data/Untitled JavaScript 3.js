// @input Component component;
//@input string text = ""


function updateText(llm) {
    script.component.text = llm;
    print("updated!");
}

var updateEvent = script.createEvent('UpdateEvent');
updateEvent.bind(function() {
    updateText("test");
});