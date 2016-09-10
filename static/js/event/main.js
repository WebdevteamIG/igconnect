
var uniqueID = (function() { 
 var id = 0; 
 return function() { return id++; }; 
})(); 

function colorDiv(){
    var x = uniqueID();
    if(x % 3 == 0)
        document.write('<div class="card green lighten-1 white-text z-depth-2">');
    else if(x % 3 == 1)
        document.write('<div class="card teal lighten-1 white-text z-depth-2">');
    else if(x % 3 == 2)
       document.write('<div class="card red lighten-2 white-text z-depth-2">');
}

$(document).ready(function(){
    $('#skills').DataTable();
    $('#editSkillsTable').DataTable();
    $('#editMentorsTable').DataTable();
    $('#mentors').DataTable();
    $('select').material_select();
    $(".dropdown-button").dropdown({hover:false});
    $('#loader').hide();
    pageNo = 2; //for django pagination
    skills=[];
    mentors=[];
    event={};
    $('#addEvent').click(function(){
    	$('#skills').DataTable().$('input[type="checkbox"]:checked').each(function(){
    		skills.push($(this).attr("skillId"));
    	});
    	$('#mentors').DataTable().$('input[type="checkbox"]:checked').each(function(){
    		mentors.push($(this).attr("username"));
    	});
        
    	event['skills']=skills;
        event['mentors']=mentors;
    	event['eventname']=$('#eventname').val();
    	event['eventDescription']=$('#eventDescription').val();
        event['organiser']=$('#organiser').val();
        event['startdate']=$('#sdate').val();
        event['enddate']=$('#edate').val();
        
    	$.ajax({        
            type:"POST",
            url: "/event/addEvent/",
            data: {
              csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
              'event': JSON.stringify(event),
          },
          success: function(data) {  
            //Materialize.toast('Project Added successfully', 4000)
            alert("Event Added successfully");
            window.location.href = "../";   
              
        }
    });     
    });
    
    $('.loadMore').click(function(){
    //console.log("hello");
    if($('#e1').is(":checked"))
        loadMore(0);
    else{
        loadMore(1);
    }
    });
    
    $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year
    format: 'yyyy-mm-dd'
  });
    

    $('input[type="checkbox"]').click(function(){
        if($(this).attr('eId') == 0){ //for ALL named checkbox
//            console.log("here it is")
            $('input[type="checkbox"]').attr('checked',false);
            $('.all').show();
            $('.eventList').attr('cpageNo',1);
            $('.category').hide();
            $('.loadMore').show();
            $(this).prop('checked',true);
        }
        else{
            console.log("here it is")
            $('.all').hide();
            $('#e1').prop('checked',false);
            $('.eventList').attr('cpageNo',1);
            $('.category').show();
            $('.category').html(' ');
            loadMore(1);
        }
    });
    
    
});



function addEvents(events,category){
    if(events.length == 0)
    {
        Materialize.toast('No more events to load', 4000)
        $(".loadMore").remove();
        return;    
    }
    $(".loadMore").remove();
    for(var i = 0;i<events.length;i++){
        var skills = "<div class='card-action'>";
        for(var j = 0;j<events[i].skillList.length;j++){
            skills += " <div class='chip'>"+events[i].skillList[j] + "</div>";
        } 
        

        var html_str = "<div class = 'row'><a href='viewEvent/?projectId="+ events[i].id +"' target='_blank'>";
        if(i % 3 == 0)
            html_str += "<div class='card green lighten-1 white-text z-depth-2'>";
        else if(i % 3 == 1)
            html_str += "<div class='card teal lighten-1 white-text z-depth-2'>";
        else if(i % 3 == 2)
            html_str += "<div class='card red lighten-2 white-text z-depth-2'>";
        
        html_str += "<div class='card-content'><div class = 'row white-text'><span class='card-title'>"+ events[i].eventName + "</span><div class = 'divider'></div><div class = 'section'></div><p><b>" + events[i].user.first_name + " " + events[i].user.last_name + "</b></p><p class = 'desp'> " + events[i].eventDescription.substr(0,180) + "</p><p>starts on : "+events[i].startdate+"</p><p>ends on : "+events[i].enddate+"</p></div>";
        
        html_str += skills;
        html_str += "</div></a></div>";
        if(category == 0)
            $('.all').append(html_str);
        else
            $('.category').append(html_str);
    }
    new_loadMore = $("<div class = 'loadMore col offset-m4 offset-s4' style='cursor:pointer'><a class='waves-effect waves-light btn'><i class='material-icons right'>system_update_alt</i>Load More</a></div>");
  
    new_loadMore.click(function(){
        if($('#e1').is(":checked"))
            loadMore(0);
        else{
            loadMore(1);
        }
    });
    //if(category == 0)
        $('.eventList').append(new_loadMore);
}



function loadMore(x){
    console.log(x);
    if(x == 0){
        var pageNo = $('.eventList').attr('pageNo');
        $.ajax({type:"GET",
            url:"/event/viewall/" + pageNo,
            success: function(data){
                $('#loader').fadeOut();
                addEvents(data,0);
                pageNo = parseInt(pageNo) + 1;
                $('.eventList').attr('pageNo',pageNo);
            },
            error: function(data){
               $('#loader').fadeOut();
               Materialize.toast('No more events to load', 4000)
               $(".loadMore").hide();

           },
            beforeSend: function() {
                $('#loader').fadeIn();
            }

       });
    }
else if(x == 1){
        timing = []
        $('.timebox input:checked').each(function(){
            timing.push($(this).attr('eId'));
        });
        dataItems = {};
        dataItems['eventList'] = timing;
        dataItems['pageNo'] = $('.eventList').attr('cpageNo');
        console.log("hi")
        $.ajax({
            type: "POST",
            url: '/event/viewall/',
            data: { data : JSON.stringify(dataItems)},
            traditional: true,
            success: function(data) {
                $('#loader').fadeOut();
                addEvents(data,1);
                $('.eventList').attr('cpageNo',parseInt(dataItems['pageNo']) + 1)
            },
            error: function(data){
                $('#loader').fadeOut();
               Materialize.toast('No more events to load', 4000)
               $(".loadMore").hide();

           },
            beforeSend: function() {
                $('#loader').fadeIn();
            }
});

    }
}
