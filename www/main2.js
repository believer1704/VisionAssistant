$(document).ready(function () {

    // Initialize textillate animation for the text element
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },
    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },
    });

    // Mic button click event
    $("#MicBtn").click(function () {
        eel.playAssistantSound(); // Play sound
        $("#Oval").attr("hidden", true); // Hide oval element
        $("#SiriWave").attr("hidden", false); // Show SiriWave animation
        eel.allCommands()().then(function (result) {
            // Handle any results here, if necessary
            console.log(result); // You can add any actions based on the result
        }).catch(function (error) {
            console.error("Eel function failed:", error);
        });
    });

    // To handle shortcut (Command + J or Ctrl + J) to activate the mic
    function doc_keyUp(e) {
        if (e.key === 'j' && (e.metaKey || e.ctrlKey)) {
            eel.playAssistantSound(); // Play sound
            $("#Oval").attr("hidden", true); // Hide oval element
            $("#SiriWave").attr("hidden", false); // Show SiriWave animation
            eel.allCommands()().then(function (result) {
                // Handle result
                console.log(result);
            }).catch(function (error) {
                console.error("Eel function failed:", error);
            });
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // Function to play assistant message
    function PlayAssistant(message) {
        if (message != "") {
            $("#Oval").attr("hidden", true); // Hide oval element
            $("#SiriWave").attr("hidden", false); // Show SiriWave animation
            eel.allCommands(message).then(function (response) {
                // Handle response
                $("#SiriWave").attr("hidden", true);
                $(".siri-message").text(response);
                $(".siri-message").textillate('start'); // Start the text animation
            }).catch(function (error) {
                console.error("Error in PlayAssistant:", error);
                $("#SiriWave").attr("hidden", true);
                $(".siri-message").text("An error occurred.");
            });

            $("#chatbox").val(""); // Clear chatbox
            $("#MicBtn").show(); // Show Mic button
            $("#SendBtn").hide(); // Hide Send button
        }
    }

    // Toggle function to hide and display mic and send button
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").show(); // Show Mic Button
            $("#SendBtn").hide(); // Hide Send Button
        } else {
            $("#MicBtn").hide(); // Hide Mic Button
            $("#SendBtn").show(); // Show Send Button
        }
    }

    // Keyup event handler on the chatbox
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message); // Toggle visibility of buttons
    });

    // Send button click event handler
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message); // Play assistant message
    });

    // Enter press event handler on chatbox
    $("#chatbox").keydown(function (e) {
        if (e.key === 'Enter') {
            let message = $("#chatbox").val();
            PlayAssistant(message); // Play assistant message when Enter is pressed
        }
    });

});
