ADMIN CREDENTIALS

Use these credentials to login as an admin:-

1. username    :   'admin'
2. password    :   '1234'

##### How does this work?

1. First User have to register themselves and then login to the program.
2. Logged users are then promted to the upload file page where they can upload files.
3. After uploading files the user can logout.
4. Now from the same login the superuser can login but it will have access to more pages.

List of pages and there access rights:-

1. Homepage: Here list of all uploaded files will be shown from where admin can download and see the contents of the file. This page is only accessible to **admins**.
2. Show Data: Here the content of the file is shown as a table when the ***open*** button is clicked. This page is also accessible only to the **admins**.
3. Upload files: Here any user can upload files. This pages is accessible to both admin and normal users.

Things that admin can do:-
1. Upload files
2. Download files
3. Delete files
4. Open files

Things that normal users can do:-
1. Upload files

Note: Admins can not register themselves from register page. If you want to register new admin you will have to user **python manage.py createsuperuser** command

Following formats are supported to be uploaded:

1. csv
2. xls
3. xlsx
