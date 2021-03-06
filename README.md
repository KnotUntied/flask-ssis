# Flask - Simple Student Information System

Application is expected to have CRUDL and search functionality for students, courses, and colleges.

## Installation and Usage (Development)

MySQL is required. Also see and execute included SQL files.
```sh
mysqld --console
```

Dependencies are to be installed via [pipenv](https://realpython.com/pipenv-guide/#pipenv-introduction) or a regular virtual environment.

Duplicate `.env-template` and `.flaskenv-template` as `.env` and `.flaskenv`, respectively. Replace the values within as needed.
```sh
cp .env-template .env
cp .flaskenv-template .flaskenv
```

Start the development server.
```sh
flask run
```

## Personal Remarks

- Models need more consistent methods
- Some hardcoded values, especially in forms
- May want to list related elements in profiles (e.g. students under a particular course/college, courses under a particular college)

## TODOs

- Hide photo field in Edit Student form if `Remove Photo` is selected
- Use Cloudinary's upload widget instead of server-side upload (allows upload from third-party sources, allows for manual cropping, potentially improves performance by skipping this server and uploading straight to Cloudinary; lack of documentation, potential difficulties in editing/deleting avatars)

## Resources

- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [MySQL Tutorial](https://www.mysqltutorial.org/)
- [How to display a confirmation dialog when clicking an \<a\> link?](https://stackoverflow.com/questions/10462839/how-to-display-a-confirmation-dialog-when-clicking-an-a-link)
- [Modify query parameters in current GET request for new url](https://stackoverflow.com/questions/31120921/modify-query-parameters-in-current-get-request-for-new-url)
- [[AF] Multiple of the same WTForms form on one page.](https://www.reddit.com/r/flask/comments/86yf1t/)
- [Nyaa](https://github.com/nyaadevs/nyaa)