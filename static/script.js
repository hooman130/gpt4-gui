$(document).ready(function() {
    $('#user-input').focus();

    $('#send-button').click(function() {
        var userInput = $('#user-input').val();
        if (userInput) {
            $('#chatbox').append('<div class="message user-message"><strong>You:</strong> ' + userInput + '</div>');
            $('#user-input').val('');
            $('#chatbox').append('<div id="typing" class="message ai-message"><strong>GPT-4:</strong> Typing...</div>');
            $.ajax({
                url: '/chat',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({message: userInput}),
                success: function(data) {
                    $('#typing').remove();
                    $('#chatbox').append('<div class="message ai-message"><strong>GPT-4:</strong> ' + data.message + '</div>');
                    $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                }
            });
        }
    });

    $('#user-input').keypress(function(e) {
        if (e.which == 13) {  // Enter key
            $('#send-button').click();
        }
    });
});
