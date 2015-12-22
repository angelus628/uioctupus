
var iText = '';
$( document ).ready( function( ) {
    $( '.tree li' ).each( function() {
        if( $( this ).children( 'ul' ).length > 0 ) {
            $( this ).addClass( 'parent' );
        }
    });

    $( '.tree li.parent > a' ).click( function( ) {
        $( this ).parent().toggleClass( 'selected' );
        $( this ).parent().children( 'ul' ).slideToggle( 'fast' );
    });

    $( '#all' ).click( function() {
        $( '.tree li' ).each( function() {
            $( this ).toggleClass( 'selected' );
            $( this ).children( 'ul' ).slideToggle( 'fast' );
        });
    });

    function getAttrs(){
        var info  = JSON.parse($('.tree li > a.selected').attr('data-info').replace(",}", "}").replace("{ ", "{"));
        var attrs = {};
        $.each(info, function(k, v){
            k = k.replace('-', '_');
            attrs[k] = decodeURIComponent(v);
        });

        return attrs;
    }

    $('#add_text').on('click', function(){
        var text        = '';
        var param_text  = '';
        var param_op    = '';
        var param_value = '';
        var new_attr    = getAttrs();
        var serial      = $('#screen').attr('data-serial');
        if(new_attr.class === "android.widget.EditText") {
            var own_text = prompt('Digite el texto que va en la caja');
            if(typeof own_text == 'undefined' || own_text == null){ return false; }
            new_attr.text = new_attr.text.split(' ')[0]

            if(typeof new_attr.resource_id != 'undefined'){
                text       += "iText = \"Navigate to: \" + d(resourceId=\""+new_attr.resource_id+"\").info['text'] + \"<br>\"\n";
                text       += "d(resourceId=\""+new_attr.resource_id+"\").clear_text()\n";
                text       += "d(resourceId=\""+new_attr.resource_id+"\").set_text(\""+own_text+"\")\n";
                param_op    = 0;
                param_text  = new_attr.resource_id;
                param_value = own_text;
            }
            else if(new_attr.text !== '') {
                text       += "iText = \"Navigate to: \" + d(textContains=\""+new_attr.text+"\", className=\"" + new_attr.class + "\").info['text'] + '<br>'\n";
                text       += "d(textContains=\""+new_attr.text+"\", className=\"" + new_attr.class + "\").clear_text()\n";
                text       += "d(textContains=\""+new_attr.text+"\", className=\"" + new_attr.class + "\").set_text(\""+own_text+"\")\n";
                param_op    = 1;
                param_text  = new_attr.text;
                param_value = own_text;
            } else if (new_attr.content_desc !== '' && new_attr.content_desc.indexOf('&') == -1 ) {
                text       += "iText = \"Navigate to: \" + d(description=\""+new_attr.content_desc+"\", className=\"" + new_attr.class + "\").info['text'] + '<br>'\n";
                text       += "d(description=\""+new_attr.content_desc+"\", className=\"" + new_attr.class + "\").clear_text()\n";
                text       += "d(description=\""+new_attr.content_desc+"\", className=\"" + new_attr.class + "\").set_text(\""+own_text+"\")\n";
                param_op    = 2;
                param_text  = new_attr.content_desc;
                param_value = own_text;
            }
            if(text !== '') {
                text         += "d.press.enter()\ntime.sleep(20)\n";
                var myconsole = window.parent.document.getElementById('myconsole');
                $(myconsole).val($(myconsole).val() + text);
                $.get('/add_text?serial='+serial+'&op='+param_op+'&text='+encodeURIComponent(param_text)+'&value='+param_value+'&class='+new_attr.class, function(data){ 
                    window.location.reload();
                });
            }
        }
    });

    var getURL = function(){
        return $.ajax('/geturl?serial=' + $('#screen').attr('data-serial'), {
            type: 'GET',
            async: false,
            error: function() {
                console.log('An error occurred');
            }
        }).responseText;
    };

    $('#take_screenshot').on('click', function(){
        var own_text  = prompt('Digite el nombre de la imagen');
        if(typeof own_text != 'undefined'){
            own_text      = own_text.toLowerCase().replace(' ', '-').replace('ñ', 'n');
            var d         = new Date();
            var file_path = 'static/screenshots/' + d.getFullYear() + '-' + ("0" + (d.getMonth() + 1)).slice(-2) + '-' + d.getDate() + '/' + own_text;
            var text      = 'iText += "Navigate to: ' + getURL() + '<br>"\n' + 'd.screenshot("' + file_path + '.png")\nimg.append("' + file_path + '.png")\n';
            var myconsole = window.parent.document.getElementById('myconsole');
            $(myconsole).val($(myconsole).val() + text);
        }
    });

    $('#click_el').on('click', function() {
        var text = "";
        var new_attr = getAttrs();
        var myindex = new_attr.index;
        var serial = $('#screen').attr('data-serial');
        console.log(new_attr['content-desc'].indexOf('&'))
        if (new_attr.text !== '') {
            text += "d(text=\""+new_attr.text+"\", index=\""+new_attr.index+"\").click()\n";
            param_op = 1;
            param_text = new_attr.text;
        } else if (new_attr['content-desc'] !== '' && new_attr['content-desc'].indexOf('&') == -1 ) {
            text += "d(description=\""+new_attr['content-desc']+"\", index=\""+new_attr.index+"\").click()\n";
            param_op = 2;
            param_text = new_attr['content-desc'];
        } else {
            var bounds = new_attr.bounds;
            var coords = bounds.replace(/^\[/, '').replace(/\]$/,'').replace("][", ',').split(',');
            param_op = 3;
            // X coords
            param_text = Math.round(((parseInt(coords[2]) - parseInt(coords[0])) / 2) + parseInt(coords[0]));
            // Y coords
            myindex = Math.round(((parseInt(coords[3]) - parseInt(coords[1])) / 2) + parseInt(coords[1]));
            text += "d.click("+param_text+", "+myindex+")\n";
        }
        text += "time.sleep(20)\n"
        var myconsole = window.parent.document.getElementById('myconsole');
        $(myconsole).val($(myconsole).val() + text);
        $.get('/click?serial='+serial+'&op='+param_op+'&text='+param_text+'&index='+myindex, function(data){
            window.location.reload();
        });
    });

     $('#add_scroll').on('click', function() {
        var deviceInfo = $('#screen').attr('data-info').replace(/'/g,'"').replace(/u"/g,'"').replace(/True/g,"true").replace(/False/g,"false");
        var oJson = JSON.parse(deviceInfo);
        var x = oJson.displayWidth / 2;
        var parts = Math.round(oJson.displayHeight / 5);
        var y0 = parts;
        var y1 = Math.round(parts * 4);
        var text = "d.swipe("+x+","+y1+","+x+","+y0+")\n";
        var serial = $('#screen').attr('data-serial');

        var myconsole = window.parent.document.getElementById('myconsole');
        $(myconsole).val($(myconsole).val() + text);
        $.get('/swipe?serial='+serial+'&x0='+x+'&y0='+y1+'&x1='+x+"&y1="+y0, function(data){
            window.location.reload();
        });
    });

    $('#screen').click(function (e) { //Offset mouse Position
        var posX = $(this).offset().left,
            posY = $(this).offset().top;
        var x =  Math.round(e.pageX - posX),
            y =  Math.round(e.pageY - posY);
        var ok = confirm('Desea capturar un click en las coordenadas: ' + x + ' , ' + y);
        var serial = $('#screen').attr('data-serial');
        if(ok) {
            var text = "d.click("+x+", "+y+")\n";
            text += "time.sleep(20)\n"
            var myconsole = window.parent.document.getElementById('myconsole');
            $(myconsole).val($(myconsole).val() + text);
            $.get('/click?serial='+serial+'&op=3&text='+x+'&index='+y, function(data){
                window.location.reload();
            });
        }
    });

    $('#screen').mousemove(function (e) { //Offset mouse Position
        var posX = $(this).offset().left,
            posY = $(this).offset().top;
        $('#mvcoords').text(Math.round(e.pageX - posX) + ' , ' + Math.round(e.pageY - posY));
    });

    $('.show-info').on('click',function(){
        /**
        * Resaltado
        **/
        $( '.tree li > a' ).removeClass('selected');
        $( this ).addClass('selected');

        /**
        * Info
        **/
        var tmpl = "<th>{key}</th><td>{value}</td>";
        var tmplTable = '<table class="table table-condensed table-bordered" ><tbody>{rows}</tbody></table>';
        //var str_attrs = $(this).attr('data-info');

        var str_attrs = JSON.parse($(this).attr('data-info').replace(",}", "}").replace("{ ", "{"));

        //var attrs = decodeURIComponent(str_attrs.substring(0,str_attrs.length - 1)).split('|');

        var iTmpl = '<tr>';
        var iTmplTable = '';

        var i = 1;
        var bounds = '';

        var attrs = {};
        $.each(str_attrs, function(k, v){
            iTmpl += tmpl.replace('{key}', k).replace('{value}', unescape(decodeURIComponent(v)));

            i++;

            if (k == 'bounds') {
                bounds = unescape(v);
            }
            if (i >= 2) {
                i = 1;
                iTmpl += '</tr>';
            }
        });

        iTmplTable = tmplTable.replace('{rows}', iTmpl);
        $('#info').html(iTmplTable);

        /**
        * Localizacion
        **/

        var coords = bounds.replace(/^\[/, '').replace(/\]$/,'').replace("][", ',').split(',');
        var mycss = {
            "top" : coords[1]+"px",
            "left" : coords[0]+"px",
            "width" : (coords[2] - coords[0])+"px",
            "height" : (coords[3] - coords[1])+"px"
        };
        $('#rect').css(mycss);
    });
});
