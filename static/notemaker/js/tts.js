read_msg = function (msg, lang){
    console.log('Playing ' + msg + ' using browser TTS');
    let utterance = new SpeechSynthesisUtterance(msg);
    utterance.lang = lang;
    window.speechSynthesis.speak(utterance);
}

$( document ).on('click', '.mp3', function(){
    let msg_text = $(this).attr("msg");
    read_msg(msg_text, "fr-FR");
});

$("#resultWindow").bind('isFlipped', function(){
    let msg_text = $("#resultWindow").find(".back").find(".mp3").attr("msg");
    read_msg(msg_text, "fr-FR");
});
