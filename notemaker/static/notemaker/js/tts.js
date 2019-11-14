$( document ).on('click', '.mp3', function(){
    msg_text = $(this).attr("msg");
    console.log('Playing ' + msg_text + ' using browser TTS');
    var utterance = new SpeechSynthesisUtterance(msg_text);
    utterance.lang = "fr-FR";
    window.speechSynthesis.speak(utterance);
});
