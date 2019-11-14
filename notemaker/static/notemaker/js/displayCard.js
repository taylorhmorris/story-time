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

    this.getHTML = function() {
        var functionName = "draw"+this.card_type;
        return this[functionName]();
    };
    
    this.drawBack = function(){
        return "<div class=\'back\'><b>"+ this.word +"</b> /"+ this.ipa +"/ <a class=\'mp3\' msg=\'"+ this.word.replace(/[']/ig, "") +"\' href=\'#\'>&#128265;</a><br>Definition: "+ this.definition +"<br>Example: "+ this.example +"<br><img src=\'data:image/jpg;base64, "+ this.image +"\'><br></div><div class=\'rate_bar_rate\' style=\'display: none;\'><button id=\'rate_0\' class=\'rate_button\' card_id=\'"+this.id+"\'>Incorrect</button><button id=\'rate_1\' class=\'rate_button\' card_id=\'"+this.id+"\'>Correct</button><button id=\'rate_2\' class=\'rate_button\' card_id=\'"+this.id+"\'>Easy</button><button class=\'rate_button\' id=\'rate_9\'>Skip Card</button></div>";
    };
    
    this.drawAnswerButton = function(){
        return "<div class='rate_bar_show'><button class='flipCard'>Show Answer</button><button class='rate_button' id='rate_9'>Skip Card</button></div>";
    }
    
    this.drawImageToWord = function(){
        let result = "<span class='flashcard'><div class='front'>";
        result += "What word goes with this image:<br><img src='data:image/jpg;base64, "+ this.image +"'></div>";
        
        result += this.drawAnswerButton();
        result += this.drawBack();
        result += "</span>";
        return result;
    };
    
    this.drawWordToImage = function(){
        let result = "<span class='flashcard'><div class='front'>";
        result += "What does this word mean:<br><b>"+ this.word +"</b> /"+ this.ipa +"/ <a class='mp3' msg='"+ this.word.replace(/[']/ig, "") +"' href='#'>&#128265;</a></div>"
        
        result += this.drawAnswerButton();        
        result += this.drawBack();        
        result += "</span>";
        return result;
    };
    
    this.drawFillInTheBlank = function(){
        let blankedExample = this.example.replace(this.word, "____");
        let result = "<span class='flashcard'><div class='front'>";
        result += "Fill in the Blank:<br>"+ blankedExample +"</div>";
        
        result += this.drawAnswerButton();
        
        let boldedExample = this.example.replace(this.word, "<b>"+this.word+"</b>");
        result += "<div class='back'>"+ boldedExample +"<a class='mp3' msg='"+ this.example.replace(/[']/ig, "") +"' href='#'>&#128265;</a><br><br><b>"+ this.word +"</b> /"+ this.ipa +"/ <a class='mp3' msg='"+ this.word.replace(/[']/ig, "") +"' href='#'>&#128265;</a><br>Definition: "+ this.definition +"<br><img src='data:image/jpg;base64, "+ this.image +"'><br></div><div class='rate_bar_rate' style='display: none;'><button id='rate_0' class='rate_button' card_id='"+this.id+"'>Incorrect</button><button id='rate_1' class='rate_button' card_id='"+this.id+"'>Correct</button><button id='rate_2' class='rate_button' card_id='"+this.id+"'>Easy</button><button class='rate_button' id='rate_9'>Skip Card</button></div>";
        
        result += "</span>";
        return result;
    };
};

function flipCard(){
    console.log("flipping card");
    $("#resultWindow").find(".front").toggle();
    $("#resultWindow").find(".back").toggle();
    $("#resultWindow").find(".rate_bar_show").toggle();
    $("#resultWindow").find(".rate_bar_rate").toggle();
};

function showFrontOfCard(){
    $("#resultWindow").find(".front").show();
    $("#resultWindow").find(".back").hide();
    $("#resultWindow").find(".rate_bar_show").show();
    $("#resultWindow").find(".rate_bar_rate").hide();
}

$( document ).on('click', '.flipCard', function(){
    flipCard();
});

$( document ).on('click', '.rate_button', function(){
    let value = $(this).attr('id')[5];
    //console.log(value);
    if (value == '9'){
        console.log("This would be a 9 string");
        showFrontOfCard();
        $( "#resultModal" ).trigger( "finish-card", [value] );
    } else{
        $.ajax({
            url: "../ajax/rate_card/",
            data: {'card_id': $(this).attr('card_id'), 'rating': value},
            dataType: 'json',
            success: function (data) {
                //console.log(data);
                $( "#resultModal" ).trigger( "finish-card", [value] );
            }
        });
    }
});
