# Deployment and Payment setup

- The app was deployed with [Heroku](https://www.heroku.com/).

- The database was made with [PostgreSQL from Code Institute](https://dbs.ci-dbs.net/).

- AWS S3 was used for media files. [AWS S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/GettingStarted.html)

- The app can be reached by the [link](https://tempusap-74bb3112eef0.herokuapp.com/).

---

## Local deployment

1. Clone the repository.

    - ```git clone https://github.com/cptvalleyberg84/tempus-author-platform```

2. Go to the ```tempus_config``` directory.

    - ```cd tempus_config```

3. Create a virtual environment.

    - ```python -m venv env```

    - ``` .\env\Scripts\Activate```

4. Install all dependencies.

    - ```pip install -r requirements.txt```

5. Create a ```env.py``` file.

    - ```touch env.py```

6. Add the following lines to ```env.py```:

    - ```import os```
    - ``` os.environ.setdefault('SECRET_KEY', 'django-secure-6_-lf9g(&krgzr418l0c2e3%-dj#vzb7_3ve4xhh*&9t(0@')``` = your secret key.
    -``` os.environ['DEVELOPMENT'] = 'True' ```= your development mode

    you can add for later (i found it a very effective to help find production bugs)
    -``` # os.environ['DEBUG'] = 'True' ```
    -``` # os.environ['USE_AWS'] = 'True' ```
    NOTE: these 2 lines above are commented out (use development or USE AWS , Debug = true - if you want to Debug Production while USE_AWS)
    
    Continue with
    -``` os.environ.setdefault('DATABASE_URL', 'your postgres link') ```
    - ```os.environ["DATABASE_URL"] = 'your database url' ```
    -``` os.environ['GOOGLE_FORM_URL'] = 'your google scripts link from your google sheets file'```
    -``` os.environ['AWS_ACCESS_KEY_ID'] = 'your AWS access ID' ```
    -``` os.environ['AWS_SECRET_ACCESS_KEY'] = 'your AWS  secret access key' ```
    Setup you email here, and stripe configuration.

7. Create and migrate the database.

8. Create the superuser.

    - ```python manage.py createsuperuser```

9. Run the server.

    - ```python manage.py runserver```

10. Access the website by the link provided in terminal. Add ```/admin/``` at the end of the link to access the admin panel.

---

**The app is deployed to Heroku but Heroku has removed its free tier services from November 29 2022**

---

## Heroku Deployment


1. Create a Heroku account if you don't already have one.

2. Create a new app on Heroku.

    1. Go to the [Heroku dashboard](https://dashboard.heroku.com/apps).
    2. Click on the "New" button.
    3. Click on the "Create new app" button.
    4. Choose a name for your app.
    5. Choose a region.
    6. Click on the "Create app" button.

3. In your app, go to the "Settings" tab, press "Reveal Config Vars", and add all the same variables that you have stored in your env.py file.

5. In your app go to the "Deploy" tab.

    1. If it's already possible, connect your Heroku account to your GitHub account and then click on the "Deploy" button.
    2. If not, you need to copy the Heroku CLI command to connect your heroku app and your local repository.

        - ```heroku git:remote -a <your-heroku-app-name>```

6. Go to your local repository.

7. Setup your heroku at the website or login to your Heroku account in your terminal and connect your local repository to your heroku app.

    1. ```heroku login -i``` - Enter all your Heroku credentials it will ask for.
    2. Paste the command you copied from step 5 into your terminal.

8. Create Procfile.

    This project uses Gunicorn to ```web: gunicorn your_app_name.wsgi```

9. Create ```requirements.txt```. This can be done by running the following command:

    - ```pip freeze > requirements.txt```

    It's important that you overwrite the file in the rep if you change any requirements.

10. Add and commit all changes.

11. Push your changes to GitHub.

    - ```git push```

12. Deploy in heroku and check your app's logs in heroku dashboard and ensure everything is working.

---

## AWS S3 Setup 

1. Create a new S3 bucket.
2. Configure the bucket to accept public access.
3. Add a new policy to the bucket in permissions to allow public access.

        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "your-bucket-ARN/*"
                }
            ]
        }

4. Setup CORS Cross Origing in your S3 bucket permissions.

        [
            {
                "AllowedHeaders": [
                    "*"
                ],
                "AllowedMethods": [
                    "GET",
                    "POST",
                    "PUT"
                ],
                "AllowedOrigins": [
                    "*"
                ],
                "ExposeHeaders": [
                    "ETag"
                ],
                "MaxAgeSeconds": 3000
            }
        ]

5. Upload the media files to the bucket.

6. Update the AWS_S3_CUSTOM_DOMAIN and AWS_STORAGE_BUCKET_NAME settings in your settings.py and env.py file.

7. Update the AWS S3 settings in your settings.py file.

8. The static files should be uploaded when USE_AWS is set to True in your env.py file, with the command: 
    - python manage.py collectstatic

    (for the testing of production at your local environment)

    - The files will be uploaded automatically in properly set Heroku.
9. Commit and push the changes to GitHub.
10. Deploy in heroku and check your app's logs in heroku dashboard and ensure everything is working.