$(document).ready(function(){
    jQuery.validator.addMethod(
        "multiemails",
        function(value, element) {
            if (this.optional(element)) // return true on optional element
                return true;

            var emails = value.split(/[;,]+/); // split element by , and ;
            valid = true;
            for (var i in emails) {
                value = emails[i];
                valid = valid &&
                jQuery.validator.methods.email.call(this, $.trim(value), element);
            }

            return valid;
        },
        jQuery.validator.messages.multiemails
    );

    $('#scriptForm').validate({
        rules: {
            myconsole: { required: true },
            subject:   { required: true },
            emails:    { required: true, multiemails: true },
        },
        messages: {
            myconsole: {
                required: 'You forgot to fill in the script field.'
            },
            subject: {
                required: 'You forgot to fill in the mail subject.'
            },
            emails: {
                required: 'You forgot to fill in the email address.',
                multiemails: 'You must enter a valid email address.'
            }
        }
    });
});
