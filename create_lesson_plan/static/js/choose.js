function addAnnotation(divtype,id)
  {
    var resultDiv = document.getElementById(divtype+id);
    var label = document.createElement("label");
    var savetextBtn = document.createElement("input");
    savetextBtn.setAttribute("type", "button");
    savetextBtn.setAttribute("value", "Save Note");
    savetextBtn.setAttribute("name","Annotation" + id);
    savetextBtn.setAttribute("data-id", id);
    //savetextBtn.setAttribute("onclick", "saveAnnotation(\$id\)");
    //savetextBtn.addEventListener("click", saveAnnotation)

    savetextBtn.addEventListener('click', function(event) {
    		// prevents the default behavior when clicking on the button,
    		// so we can add our own custom behavior
    		event.preventDefault();

    		// 'this' when called inside an event listener always refers to the
    		// element that the event is acting upon -- in this case it's the element
    		// being clicked on, or the button
    		var id = this.getAttribute('data-id');

    		// call the saveAnnotation() function, and pass the ID as a parameter
    		saveAnnotation(id);
    	});




    label.innerHTML="Add Description";
    var textarea = document.createElement("textarea");
    textarea.setAttribute("id", "Annotation" + id);
    textarea.setAttribute("rows", "5");
    textarea.setAttribute("cols", "60");
    textarea.setAttribute("placeholder", "Please add your comments here");
    resultDiv.appendChild(document.createElement("br"));
    resultDiv.appendChild(label);
    resultDiv.appendChild(document.createElement("br"));
    resultDiv.appendChild(textarea);
    resultDiv.appendChild(document.createElement("br"));
    resultDiv.appendChild(savetextBtn);
  }


  function saveAnnotation(id)
  {
    //alert(id);
    var textarea = document.getElementById("Annotation" + id);
    var teachersNote = textarea.value;
    textarea.setAttribute("placeholder", teachersNote);
    textarea.setAttribute("disabled", true);
    //alert("hey wassup");
  }

  function displayresult()
  {
    //alert("hey wassup");
    //document.getElementById("Annotation0_0").readOnly = true;
    var textarea = document.getElementById("Annotation0_0");
    var test1 = document.getElementById("Annotation0_0").value;
    alert(test1);
    textarea.setAttribute("placeholder", test1);
    }

    function createflow()
    {
    //hide all elements that shouldn't be displayed in final lesson plan
    var inputs = document.getElementsByTagName('input');

    for(var i = 0; i < inputs.length; i++) {
        	inputs[i].style.display = 'none';
        //if(inputs[i].type.toLowerCase() == 'text') {
            //alert(inputs[i].value);
        }
  }
  //return window.open( "data:application\/msword,"+escape("<"+"html>"+document.documentElement.innerHTML+"<\/html>")  );

  //my_Window = window.open ("page.htm","myWindow","location=1,scrollbars=1,width=500,height=300");
  //my_Window.moveTo(50,50);
