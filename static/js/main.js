
$(document).ready(function(){
    $('.skillTable').DataTable();
    $('#contributers').DataTable();
    $('select').material_select();

    skills=[];
    contributers=[];
    project={};
    $('#addProject').click(function(){
    	$('#skills').DataTable().$('input[type="checkbox"]:checked').each(function(){
    		skills.push($(this).attr("skillId"));
    		console.log($(this).attr("skillId"));
    	});
    	$('#contributers').DataTable().$('input[type="checkbox"]:checked').each(function(){
    		contributers.push($(this).attr("username"));
    	});
    	project['skills']=skills;
    	project['contributers']=contributers;
    	project['projectName']=$('#projectName').val();
    	project['projectDescription']=$('#projectDescription').val();
    	$.ajax({        
				type:"POST",
				url: "../addProject/",
				data: {
						csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
						'project': JSON.stringify(project),
					  },
				success: function(data) {  
			    	console.log(data); 
			    	window.alert("Project added successfully")
			    	window.location.href = "../";    
				}
		    }); 
    });

    $('.viewProject').click(function(){
    	console.log('clicked');
    	window.open("viewProject/?projectId="+$(this).attr('projectId'),"_blank");
    })


});

