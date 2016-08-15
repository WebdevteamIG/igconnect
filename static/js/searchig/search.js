
function domManipulate(data){

    if(data.length == 0)
    {
        $('.projects').append('Nothing found..');
        return;
    }

    $('.projects').html('');
    $('.users').html('');
    //console.log(data);
    jsonData = JSON.parse(data);
    projects = JSON.parse(jsonData['projects']);
    users = JSON.parse(jsonData['users']);
    if(users.length == 0 && projects.length == 0){

        alert("Nothing Found\n");
        return;
    }
    $('.projects').append("<h6>Projects: </h6> <div class='divider'></div>")
    if(projects.length == 0)
        $('.projects').append('<p><b>No project found</b></p>');

    for(var i = 0;i<projects.length;i++){
        skills = "";
        for(var j = 0;j<projects[i]['skillList'].length;j++){
            skills += projects[i]['skillList'][j].skillName;
            skills += " " 
        }
       // console.log(projects[i]['_id']['$oid'])
        toAppend = "<div class='card blue-grey darken-1 col s12 m6 offset-s1'><div class='card-content white-text'><h5>" +projects[i]['projectName'] +"</h5><p>" + projects[i]['projectDescription'] + "</p><span class='card-title'>Skills</span><br/>"+ skills +" </div><div class='card-action'><a href = '../dashboard/viewProject/?projectId=" + projects[i]['_id']['$oid'] +"' ><button  projectId= "+ projects[i]['_id']['$oid'] + " class='btn waves-effect waves-light viewProject'  type='button'>View Project</button></a></div> </div>"
        $('.projects').append(toAppend);
    }
    $('.users').append("<h6>Users: </h6> <div class='divider'></div>")
    if(users.length == 0)
        $('.users').append('<p><b>No users found</b></p>');
    
    for(var i = 0;i<users.length;i++){
        toAppend = "<div class='card blue-grey darken-1 col s12 m6 offset-s1'><div class='card-content white-text'><h5>" +users[i]['first_name'] + " " + users[i]['last_name'] + "</h5><p>Username: " + users[i]['username'] + "</p> </div><div class='card-action'><a href = '/profile/view/" + users[i]['username'] +"'><button class='btn waves-effect waves-light viewProject'  type='button'>View Profile</button></div> </div>"
        $('.users').append(toAppend);
    }

}


function search(){
    var query_str = $('.searchbar').val();
    $.ajax({
        type: 'GET',
        url: "/search/query/"+query_str+"/",
        data: "project",
        traditional:true,
        success: function (data) {
            if(data.length > 0){
               $("#loader").fadeOut();
                domManipulate(data);
            }
            else
                alert("Nothing Found!");
        },
        error: function(data) {
            $("#loader").fadeOut();
            console.log(data);
            alert('Error Occured!');
        },
        beforeSend: function() {
            $('#loader').fadeIn();
        }
    });
}


