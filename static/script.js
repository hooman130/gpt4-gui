
$(document).ready(function () {
    $('#user-input').focus();

    $('#send-button').click(function () {
        var userInput = $('#user-input').val();
        if (userInput) {
            $('#chatbox').append('<div class="message user-message"><strong>You:</strong> ' + userInput + '</div>');
            $('#user-input').val('');
            $('#chatbox').append('<div id="typing" class="message ai-message"><strong>GPT-4:</strong> Typing...</div>');
            $.ajax({
                url: '/chat',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ message: userInput }),

                success: function (data) {
                    $('#typing').remove();
                    const formattedMessage = '<div class="formatted-message"><div class="message-content"><strong>GPT-4:</strong> ' + data.message.replace(/\n/g, "<br>") + '</div><button class="copy-button-small">Copy</button></div>';
                    $('#chatbox').append(formattedMessage);
                    $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);

                    // Add Click listener to copy button
                    $('.copy-button-small').click(function () {
                        const messageContent = $(this).prev('.message-content').text();
                        navigator.clipboard.writeText(messageContent);
                    });
                },
                error: function (request, status, error) {
                    $('#typing').remove();
                    $('#chatbox').append('<div class="message ai-message error"><strong>GPT-4:</strong> Error! Please try again.</div>');
                    $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                }
            });
        }
    });

    $('#user-input').keypress(function (e) {
        if (e.which == 13) {  // Enter key
            $('#send-button').click();
        }
    });
});
