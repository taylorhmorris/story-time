function FlashCard(card) {
    this.card_type = card.card_type;
    this.id = card.id;
    this.due_date = card.due_date;
    this.word = card.note.word;
    this.ipa = card.note.ipa;
    this.grammar = card.note.grammar;
    this.definition = card.note.defintion;
    this.example = card.note.example;
    this.expression = card.note.expression;
    this.expression_meaning = card.note.expression_meaning;
    this.image = card.note.image;

    this.getHTML = function() {
        var functionName = "draw"+this.card_type;
        return this[functionName]();
    };
    
    this.drawBack = function(){
        return "<div id='back'><b>"+ this.word +"</b> /"+ this.ipa +"/ <a class='mp3' msg='"+ this.word +"' href='#'>&#128265;</a><br>Definition: "+ this.definition +"<br>Example: "+ this.example +"<br>Image: <img src='data:image/jpg;base64, "+ this.image +"'><br></div><div id='rate_bar_rate' style='display: none;'><button id='rate_0' class='rate_button' card_id='"+this.id+"'>Incorrect</button><button id='rate_1' class='rate_button' card_id='"+this.id+"'>Correct</button><button id='rate_2' class='rate_button' card_id='"+this.id+"'>Easy</button><button class='flipCard'>Flip Card</button></div>";
    };
    
    this.drawAnswerButton = function(){
        return "<div id='rate_bar_show'><button class='flipCard'>Show Answer</button></div>";
    }
    
    this.drawImageToWord = function(){
        let result = "<div id='front'>";
        result += "What word goes with this image:<br><img src='data:image/jpg;base64, "+ this.image +"'></div>";
        
        result += this.drawAnswerButton();
        result += this.drawBack();
        return result;
    };
    
    this.drawWordToImage = function(){
        let result = "What does this word mean:<br><b>"+ this.word +"</b> /"+ this.ipa +"/ <a class='mp3' msg='"+ this.word +"' href='#'>&#128265;</a><br>"
        
        result += this.drawAnswerButton();
        result += this.drawBack();
        return result;
    };
};

$( document ).on('click', '.flipCard', function(){
    console.log("flipping card");
    $("#front").toggle();
    $("#back").toggle();
    $("#rate_bar_show").toggle();
    $("#rate_bar_rate").toggle();
});

$( document ).on('click', '.rate_button', function(){
    let value = $(this).attr('id')[5];
    console.log(value);
    $.ajax({
        url: "../ajax/rate_card/",
        data: {'card_id': $(this).attr('card_id'), 'rating': value},
        dataType: 'json',
        success: function (data) {
            console.log(data);
        }
    }); 
});
