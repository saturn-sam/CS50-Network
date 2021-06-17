document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#edit-button').forEach(function(button) {
        button.onclick = function() {
         $('#edit-input').val('');
         abc = button.dataset.content;
         console.log(abc);
         $('#edit-input').val(abc);
         $('#post-id-container').val(button.dataset.postid);
        }
    });
 });
 $('.edit-post').click(function (event) {
     event.preventDefault()
     var postId = $('#post-id-container').val()
     var content = $('#edit-input').val()

     $.ajax({
     type: "POST",
     url: `/posts/edit/${postId}`,
     data: {
         csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
         post_id: postId,
         textarea: content
     },
     success: function(data) {
         $('.modal-edit').modal('hide')
         var content = $('#edit-input').val()
         $(`.post-object-content${postId}`).html(content)
     }
     })
 })

 $('.like').click(function(event){
    event.preventDefault();
    var postid;
    var total;
    var value;
    postid = $(this).data("postid");
    $.ajax(
    {
        type:"GET",
        url: "/likedislikepost",
        data:{
                post_id: postid
        },
        success: function( data ) 
        {
            total = $('#'+ postid).attr("data-total")
            if ($('#'+postid).attr("data-value") == 'Like'){
                $( '#liked'+postid ).text((parseInt(total) + 1));
                $( '#like'+postid ).css('color', 'red')
                $('#'+postid).attr("data-total", parseInt(total) + 1)
                $('#'+postid).attr("data-value", 'Unlike')
            }
            else{
                $( '#liked'+postid ).text((parseInt(total) - 1));
                $( '#like'+postid ).css('color', 'black')
                $('#'+postid).attr("data-total", parseInt(total) - 1)
                $('#'+postid).attr("data-value", 'Like')
            }
        },
        error: function()
        {
            alert("Please login to like the post.");
        }
    })

    
})