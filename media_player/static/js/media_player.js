//Autoplay for video and audio
window.addEventListener("load", function (event) {
    var video_players = document.getElementsByTagName('video');
    var audio_players = document.getElementsByTagName('audio');
    var next_media = document.getElementById('nextmedia').value;
    if (video_players.length == 1) {
        var mediaplayer = video_players[0];
    }
    if (audio_players.length == 1) {
        var mediaplayer = audio_players[0];
    }
    var ap_selector = document.querySelector('input[name=autoplay]');
    mediaplayer.onended = function(e) {
        if (ap_selector.checked) {
            if (next_media != "") {
                window.location = next_media;
            }
        }
    }
});
