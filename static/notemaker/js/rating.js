$( document ).on('click', '.flipCard', function(){
    console.log("flipping card");
    $("#front").toggle();
    $("#back").toggle();
    $("#rate_bar_show").toggle();
    $("#rate_bar_rate").toggle();
});

$(".rate_button").click(function(){
    let value = $(this).attr('id')[5];
    console.log(value);
    $.ajax({
        url: "{% url 'ajax-rate-card' %}",
        data: "{'card_id': {{ card.id }}, 'rating': value}",
        dataType: 'json',
        success: function (data) {
            console.log(data);
        }
    }); 
});
