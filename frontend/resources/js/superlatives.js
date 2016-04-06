/**
 * Add a notification event to the view
 * Params:
 *  - type - alert type (see Noty Docs)
 *  - message - message to display
 **/
function notify(type, message) {
    var layoutType = "bottomRight";

    // Set layout type by display size
    if ($(window).width() < 768) {
        layoutType = "bottom";
    }

    if (type == "success") {
        noty({
            layout: layoutType,
            theme: 'csh',
            text: message,
            type: 'success',
            animation: {
                open: 'animated fadeInUp',
                close: 'animated fadeOutDown',
            },
            maxVisible: 1,
            killer: true
        });
    }
    else if (type == "error") {
        noty({
            layout: layoutType,
            theme: 'csh',
            text: message,
            type: 'error',
            animation: {
                open: 'animated fadeInUp',
                close: 'animated fadeOutDown',
            },
            maxVisible: 1,
            killer: true
        });
    } else if (type == "warning") {
        noty({
            layout: layoutType,
            theme: 'csh',
            text: message,
            type: 'warning',
            animation: {
                open: 'animated fadeInUp',
                close: 'animated fadeOutDown',
            },
            maxVisible: 1,
            killer: true
        });
    }
    else {
        noty({
            layout: layoutType,
            theme: 'csh',
            text: message,
            type: 'information',
            animation: {
                open: 'animated fadeInUp',
                close: 'animated fadeOutDown',
            },
            maxVisible: 1,
            killer: true
        });
    }
    setTimeout(function () {
        $('.animated').removeClass("fadeIn");
        $('.animated').addClass("fadeOutDown");
    }, 3000);

    setTimeout(function () {
        $('.animated').remove();
    }, 3500);

}

/* Profile Form Submission */
$("#superlativeForm").submit(function (event) {
    var URL = 'resources/api/';
    event.preventDefault();
    datastring = $("#evalForm").serialize();
    console.log(datastring);

    if ($("#position").val() == "" || $("#comments").val() == "") {
        notify("error", "Required fields must be filled in.")
    }

    $.ajax({
        type: "POST",
        url: URL,
        data: datastring,
        success: function (data) {
            console.log("Success"); //debug
            notify("success", "Thank you for submitting!");
            $(':input', '#evalForm')
                .not(':button, #position, :submit, :reset, :hidden')
                .val('')
                .removeAttr('checked');
            $('#evalForm option[value=eboard]').attr('selected', 'selected');
        },
        error: function (data) {
            notify("error", "Failed to submit! Try again.")
        }
    });

    return false;
});

$(document).ready(function() {
    setTimeout(function() {
        $("#spinnerContainer").fadeOut('slow', function() {
           $("#formContainer").slideDown('slow');
        });
    }, 2000);
});