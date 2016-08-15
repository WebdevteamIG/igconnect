var addMOOC = function(){
    var count = parseInt($('.MOOCList').attr('count'));
    count += 1;
    $('.MOOCList').attr('count',count);
    $('.MOOCList').append("<div class='input-field'><textarea class='materialize-textarea' id = 'MOOC" +count+ "'max-length = '100'></textarea><label for='textarea1'>MOOC</label></div>");
}

var addResearch = function(){
    var count = parseInt($('.researchPaperList').attr('count'));
    count += 1;
    $(".researchPaperList").attr('count',count);
    $('.researchPaperList').append("<div class='input-field'><textarea class='materialize-textarea' id = 'researchPaper" +count+ "'max-length = '100'></textarea><label for='textarea1'>Research Paper</label></div>");
}

var addConference = function(){
    var count = parseInt($('.conferenceList').attr('count'));
    count += 1;
    $(".conferenceList").attr('count',count);
    $('.conferenceList').append("<div class='input-field'><textarea class='materialize-textarea' id = 'conference" +count+ "'max-length = '100'></textarea><label for='textarea1'>Conference Attended</label></div>");

}

var check = function(){
    var skillList = [];
    $('.skillTable').DataTable().$('input[type=checkbox]').each(function () {
     if (this.checked) {
       skillList.push(this.name);	    
   }
});

    var MOOCList = [];
    var conferenceList = [];
    var researchPaperList = [];

    var MOOCCount = $('.MOOCList').attr('count');
    var conferenceCount = $('.conferenceList').attr('count');
    var researchPaperCount = $('.researchPaperCount').attr('count');

    $('[id^=MOOC]').each(function(){
        if($(this).val().trim().length > 0){
            MOOCList.push($(this).val());
        }
    });

    $('[id^=conference]').each(function(){
        if($(this).val().trim().length > 0){
            conferenceList.push($(this).val());
        }
    });

    $('[id^=researchPaper]').each(function(){
        if($(this).val().trim().length > 0){
            researchPaperList.push($(this).val());
        }
    });


    var regNum = $('.regNum').val();
    var level = $('.level :selected').val();
    var branch = $('.branch :selected').val();
    var frm = $('.editForm');
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: {'first_name':$('.first_name').val(),'last_name':$('.last_name').val(),'email':$('.email').val(),'skills':JSON.stringify(skillList),'aboutMe':$('.aboutMe').val(),'phoneNum':$('.phoneNum').val(),'share':$('.share').val(),
        'MOOCs':JSON.stringify(MOOCList),'researchPapers':JSON.stringify(researchPaperList),'conferences':JSON.stringify(conferenceList),'level':level,'branch':branch,'regNum':regNum,'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()},
        traditional:true,
        success: function (data) {
            window.location.replace("/profile/view");
        },
        error: function(data) {
            console.log(data);
        }
    });


}

            
$(document).ready(function(){
    $('.skillTable').DataTable();
    //$('#contributers').DataTable();
    $('select').material_select();
    //changeSelect({{userData.branch}},{{userData.level}})
});