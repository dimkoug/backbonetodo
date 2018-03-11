(function($){
    $(document).ready(function(){
      $('#id_form').on('submit', function(e){
          e.preventDefault();
          $.ajax({
              url: $(this).attr('action'),
              method: $(this).attr('method'),
              data: $(this).serialize(),
              datatype: 'json',
              success: function(response){
                $('.result').html('');
                var data = eval(response);
                for (var key in data) {
                  if (data.hasOwnProperty(key)) { // this will check if key is owned by data object and not by any of it's ancestors
                    $('.result').append(key + ':' + data[key] + '</br>'); // this will show each key with it's value
                  }
                }
               }
         });
      });
    });
})(jQuery)
