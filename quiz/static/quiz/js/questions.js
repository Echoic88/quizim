$(document).ready(function () {

    //Set the plus and minus buttons for adding/editing quesitons displays correctly 
    function plusMinusBtnsConfig() {
        // Only the button on the last row will be an add row button
        // All the others will delete rows
        $(".add-form-row").hide();
        $(".delete-form-row").show();
        $(".add-form-row:last").show();
        $(".delete-form-row:last").hide();
    }


    function addQuestionRow() {

        let numForms = $("#id_form-TOTAL_FORMS").val();

        let newForm = $(this).closest(".question-form").clone(true);

        //Increment the form number in the name field
        //e.g. "form-2-id" becomes "form-3-id" 
        
        newForm.find("input").each(function () {
            let splitName = $(this).attr("name").split("-");
            let splitId = $(this).attr("id").split("-");
            splitName[1] = numForms;
            splitId[1] = numForms;
            newName = splitName.join("-");
            newId = splitId.join("-");
            $(this).attr({
                "name":newName,
                "id":newId,
            });
        })
            
        newForm.insertAfter($(".question-form").last())
        $(".question-form:last").find("input[type='text']").val("")
            
        numForms++
        $("#id_form-TOTAL_FORMS").val(numForms);

        //Plus and minus buttons display correctly
        plusMinusBtnsConfig()

        // Focus the Question field of the last form row
        $(".question-form:last").find("input:first").focus()
    
    }


    function createPageDeleteQuestionRow() {
        // add request to delete to management form data
        let numForms = $("#id_form-TOTAL_FORMS").val();
        numForms--;
        $("#id_form-TOTAL_FORMS").val(numForms);

        $(this).closest(".question-form").remove();

        //Focus the Question field of the last rows
        $(".question-form:last").find("input:first").focus()
    }

    // Delete a question row when editing a quiz
    // This handles the management form differently to the create page
    // No change is made to TOTAL-FORMS value since all forms will need to be 
    // submitted to server to allow for delete from database
    function editPageDeleteQuestionRow() {
        // add request to delete to management form data
        $(this).siblings("input[type=checkbox]")
            .prop("checked", true)
            .closest(".question-form").children().hide();

        //Focus the Question field of the last rows
        $(".question-form:last").find("input:first").focus()
    }


    
    // call functions
    // When the page loads on the create and edit quiz pages the last row will have
    // a plus button to add a question and other rows should have a minus button to remove
    // a question
    window.onload = plusMinusBtnsConfig();

    // On click of plus/minus buttons on create quiz and edit quiz pages
    $(".add-form-row").on("click", addQuestionRow);
    $(".create-page-delete-form-row").on("click", createPageDeleteQuestionRow);
    $(".edit-page-delete-form-row").on("click", editPageDeleteQuestionRow);


    // Hover over or click on the save button on create quiz or edit quiz pages will focus
    // the save button - this is so the last question entered will save correctly.
    // If focus isnt expressly removed from the form field it saves as a blank entry
    $(".save-quiz-btn").mouseover(function() {
        $(this).focus();
    })
    $(".save-quiz-btn").click(function() {
        $(this).focus();
    });

});