$( document ).on('click', '.mp3', function(){
    console.log('Playing Word using browser TTS');
    msg_text = $(this).attr("msg")
    var utterance = new SpeechSynthesisUtterance(msg_text);
    utterance.lang = "fr-FR";
    window.speechSynthesis.speak(utterance);
});
