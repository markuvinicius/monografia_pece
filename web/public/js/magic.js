$(document).ready(function(){
  $("form#changeQuote").on('submit', function(e){
      e.preventDefault();
      var data = $('input[name=quote]').val();
      $.ajax({
          type: 'post',
          url: '/unlabeled',
          data: data,
          dataType: 'text'
      })
      .done(function(data){
          $('h1').html(data.quote);
      });
  });
});