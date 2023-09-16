/* globals $, document, console, window, confirm */
/* jshint unused: false, regexpu: false */
function FlashCard(card) {
	this.card_type = card.card_type;
	this.id = card.id;
	this.due_date = card.due_date;
	this.word = card.note.word;
	this.ipa = card.note.ipa;
	this.grammar = card.note.grammar;
	this.definition = card.note.definition;
	this.example = card.note.example;
	this.expression = card.note.expression;
	this.expression_meaning = card.note.expression_meaning;
	this.image = card.note.image;
	this.note_id = card.note.id;
	this.blankedExample = card.note.example.replace(this.word, "____");

	this.questionText = function () {
		return "What does this word mean?";
	};

	this.getHTML = function () {
		let functionName = "draw" + this.card_type;
		return this[functionName]();
	};

	this.imageTag = function () {
		return "<img src=\'data:image/jpg;base64, " + this.image + "\'>"
	};

	this.imageSrc = function () {
		return "data:image/jpg;base64, " + this.image;
	};

	this.drawBack = function () {
		return "<div class=\'back\'><b>" + this.word + "</b> /" + this.ipa + "/ <a class=\'mp3\' msg=\'" + this.word.replace(/[']/ig, "") + "\' href=\'#\'>&#128265;</a><br>Definition: " + this.definition + "<br>Example: " + this.example + "<br><img src=\'data:image/jpg;base64, " + this.image + "\'><br></div><div class=\'rate_bar_rate\' style=\'display: none;\'><button id=\'rate_0\' class=\'rate_button\' card_id=\'" + this.id + "\'>Incorrect</button><button id=\'rate_1\' class=\'rate_button\' card_id=\'" + this.id + "\'>Correct</button><button id=\'rate_2\' class=\'rate_button\' card_id=\'" + this.id + "\'>Easy</button><button class=\'rate_button\' id=\'rate_9\'>Skip Card</button><button class='delete_button' card_id=\'" + this.id + "\'>Delete</button><button class='edit_button' note_id=\'" + this.note_id + "\'>Edit</button></div>";
	};
	this.drawAnswerButton = function () {
		return "<div class='rate_bar_show'><button class='flipCard'>Show Answer</button><button class='rate_button' id='rate_9'>Skip Card</button><button class='delete_button' card_id=\'" + this.id + "\'>Delete</button></div>";
	};

	this.drawImageToWord = function () {
		let result = "<span class='flashcard'><div class='front'>";
		result += "What word goes with this image:<br><img src='data:image/jpg;base64, " + this.image + "'></div>";

		result += this.drawAnswerButton();
		result += this.drawBack();
		result += "</span>";
		return result;
	};

	this.drawWordToImage = function () {
		let result = "<span class='flashcard'><div class='front'>";
		result += "What does this word mean:<br><b>" + this.word + "</b> /" + this.ipa + "/ <a class='mp3' msg='" + this.word.replace(/[']/ig, "") + "' href='#'>&#128265;</a></div>";

		result += this.drawAnswerButton();
		result += this.drawBack();
		result += "</span>";
		return result;
	};

	this.drawFillInTheBlank = function () {
		let blankedExample = this.blankedExample;
		let result = "<span class='flashcard'><div class='front'>";
		result += "Fill in the Blank:<br>" + blankedExample + "</div>";

		result += this.drawAnswerButton();

		let boldedExample = this.example.replace(this.word, "<b>" + this.word + "</b>");
		result += "<div class='back'>" + boldedExample + "<a class='mp3' msg='" + this.example.replace(/[']/ig, "") + "' href='#'>&#128265;</a><br><br><b>" + this.word + "</b> /" + this.ipa + "/ <a class='mp3' msg='" + this.word.replace(/[']/ig, "") + "' href='#'>&#128265;</a><br>Definition: " + this.definition + "<br><img src='data:image/jpg;base64, " + this.image + "'><br></div><div class='rate_bar_rate' style='display: none;'><button id='rate_0' class='rate_button' card_id='" + this.id + "'>Incorrect</button><button id='rate_1' class='rate_button' card_id='" + this.id + "'>Correct</button><button id='rate_2' class='rate_button' card_id='" + this.id + "'>Easy</button><button class='rate_button' id='rate_9'>Skip Card</button></div><button class='delete_button' card_id=\'" + this.id + "\'>Delete</button><button class='edit_button' card_id=\'" + this.id + "\'>Edit</button>";

		result += "</span>";
		return result;
	};
}
