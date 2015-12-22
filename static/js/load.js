$( document ).ready( function( ) {
    $('#refresh').on('click',function(event){
        event.preventDefault();
        var src = $('#page').attr('src');
        console.log(src);
        if(src != "") {
            console.log(src, src.indexOf('?x'))
            if (src.indexOf('?x') == -1 ) {
                $('#page').attr('src',src+'?x='+Math.random());
            } else {
                $('#page').attr('src',src.substr(0,src.indexOf('?x'))+'?x='+Math.random());
            }
        }
    });

    $('#serial_opt').on('change',function(e){
        var serial = $( '#serial_opt' ).val();

        $.ajax({
            url: '/load/'+serial,
            success: function(data){
                console.log(data);
                if(data == 'ok'){
                    $('#page').attr('src','page/'+serial+'?x='+Math.random());
                }
            },
            error: function(data){
                console.log('Error:' +  data);
            }
        }).done(function(data) {
            console.log('Done.');
        });

        var str = 'from uiautomator import Device\n';
        str += 'import time, os, sys\n';
        str += 'from subprocess import call, check_output\n';
        str += 'sys.path.append(os.path.join(os.path.abspath("./scripts")))\n';
        str += 'import myemail\n\n';
                
        str += 'os.popen("adb -s ' + serial + ' shell pm clear com.android.chrome").read()\n';
        str += 'os.popen("adb -s ' + serial + ' shell am start -a android.intent.action.VIEW -n com.android.chrome/com.google.android.apps.chrome.Main -d http://www.google.com/").read()\n';
        str += 'd = Device("' + serial + '")\nimg = []\niText = ""\n';
        $('#myconsole').val(str);
    });

     $('#add_emails').on('click',function(e) {
        var info    = $('#myconsole').val();
        var emails  = $.trim($('#emails').val());
        var aEmails = emails.split(',')
        for (var i = 0; i < aEmails.length; i++ ) {
            aEmails[i] = $.trim(aEmails[i]);
        }
        var subject = $('#subject').val();
        emails      = aEmails.join(', ');
        info       += "myemail.mail(\""+emails+"\", \""+subject+"\", iText, img)\nmyemail.clean(img)\n";
        $('#myconsole').val(info);
     });
});
