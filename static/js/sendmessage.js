$(document).ready(function(){

	$('#send-in-chat').click(function(){
		$.ajax({        
			type:"POST",
			url: "/message/send/",
			data: {
				csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
				'to': $('#send-in-chat').attr('to'),
				'from':$('#send-in-chat').attr('from'),
				'body':$('#body').val(),
			},
			success: function(data) {  
				console.log(data); 
				if(data=='-1')
				{
					alert('Unauthorized');

				}
				else
				{

					var str="<div class='card teal lighten-1 white-text'><div class='card-content'><span class='card-title'><i class='material-icons'>perm_identity</i><span class='font-size:20px'>"+$('#send-in-chat').attr('from')+"</span></span><br/><div class='divider'></div><br/><p style='word-wrap: break-word;'>"+$('#body').val()+"</p><br/><div class='right-align '><div class='chip'>Sent now</div></div></div></div>";
					$('.chatlist').append(str);
					$('#body').val('');
					//window.location.href="../";
				}
			}
		})
	})

	$('#searchText').keyup(function(){
				var query_str = $('#searchText').val();
				$.ajax({
		        type: 'GET',
		        url: "/search/query_user/"+query_str+"/",
		        traditional:true,
		        success: function (data) {
		            if(data.length > 0){
		            	console.log(data);
		            	showUser(data);
		            }
		            else
		                alert("Nothing Found!");
		        },
		        error: function(data) {
		            $("#loader").fadeOut();
		            alert('Error Occured!');
		        },
		        beforeSend: function() {
		            $('#loader').fadeIn();
		        }
		    	});
		

	});

	$('.sendBtn').click(function(){
		$("#messageModal").openModal();
	});


	
})
$('#message').click(function(){
	$('#messageModal').openModal();

	$('#send').click(function(){
		$.ajax({        
			type:"POST",
			url: "/message/send/",
			data: {
				csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
				'to': $('#send').attr('to'),
				'from':$('#send').attr('from'),
				'body':$('#body').val(),
			},
			success: function(data) {  
				console.log(data); 
				if(data=='-1')
				{
					alert('Unauthorized');

				}
				else
				{
					window.location.href="../../message/view/";
				}
			}
		})
	})	
});

function showUser(data){

    $('.userList').html('');
    jsonData = JSON.parse(data);
    users = JSON.parse(jsonData['users']);
   
    if(users.length == 0)
        $('.userList').append('<p><b>No users found</b></p>');
    
    for(var i = 0;i<users.length;i++){
        toAppend = "<div class = 'card'><p>Username: " + users[i]['username']+"</p><p>" + users[i]['first_name'] + " "+ users[i]['last_name'] +"</p></div>"
        $('.userList').append(toAppend);
    }

}