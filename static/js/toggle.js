$('.buttons button').on('click',function(e) {
    if ($(this).hasClass('grid')) {
        $('.container .pic-grid').removeClass('hide');
      	$('.container table').addClass('hide');
    }

    else if($(this).hasClass('table-hover')) {
        $('.container table').removeClass('hide');
      	$('.container .pic-grid').addClass('hide');
    }
});