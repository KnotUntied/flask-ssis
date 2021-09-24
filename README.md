# Flask - Simple Student Information System

Application is expected to have CRUDL and search functionality for students, courses, and colleges.

## Installation and Usage (Development)

MySQL is required. Also see included SQL files.
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

## Resources

- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [MySQL Tutorial](https://www.mysqltutorial.org/)
- [How to display a confirmation dialog when clicking an \<a\> link?](https://stackoverflow.com/questions/10462839/how-to-display-a-confirmation-dialog-when-clicking-an-a-link)
- [Modify query parameters in current GET request for new url](https://stackoverflow.com/questions/31120921/modify-query-parameters-in-current-get-request-for-new-url)
- [[AF] Multiple of the same WTForms form on one page.](https://www.reddit.com/r/flask/comments/86yf1t/)
- [Nyaa](https://github.com/nyaadevs/nyaa)