$(document).ready(function() {
$('.info').css('display','none');
    $('#id-contests').click(function(){
            $('.contests').css('display','flex');
            $('.tasks').css('display','none');
            $('.info').css('display','none');
        }
    );
    $('#id-tasks').click(function(){
            $('.contests').css('display','none');
            $('.tasks').css('display','flex');
            $('.info').css('display','none');
        }
    );
    $('#id-info').click(function(){
            $('.info').css('display','flex');
            $('.tasks').css('display','none');
            $('.contests').css('display','none');
        }
    );




const accordionItemHeaders = document.querySelectorAll(
  ".accordion-item-header"
);

accordionItemHeaders.forEach((accordionItemHeader) => {
  accordionItemHeader.addEventListener("click", (event) => {
    // Uncomment in case you only want to allow for the display of only one collapsed item at a time!

    // const currentlyActiveAccordionItemHeader = document.querySelector(".accordion-item-header.active");
    // if(currentlyActiveAccordionItemHeader && currentlyActiveAccordionItemHeader!==accordionItemHeader) {
    //   currentlyActiveAccordionItemHeader.classList.toggle("active");
    //   currentlyActiveAccordionItemHeader.nextElementSibling.style.maxHeight = 0;
    // }

    accordionItemHeader.classList.toggle("active");
    const accordionItemBody = accordionItemHeader.nextElementSibling;
    if (accordionItemHeader.classList.contains("active")) {
      accordionItemBody.style.maxHeight = accordionItemBody.scrollHeight + "px";
    } else {
      accordionItemBody.style.maxHeight = 0;
    }
  });
});


var menu = document.querySelector('.nav__list');
var burger = document.querySelector('.burger');
var doc = $(document);
var l = $('.scrolly');
var panel = $('.panel');
var vh = $(window).height();

var openMenu = function() {
  burger.classList.toggle('burger--active');
  menu.classList.toggle('nav__list--active');
};

// reveal content of first panel by default
panel.eq(0).find('.panel__content').addClass('panel__content--active');

var scrollFx = function() {
  var ds = doc.scrollTop();
  var of = vh / 4;

  // if the panel is in the viewport, reveal the content, if not, hide it.
  for (var i = 0; i < panel.length; i++) {
    if (panel.eq(i).offset().top < ds+of) {
     panel
       .eq(i)
       .find('.panel__content')
       .addClass('panel__content--active');
    } else {
      panel
        .eq(i)
        .find('.panel__content')
        .removeClass('panel__content--active')
    }
  }
};


var scrolly = function(e) {
  e.preventDefault();
  var target = this.hash;
  var $target = $(target);

  $('html, body').stop().animate({
      'scrollTop': $target.offset().top
  }, 300, 'swing', function () {
      window.location.hash = target;
  });
}

var init = function() {
  burger.addEventListener('click', openMenu, false);
  window.addEventListener('scroll', scrollFx, false);
  window.addEventListener('load', scrollFx, false);
  $('a[href^="#"]').on('click',scrolly);
};

doc.on('ready', init);

});


$('.sort').click(function (){
    var tasks = $(".tasks").css("display");

    var val1 = $(".r1:checked").val();
    var val2 = $(".r2:checked").val();

    var val3 = [];


    $('input[name="ch"]:checked').each(function() {
        val3.push(this.value);
    });

    if (tasks !== 'none') {
        window.location = '/sort?val1=' + val1 + '&val2=' + val2 + '&val3=' + val3.toString() + '&section=tasks';
    } else {
        window.location = '/sort?val1=' + val1 + '&val2=' + val2 + '&val3=' + val3.toString() + '&section=contests';

    }

    // jQuery.ajax({
    // url: "/sort",
    // type: "GET",
    // contentType: 'application/json; charset=utf-8',
    // data:{"val1":val1,"val2":val2,"val3":val3.toString()},
    // success: function (resultData) {
    //     alert(resultData)
    // },
    // error: function (jqXHR, textStatus, errorThrown) {alert("GG");
    // },
    // timeout: 120000,
    // });
})