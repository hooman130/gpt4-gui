
$(document).ready(function () {
    $('#user-input').focus();

    $('#send-button').click(function () {
        var userInput = $('#user-input').val();
        if (userInput) {
            $('#chatbox').append('<div class="message user-message"><strong>You:</strong> ' + userInput + '</div>');
            $('#user-input').val('');
            $('#chatbox').append('<div id="typing" class="message ai-message"><strong>GPT-4:</strong> Typing...</div>');
            var source = new EventSource('/chat', {
                method: 'POST',
                body: JSON.stringify({ message: userInput }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            source.onmessage = function (event) {
                var data = JSON.parse(event.data);
                if (data.error) {
                    $('#typing').remove();
                    $('#chatbox').append('<div class="message ai-message error"><strong>GPT-4:</strong> Error! Please try again.</div>');
                } else {
                    $('#typing').remove();
                    const formattedMessage = '<div class="formatted-message"><div class="message-content"><strong>GPT-4:</strong> ' + data.message.replace(/\n/g, "<br>") + '</div><button class="copy-button-small">Copy</button></div>';
                    $('#chatbox').append(formattedMessage);
                }
            }
            source.onerror = function (event) {
                console.error("EventSource failed:", event);
                // Handle the error...
            };
        }
    });

    $('#user-input').keypress(function (e) {
        if (e.which == 13) {  // Enter key
            $('#send-button').click();
        }
    });
});
