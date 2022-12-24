# <p align=center> <a name="top">Flask-trip_form-project_vol_2 </a></p>  


This is the second version of the Trip form project on my github. If you want to check the previous version [click here.](https://github.com/krzysztofgrabczynski/Flask-trip_form-project)


## <p align=center> How it works </p>

Basically, the main idea is to select the specific trip form (as a guest) that can be added only by users with a valid account on this site. Users add new forms where they enter information about the trip and their contact details like email. User can edit his own account (changing password, email) and only his own specific trip form. In addition there is administrator account that can edit users accounts and all trip forms.

This version is more advanced than the previous one and has new features:
- [x] using sqlite database instead of .csv files
- [x] create admin account when login the first time
- [x] login, logout and registration of ther user 
- [x] user account validation and service
  - [x] edit or delete the user account by admin
  - [x] edit account by user
  - [x] checking if the name and email are unique
  - [x] checking if the specific user can edit specific trip form
  - [x] checking if the user is logged in and modifying the appearance of the menu according this information
- [x] edit, delete of the trip form (accordingly if the user has permission, is a guest, or is an administrator)
- [x] changing user permissions by admin


## <p align=center> How to run the application </p>
- Copy the repository 
- Create virtual environment using 'python -m venv venv' in project directory
- Use '. venv/Scripts/activate' to activate the virtual environment
- Install required packages by 'pip install -r pip_install_req.txt'
- Now, you can run the application with this: 'python app.py'
- Everything done! You can open Trip form page in your browser by ctrl + left click on http link in your console

<br><br>

[Go to top](#top) 
