

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
    $('#branches').DataTable();
    $('#editSkillsTable').DataTable();
    $('#editContributorsTable').DataTable();
    $('#contributers').DataTable();
    $('select').material_select();
    $(".dropdown-button").dropdown({hover:false});
    $('#loader').hide();
    pageNo = 2; //for django pagination
    skills=[];
    contributers=[];
    branches = [];
    project={};
    $('#addProject').click(function(){
    	$('#skills').DataTable().$('input[type="checkbox"]:checked').each(function(){
    		skills.push($(this).attr("skillId"));
    	});
        $('#branches').DataTable().$('input[type="checkbox"]:checked').each(function(){
            branches.push($(this).attr("branchId"));
        });
    	$('#contributers').DataTable().$('input[type="checkbox"]:checked').each(function(){
    		contributers.push($(this).attr("username"));
    	});
    	project['skills']=skills;
    	project['branches'] = branches;
        project['contributers']=contributers;
    	project['projectName']=$('#projectName').val();
    	project['projectDescription']=$('#projectDescription').val();
        project['shortDesc']=$('#shortDesc').val();
        project['projectImage']=document.getElementById("projectImage").value;

    	$.ajax({        
            type:"POST",
            url: "../addProject/",
            data: {
              csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
              'project': JSON.stringify(project),
          },
          success: function(data) {  
            //Materialize.toast('Project Added successfully', 4000)
            alert("Project Added successfully");
            window.location.href = "../";    
        }
    }); 
    });

    $('.viewProject').click(function(){
    	window.open("viewProject/?projectId="+$(this).attr('projectId'),"_blank");
    });
    var projectId="-1";
    $('#editProjectName').click(function(){
        $('#editProjectNameModal').openModal();
        $('#projectNameChange').val($(this).attr('projectName'));
        projectId=$(this).attr('projectId');
    });


    $('#editProjectDescription').click(function(){
        $('#editProjectDescriptionModal').openModal();
        $('#projectDescriptionChange').val($(this).attr('projectDescription'));
        projectId=$(this).attr('projectId');
    });

    $('#editSkills').click(function(){
        $('#editSkillsModal').openModal();
        // $('#projectDescriptionChange').val($(this).attr('projectDescription'));
        // projectId=$(this).attr('projectId');
    });
    $('#editContributors').click(function(){
        $('#editContributorsModal').openModal();
        // $('#projectDescriptionChange').val($(this).attr('projectDescription'));
        // projectId=$(this).attr('projectId');
    });
    $('#editProjectNameBtn').click(function(){
        $.ajax({        
            type:"POST",
            url: "../updateProject/",
            data: {
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                'projectName': $('#projectNameChange').val(),
                'projectId' : projectId
            },
            success: function(data) {   
                if(data == "unauthorized")
                {
                    Materialize.toast('You are not authorized to make these changes', 4000);
                    window.open("../auth/","_blank");
                }
                else
                {
                    Materialize.toast('Changes made successfully', 4000);
                    window.location.reload();
                }
            }
        });  
    });    

    $('#editProjectDescriptionBtn').click(function(){
        $.ajax({        
            type:"POST",
            url: "../updateProject/",
            data: {
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                'projectDescription': $('#projectDescriptionChange').val(),
                'projectId' : projectId
            },
            success: function(data) {  
                console.log(data); 
                if(data == "unauthorized")
                {
                    window.alert("You are not authorized to make these changes")
                    window.open("../auth/","_blank");
                }
                else
                {
                    window.alert("Project description changed successfully");
                    window.location.reload();
                }
            }
        });  
    });


    $("#addFiles").click(function(){
        //window.open("../testload/","_blank");
        //$('#addPicturesModel').load("../testLoad/")
        $('#addFilesModal').openModal();
        // $.ajax({        
        //         type:"GET",
        //         url: "../passProjectId/",
        //         data: {
        //                 csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
        //                 'projectId' : $(this).attr('projectId')
        //               },
        //         success: function(data) {  
        //             if(data=="done")
        //             {

        //                 $('#addPicturesModal').load("../uploadFiles/")
        //             }
        //         }
        //     });  

});

    $('.deleteFile').click(function(event){
        event.preventDefault();
        var input;
        var r = confirm("This file will be permanently deleted. Press cancel to keep your file");
        if (r == false) 
            return;
        
        
        var documentPath=$(this).attr('documentPath');
        var projectId=$(this).attr('projectId');
        $.ajax({
            type:"POST",
            url:"../deleteDocument/",
            data:{
               csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
               'documentPath':documentPath,
               'projectId':projectId
           },
           success:function(data){
            if(data=="success")
                window.alert("File deleted");
            else
                window.alert("failed to delete");
            window.location.reload();
        }
    });
    });

    $('#editSkillsBtn').click(function(){

        $('#editSkillsTable').DataTable().$('input[type="checkbox"]:checked').each(function(){
            skills.push($(this).attr("skillId"));
           // console.log($(this).attr("skillId"));

        });
        skillList={}
        skillList['skill']=skills
        $.ajax({        
            type:"POST",
            url: "../updateProject/",
            data: {
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                'skillList': JSON.stringify(skillList),
                'projectId' : $(this).attr('projectId')
            },
            success: function(data) {  
                console.log(data); 
                if(data == "unauthorized")
                {
                    window.alert("You are not authorized to make these changes")
                    window.open("../auth/","_blank");
                }
                else
                {
                    window.alert("Project Technologies changed successfully");
                    window.location.reload();
                }
            }
        });  
    });

contributors=[]

$('#editContributorsBtn').click(function(){

    $('#editContributorsTable').DataTable().$('input[type="checkbox"]:checked').each(function(){
        contributors.push($(this).attr("username"));
        console.log($(this).attr("username"));

    });
    contributorList={}
    contributorList['contributors']=contributors
    $.ajax({        
        type:"POST",
        url: "../updateProject/",
        data: {
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
            'contributorList': JSON.stringify(contributorList),
            'projectId' : $(this).attr('projectId')
        },
        success: function(data) {  
            console.log(data); 
            if(data == "unauthorized")
            {
                window.alert("You are not authorized to make these changes")
                window.open("../auth/","_blank");
            }
            else
            {
                window.alert("Project Contributers changed successfully");
                window.location.reload();
            }
        }
    });  
});  

$('input[type="checkbox"]').click(function(){
    
    if($(this).attr('branchId') == 0){ //for ALL named checkbox
        $('input[type="checkbox"]').attr('checked',false);
        $('.all').show();
        $('.category').hide();
        $('.loadMore').show();
        $(this).prop('checked',true);
    }
    else{
        $('.all').hide();
        $('#c1').prop('checked',false);
        $('.projectList').attr('cpageNo',1);
        $('.category').show();
        $('.category').html(' ');
        loadMore(1);
    }
});

$('.submitAnchor').click(function(){
    var form = $(this).closest("form");
    if($('.searchWords').val().length > 0)
        form.submit();
    else
        Materialize.toast('Empty keywords', 4000)
})

$('.loadMore').click(function(){
    //console.log("hello");
    if($('#c1').is(":checked"))
        loadMore(0);
    else{
        //console.log('no checked');
        loadMore(1);
    }
    
});

});


$(document.body).on('click','.rate-btn',function(event){
    event.preventDefault()
})

$(document.body).on('mouseover','.stars',function(){
    $(this).removeClass('white-text');
    $(this).siblings().removeClass('white-text');
    $(this).siblings().addClass('amber-text');
    $(this).addClass('amber-text')
})


$(document.body).on('mouseout','.stars',function(){
    $(this).removeClass('amber-text');
    $(this).siblings().removeClass('amber-text');
    $(this).siblings().addClass('white-text');
    $(this).addClass('white-text')
})


$(document.body).on('click','.ratemodalopener',function(){
    $('#ratemodal').openModal();
    var id=$(this).attr('project');
    $(document.body).on('click','i.stars',function(){
        var rating=$(this).index()+1;
        $.ajax({        
            type:"POST",
            url: "./rate/",
            data: {
                csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
                'projectId': id,
                'rating':rating,

            },
            success: function(data) {  
                //don't reload the page, change the no of stars from here
                window.location.reload()
            }
        })
    })  
})




function addProjects(projects,category){
    if(projects.length == 0)
    {
        Materialize.toast('No more projecs to load', 4000)
        $(".loadMore").remove();
        return;    
    }
    $(".loadMore").remove();
    for(var i = 0;i<projects.length;i++){
        var skills = "<div class='card-action'>";
        for(var j = 0;j<projects[i].skillList.length;j++){
            skills += " <div class='chip'>"+projects[i].skillList[j] + "</div>";
        }
        


        var ratings='<div class="row" style = "margin-bottom:0;margin-left:-10px"><div class = "col m6 s6 l6"><p class="white-text ">';

        if(projects[i].publishedDate.length > 0)
            ratings += "Published on : " + projects[i].publishedDate + "<br/>";
        var r = projects[i].rating2;
        if(r !== "0.0")
            ratings+="Rated "+r+" by "+projects[i].ratingCount+" users";
        else
            ratings+="No Ratings for this project. Be the first one to rate";
        ratings += "</p></div><div class = 'col m6 s6 l6'>";

        for(var j=0;j<projects[i].rating.length-1;j++)
            ratings+='<i class="star material-icons white-text" style = "float:right;font-size:20px">stars</i>';
       
        ratings += "<div class='section'></div> <i  style = 'float:right' class='rate-btn ratemodalopener btn-floating tooltipped waves-effect waves-light' project='{{project.id}}' data-position='bottom' data-delay='50' data-tooltip='Rate Project'><i class='material-icons'>stars</i></i>";
        ratings += "</div></div></div>";

     
        


        var html_str = "<div class = 'row'><a href='viewProject/?projectId="+ projects[i].id +"' target='_blank'>";
        if(i % 3 == 0)
            html_str += "<div class='card green lighten-1 white-text z-depth-2'>";
        else if(i % 3 == 1)
            html_str += "<div class='card teal lighten-1 white-text z-depth-2'>";
        else if(i % 3 == 2)
            html_str += "<div class='card red lighten-2 white-text z-depth-2'>";
        
        html_str += "<div class='card-content'><div class = 'row white-text'><span class='card-title'>"+ projects[i].projectName + "</span><div class = 'divider'></div><div class = 'section'></div><p><b>" + projects[i].user.first_name + " " + projects[i].user.last_name + "</b></p><p class = 'desp'> " + projects[i].projectDescription.substr(0,180) + "</p></div>";
        html_str += ratings;
        html_str += skills;
        html_str += "</div></a></div>";
        if(category == 0)
            $('.all').append(html_str);
        else
            $('.category').append(html_str);
    }
    new_loadMore = $("<div class = 'loadMore col offset-m4 offset-s4' style='cursor:pointer'><a class='waves-effect waves-light btn'><i class='material-icons right'>system_update_alt</i>Load More</a></div>");
  
    new_loadMore.click(function(){
        if($('#c1').is(":checked"))
            loadMore(0);
        else{
            loadMore(1);
        }
    });
    //if(category == 0)
        $('.projectList').append(new_loadMore);
}   




function loadMore(x){                                   
    console.log(x);
    if(x == 0){
        var pageNo = $('.projectList').attr('pageNo');
        $.ajax({type:"GET",
            url:"/dashboard/" + pageNo,
            success: function(data){
                $('#loader').fadeOut();
                addProjects(data,0);
                pageNo = parseInt(pageNo) + 1;
                $('.projectList').attr('pageNo',pageNo);
            },
            error: function(data){
               $('#loader').fadeOut();
               Materialize.toast('No more projecs to load', 4000)
               $(".loadMore").hide();

           },
            beforeSend: function() {
                $('#loader').fadeIn();
            }

       });
    }
else if(x == 1){
        branches = []
        $('.branchBox input:checked').each(function(){
            branches.push($(this).attr('branchId'));
        });
        dataItems = {};
        dataItems['branchList'] = branches;
        dataItems['pageNo'] = $('.projectList').attr('cpageNo');
        $.ajax({
            type: "POST",
            url: '../dashboard/',
            data: { data : JSON.stringify(dataItems)},
            traditional: true,
            success: function(data) {
                $('#loader').fadeOut();
                addProjects(data,1);
                $('.projectList').attr('cpageNo',parseInt(dataItems['pageNo']) + 1)
            },
            error: function(data){
                $('#loader').fadeOut();
               Materialize.toast('No more projecs to load', 4000)
               $(".loadMore").hide();

           },
            beforeSend: function() {
                $('#loader').fadeIn();
            }
});

    }
}


$(document.body).on('click','.skill',function(event){
    event.preventDefault();
    var skill = $(this).attr('skillName');
    window.location.href = '../search/fromDash/?search=' + skill;
})
