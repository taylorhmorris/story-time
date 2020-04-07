/* globals $, document, console, openModal */
/* jshint unused: false */
function drawCard(data) {
	$("#resultWindow").html(data);
	openModal();
}

function viewNote(note_id) {
	$.ajax({
		url: "../ajax/get_note/",
		data: {
			'note_id': note_id
		},
		dataType: 'html',
		success: function (data) {
			$("#resultWindow").html(data);
		}
	});
}

$(document).on('click', '#cardButton', function () {
	console.log('Clicked');
	$.ajax({
		url: "../ajax/anki_create_note/",
		data: {
			'word': $("#cardForm .word").text(),
			'form': $("form").serialize()
		},
		dataType: 'json',
		success: function (data) {
			viewNote(data.note_id);
		}
	});
});

$(document).on('click', '.image', function () {
	console.log('Selecting Image');
	$("#selectedImage").removeAttr('id');
	$("input[name=selectedImg]").val($(this).attr("value"));
	$(this).attr('id', 'selectedImage');
	let msg_text = $("input[name=selectedImg]").val();
	console.log(msg_text);

});