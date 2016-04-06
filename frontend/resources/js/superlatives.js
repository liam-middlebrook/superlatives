/**
 * Question Options Configuration
 */

var questions_all = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27];
var questions_eboard = [15];
var questions_rtps = [12, 14];

$(document).ready(function () {

    $.ajax({
        type: "GET",
        url: "/voted",
        success: function (data) {
            if (data.voted) {
                $("#spinnerContainer").fadeOut('slow', function () {
                    $("#thankYouContainer").slideDown('slow');
                });
            } else {
                update_options();
            }
        },
        error: function (data) {
            notify("error", "Unable to retrieve voting status.");
        }
    })


});

/* Form Submission */
$("#submitBtn").click(function (event) {
    // Disable modal buttons and show spinner
    $("#submitConfirmModal button").attr('disabled', 'disabled');
    $("#submitConfirmModal .modal-body p").fadeOut('slow', function () {
        $("#submitConfirmModal .modal-body .spinner").fadeIn('slow', function () {
            if ($("#quote").val() == "" || $("#memory").val() == "") {
                notify("error", "All fields are required. Please try again.");

                // Reset dialog
                $("#submitConfirmModal button").removeAttr('disabled');
                $("#submitConfirmModal .modal-body .spinner").hide();
                $("#submitConfirmModal .modal-body p").show();
                $("#submitConfirmModal").modal('hide');
            } else {
                $.ajax({
                    type: "POST",
                    url: '/submit',
                    data: {
                        "quote": $("#quote").val(),
                        "history": $("#memory").val(),
                        "answers": {
                            superlative_0: $("#superlative_0").val(),
                            superlative_1: $("#superlative_1").val(),
                            superlative_2: $("#superlative_2").val(),
                            superlative_3: $("#superlative_3").val(),
                            superlative_4: $("#superlative_4").val(),
                            superlative_5: $("#superlative_5").val(),
                            superlative_6: $("#superlative_6").val(),
                            superlative_7: $("#superlative_7").val(),
                            superlative_8: $("#superlative_8").val(),
                            superlative_9: $("#superlative_9").val(),
                            superlative_10: $("#superlative_10").val(),
                            superlative_11: $("#superlative_11").val(),
                            superlative_12: $("#superlative_12").val(),
                            superlative_13: $("#superlative_13").val(),
                            superlative_14: $("#superlative_14").val(),
                            superlative_15: $("#superlative_15").val(),
                            superlative_16: $("#superlative_16").val(),
                            superlative_17: $("#superlative_17").val(),
                            superlative_18: $("#superlative_18").val(),
                            superlative_19: $("#superlative_19").val(),
                            superlative_20: $("#superlative_20").val(),
                            superlative_21: $("#superlative_21").val(),
                            superlative_22: $("#superlative_22").val(),
                            superlative_23: $("#superlative_23").val(),
                            superlative_24: $("#superlative_24").val(),
                            superlative_25: $("#superlative_25").val(),
                            superlative_26: $("#superlative_26").val(),
                            superlative_27: $("#superlative_27").val()
                        }
                    },
                    success: function (data) {
                        notify("success", "Thank you for submitting!");
                        location.reload();
                    },
                    error: function (data) {
                        notify("error", "Failed to submit! Please try again later.")

                        // Reset dialog
                        $("#submitConfirmModal button").removeAttr('disabled');
                        $("#submitConfirmModal .modal-body .spinner").hide();
                        $("#submitConfirmModal .modal-body p").show();
                        $("#submitConfirmModal").modal('hide');
                    }
                });
            }

            return false;
        });
    });
});

/**
 * Fetch people lists from the API
 */

function update_options() {
    $.ajax({
        type: "GET",
        url: "/people",
        success: function (data) {
            $.each(data.people, function (key, value) {
                questions_all.forEach(function (currentValue, index, array) {
                    $('#superlative_' + array[index]).append($("<option></option>").attr("value", value.id).text(value.name));
                });
            });

            $.ajax({
                type: "GET",
                url: "/rtps",
                success: function (data) {
                    $.each(data.people, function (key, value) {
                        questions_rtps.forEach(function (currentValue, index, array) {
                            $('#superlative_' + array[index]).append($("<option></option>").attr("value", value.id).text(value.name));
                        });
                    });

                    $.ajax({
                        type: "GET",
                        url: "/eboard",
                        success: function (data) {
                            $.each(data.people, function (key, value) {
                                questions_eboard.forEach(function (currentValue, index, array) {
                                    $('#superlative_' + array[index]).append($("<option></option>").attr("value", value.id).text(value.name));
                                });
                            });

                            $("#spinnerContainer").fadeOut('slow', function () {
                                $("#formContainer").slideDown('slow');
                            });
                        },
                        error: function (data) {
                            notify("error", "Unable to retrieve eboard list.");
                        }
                    });
                },
                error: function (data) {
                    notify("error", "Unable to retrieve RTP list.");
                }
            });
        },
        error: function (data) {
            notify("error", "Unable to retrieve user list.");
        }
    });
}

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