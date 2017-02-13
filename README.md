The requirements.txt file lists the django packages that are needed.
Make sure to install them before starting the server.

To start the server, run the script run.sh using:
sh run.sh

and then go to the browser and type http://127.0.0.1:8000

In folder yesua: 
	media stores/consists all the documents and images uploaded by the user
	site_media contains all the static resources used by the platform like css, js, images, etc

    templates contains all the html files:
        index.html -- format for showing a lesson plan, i.e. the Engage pahse then the Explain and Evaluate phase
        homepage.html -- displays the three buttons: Create/Upload/Search lesson plans if user logged in otherwise the welcome page
	    
        list.hmtl -- showing user uploaded documents/images as a list
	    search_results_terse.html -- format for displaying lesson plans in existing database matching user's request'
        
        form.html -- landing page for creating lesson plan
        search.html-- landing page for searching lesson plans
        upload.html -- landing page for uploading a lesson plan

rest are normal files required for a standard django project

In create_lesson_plan folder:
	migrations include all the changes made in the models, which is automatically updated by the commands (in run.sh):
		python manage.py makemigrations
		python manage.py migrate

	summsrch.py is the file which applies summer_search algorithm to the results returned by bing
	bing.py implements bing search
	forms.py includes the form created to allow uploads
	rest all the defined functions are in views.py
<create_lesson_plan>: displays the page for creating a new lesson plan using form.html from the templates directory in the yesua1 folder 
<show_lesson_plan>: based on the input received in the create_lesson_plan url, sends queries to bing, fetches, parses and filters results and displays them in the format of index.html file (again from the templates directory)
<remove_from_lp>: handle press of x button from user to delete an item from the lesson plan
<save_lesson_plan>: MAIN FUNCTION!!!
<search_lp>: displays the page for searching existing lesson plans using the search.html template file
<display_lesson_plan>: show a specific lesson plan based on user selection after search
<upload>: displays the page for uploading lesson plan, basically choosing the lesson plan (based on subject, course and lesson names) to upload user-supplied document/image to
<upload_lp>: handle press of upload button from user to render generic list.html page with an option to upload documents/images
<list>: handle press of uplaod buttions when user is in the /upload_lp page by adding the uploaded item to a list uploaded so far..
<search_results_terse>: show the set of lesson plans matching user's query
using search_results_terse.html template file
