$(document).ready(function () {
    $('#subscribed').hide();
    $('#backdrop').hide();
    $('#signed-up').hide();

    function validateEmail(email){
        var re = /\S+@\S+\.\S+/;
        return re.test(email);
    }

    //generate fb and twitter links
    var title = encodeURIComponent($("meta[property='og:title']")[0].content);
    var description = encodeURIComponent($("meta[name='description']")[0].content);

    var cookies;
    var app_id = $('#app_id').val();
    var pk = $('#campaign_pk').val();

    function readCookie(name,c,C,i){
        if(cookies){ return cookies[name]; }

        c = document.cookie.split('; ');
        cookies = {};

        for(i=c.length-1; i>=0; i--){
           C = c[i].split('=');
           cookies[C[0]] = C[1];
        }
        return cookies[name];
    }
    email = readCookie('email_'+pk);
    if (email){
        $.post('http://gitviral.com/api/subscriber/'+pk+'/', {
            'app_id': app_id,
            'email' : email,
        },
        function (data) {
            console.log(data);
            if (data['code'] == 200){
                $("#subscribe-form").hide();
                $("#signed-up").show();
                document.getElementById('ref-count').innerHTML = data['referrals'];
                my_ref_id = data['ref_id'];
                document.getElementById('ref_link').innerHTML = myurl+'?ref='+my_ref_id;
                document.getElementById('facebook-link').setAttribute('href','http://www.facebook.com/share.php?u='+myurl+'%3Fref%3D'+my_ref_id+'&title='+title+'%20-%20'+description);
                document.getElementById('twitter-link').setAttribute('href', 'https://twitter.com/intent/tweet?hashtags=gitviral&text='+title+'%20-%20'+description+'&url='+myurl+'%3Fref%3D'+my_ref_id);
            }
        });
    }

    var myurl = document.location.href.split('?')[0];
    
    var queryDict = {}
    location.search.substr(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
    
    var ref = queryDict['ref'];
    var confirmed = queryDict['confirmed'];
    var link = queryDict['my_ref_id'];

    if(!ref)ref='';

    //generate fb and twitter links
    var title = encodeURIComponent($("meta[property='og:title']")[0].content);
    var description = encodeURIComponent($("meta[name='description']")[0].content);

    if (confirmed){
        $("#confirmed-header").innerHTML("Your email has been confirmed.")

        document.getElementById('ref_link').innerHTML = myurl+'?ref='+link;
        document.getElementById('facebook-link').setAttribute('href','http://www.facebook.com/share.php?u='+myurl+'%3fref%3D"+data+"&title='+title+'%20-%20'+description);
        document.getElementById('twitter-link').setAttribute('href', 'https://twitter.com/intent/tweet?hashtags=gitviral&text='+title+'%20-%20'+description+'&url='+myurl+'%3Fref%3D'+link);

        $('#subscribed').fadeIn(300);
        $('#backdrop').fadeIn(300);
    }
    //subscribe Form
    $('#subscribe-form').submit(function () {

        $("#loading-message").show();
        $("#success-message").hide();
        $("#error-message").hide();

        var action = $(this).attr('action');
        var email = $('#email').val();

        if (!validateEmail(email)){
            $("#loading-message").hide();
            $("#error-message").show();
            $("#error-message").text("Enter a valid email.")
            return false;
        } 
        $.post(action, {
            'email': email,
            'ref' : ref,
            'app_id': app_id,
            'url': myurl
        },
        function (data) {
            $("#loading-message").hide();
            if (data == 'iaid'){
                $("#success-message").hide();
                $("#error-message").show();
            }else{
                $("#error-message").hide();
                $("#success-message").show();
                document.cookie = 'email_'+pk+'='+email+';';
                document.getElementById('ref_link').innerHTML = myurl+'?ref='+data;
                document.getElementById('facebook-link').setAttribute('href','http://www.facebook.com/share.php?u='+myurl+'%3fref%3D'+data+'&title='+title+'%20-%20'+description);
                document.getElementById('twitter-link').setAttribute('href', 'https://twitter.com/intent/tweet?hashtags=gitviral&text='+title+'%20-%20'+description+'&url='+myurl+'%3Fref%3D'+data);
                $('#subscribed').fadeIn(300);
                $('#backdrop').fadeIn(300);
            }
        });
        return false;
    });
    //Modal
    $('#close-btn').click(function () {
        console.log('closing');
        $('#backdrop').fadeOut(400, function () {
            $('#backdrop').hide();
        });
        $('#subscribed').fadeOut(300, function () {
            $('#subscribed').hide();
        });
    });
});