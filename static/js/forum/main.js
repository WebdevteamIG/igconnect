

$(document).ready(function(){
    $('#tags').DataTable();
    $('select').material_select();

    tags=[];
    thread={};
    
    $('#addThread').click(function(){
    	$('#tags').DataTable().$('input[type="checkbox"]:checked').each(function(){
    		tags.push($(this).attr("skillId"));
    		console.log($(this).attr("skillId"));
    	});

    	thread['tags']=tags;
    	thread['threadTitle']=$('#threadTitle').val();
    	thread['threadQuestion']=$('#threadQuestion').val();
    	$.ajax({        
            type:"POST",
            url: "../new/",
            data: {
              csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
              'thread': JSON.stringify(thread),
          },
          success: function(data) {  
            console.log(data); 
            window.alert("Thread created successfully")    
        }
    }); 
    });

    $('.viewThread').click(function(){
    	console.log('clicked');
    	window.open("viewThread/?threadId="+$(this).attr('threadId'),"_blank");
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

    



    $('#editSkillsBtn').click(function(){
        
        $('#editSkillsTable').DataTable().$('input[type="checkbox"]:checked').each(function(){
            skills.push($(this).attr("skillId"));
            console.log($(this).attr("skillId"));

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

});


