function speakMessage(msg, lang) {
  console.log('Playing ' + msg + ' using browser TTS through util');
  let utterance = new SpeechSynthesisUtterance(msg);
  utterance.lang = lang;
  window.speechSynthesis.speak(utterance);
};
