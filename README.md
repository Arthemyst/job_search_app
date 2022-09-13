# job_search_app
Application to track python job offers by web scraping

## Website visualization
![image](https://user-images.githubusercontent.com/59807704/189936914-1d84260b-87aa-45b6-b59a-239fe877edb5.png)

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Arthemyst/job_search_app.git
$ cd job_search_app
```

This project requires Python 3.6 or later.

Create a virtual environment to install dependencies in and activate it:

Linux:
```sh
$ python3 -m venv env
$ source env/bin/activate
```

Then install the dependencies:
```sh
(env)$ pip install -r requirements.txt
```

To run tests:

```sh
(env)$ python3 -m pytest tests_scraping_functions.py
```

Application runs in terminal. Please run app by streamlit:
```sh
(env)$ cd app
(env)$ streamlit run app.py
```
