/**
 * Question Options Configuration
 */
superlative_count = 0;
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
                var answers = [];
                for(var i = 0; i < superlative_count; i++)
                {
                    answers.push($("#superlative_" + i).val());
                }
                $.ajax({
                    type: "POST",
                    url: '/submit',
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    data: JSON.stringify({
                        "quote": $("#quote").val(),
                        "history": $("#memory").val(),
                        "answers": answers
                    }),
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
    var allMembers, rtpMembers, eboardMembers;

    $.ajax({
        type: "GET",
        url: "/people",
        success: function (data) {
            allMembers = data.people;
            $.ajax({
                type: "GET",
                url: "/rtps",
                success: function (data) {
                    rtpMembers = data.people;
                    $.ajax({
                        type: "GET",
                        url: "/eboard",
                        success: function (data) {
                            eboardMembers = data.people;
                            $.ajax({
                                type: "GET",
                                url: "/questions",
                                success: function (data) {
                                    var index = 0;
                                    var last_block = $("#mem_outer");

                                    $.each(data, function(idx, value) {
                                        // a
                                        // populate questions
                                        console.log(value.name + ":" + value.type);

                                        var membersList = null;
                                        var duplicate = false;
                                        switch(value.type) {
                                            case "double":
                                                duplicate = true;
                                            case "default":
                                                membersList = allMembers;
                                                break;
                                            case "rtp":
                                                membersList = rtpMembers;
                                                break;
                                            case "eboard":
                                                membersList = eboardMembers;
                                                break;
                                        }

                                        // create div
                                        after_str = '' +
                                        '<div class="row" id="block-' + idx + '">' +
                                             '<div class="col-xs-12 col-sm-offset-1 col-md-offset-2 col-sm-10 col-md-8">' +
                                                 '<div class="panel panel-default">' +
                                                     '<div class="panel-body" style="padding-top:10px;">' +
                                                         '<label class="control-label">' + value.name + '</label>';

                                            // run twice if needed
                                            after_str += '' +
                                                            '<div class="form-group">' +
                                                                 '<select id="superlative_' + index + '" name="superlative_' + index + '" class="form-control"><option selected disabled>Please Select an Option</option></select>' +
                                                                 '<span class="material-input"></span>' +
                                                            '</div>';
                                            index++;
                                            superlative_count++;
                                            if (duplicate) {
                                                after_str += '' +
                                                                '<div class="form-group">' +
                                                                     '<select id="superlative_' + index + '" name="superlative_' + index + '" class="form-control"><option selected disabled>Please Select an Option</option></select>' +
                                                                     '<span class="material-input"></span>' +
                                                                '</div>';
                                                index++;
                                                superlative_count++;
                                            }
                                            after_str += '' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>';

                                        last_block.after(after_str);
                                        $.each(membersList, function (key, val) {
                                                $('#superlative_' + (index - 1)).append($("<option></option>").attr("value", val.id).text(val.name));
                                        });
                                        if(duplicate) {
                                            $.each(membersList, function (key, val) {
                                                    $('#superlative_' + (index - 2)).append($("<option></option>").attr("value", val.id).text(val.name));
                                            });
                                        }
                                        last_block = $("#block-" + idx);
                                    });
                                }
                            });
                            $("#spinnerContainer").fadeOut('slow', function () {
                                 $("#formContainer").slideDown('slow');
                            });
                        },
                    });
                },
            });
        },
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
