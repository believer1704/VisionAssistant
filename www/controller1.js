$(document).ready(function () {
    // Display the message passed from Python
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }
    //Display hood
    eel.expose(Showhood)
    function Showhood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }
});
