$("button#report_comment_submit").click(function(event) {
    event.preventDefault();
    var heading = jQuery("#survey_popup_title").text();
    var text = jQuery("#survey_popup_text").text();
    var ok = jQuery("#survey_popup_confirm").text();
    var cancel = jQuery("#survey_popup_deny").text();
    var url = jQuery("#survey_popup_url").text();
    $.alerts.okButton = '&nbsp;'+ok+'&nbsp;';
    $.alerts.cancelButton = '&nbsp;'+cancel+'&nbsp;';
    jConfirm(
        text, 
        heading, 
        function(result) {
            if (result == true) {
                window.open(url)
            }
            else {
                jQuery('form#report_comment_form').submit();
            }
        }
    ); 
});

$("a#oira_legal_hide_anchor").click(function(event) {
    event.preventDefault();
    jQuery("a#oira_legal_hide_anchor").hide();
    jQuery("a#oira_legal_show_anchor").show();
    jQuery("div#legal_reference").show(200);
});

$("a#oira_legal_show_anchor").click(function(event) {
    event.preventDefault();
    jQuery("a#oira_legal_hide_anchor").show();
    jQuery("a#oira_legal_show_anchor").hide();
    jQuery("div#legal_reference").hide(200);
});