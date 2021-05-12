$(document).ready(function() {
    // Clears value from input
    $(".form-control").val("");

    $(document).click(function(e) {
        if($(e.target).is(".form-control")) {
            if($(".form-control").val()) {
                $(".dropdown-menu").toggle(true);
            }
        } else {
            $(".dropdown-menu").toggle(false);
        }
    });

    var typingTimer;                // timer identifier
    var doneTypingInterval = 1000;  // time in ms. 1s = 1000ms.

    // on keyup, start the countdown
    $(".form-control").keyup(function() {
        clearTimeout(typingTimer);
        input = $(".form-control").val();
        if (input) {
            typingTimer = setTimeout(doneTyping, doneTypingInterval, input);
        }
    });
    
    // user is "finished typing," do something
    function doneTyping(user_input) {
        $.ajax({
            url: "search_spotify/" + user_input + "/",
            success: function(result) {
                result = $.parseJSON(result);
                children = $(".dropdown-menu").children();
                for(var i = 0; i < result.length; i++) {
                    $(children[i]).text(result[i]["track"] + " | " + result[i]["artists"].join(", "));
                    $(children[i]).attr("href", "playlist/" + result[i]["id"]);
                }

                $(".dropdown-menu").toggle(true);
            }
        });
    }                
});