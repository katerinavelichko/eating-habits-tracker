$(function () {
    $('.carousel-item').eq(0).addClass('active');
    var amount = $('.carousel-item').length;
    var current = 0;
    $('#moveRight').on('click', function () {
        var next = current;
        current = current + 1;
        SlidePage(next, current);
    });
    $('#moveLeft').on('click', function () {
        var prev = current;
        current = current - 1;
        SlidePage(prev, current);
    });

    function SlidePage(prev, next) {
        var slide = current;
        if (next > amount - 1) {
            slide = 0;
            current = 0;
        }
        if (next < 0) {
            slide = amount - 1;
            current = amount - 1;
        }
        $('.carousel-item').eq(prev).removeClass('active');
        $('.carousel-item').eq(slide).addClass('active');
        setTimeout(function () {

        }, 800);


        console.log('current ' + current);
        console.log('prev ' + prev);
    }
});