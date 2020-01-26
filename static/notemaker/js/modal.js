function openModal(card){
    $("#resultModal").show();
}

$( document ).ready(function() {
    $("#resultModal").hide();
});

$( document ).on('click', '.close', function(){
    $( "#resultModal" ).trigger('click')
});

$( document ).on('click', '#resultModal', function(event){
    event.stopPropagation();
    if (event.target.id == 'resultModal'){
        $(".modal").hide();
        $("#holdingBay").empty();
    };
});
