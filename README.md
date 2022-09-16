# job_search_app
Application to track python job offers by web scraping from websites:
- nofluffjobs.com
- pracuj.pl
- bulldogjob.pl

Streamlit app gives possibility to filter offers by job position (junior, trainee), website or publication date.
User can download filtered offers as csv file.
Added button to upload current offers details.

## Website visualization
![image](https://user-images.githubusercontent.com/59807704/190631081-6735d007-8f9d-42d1-b7fc-ef604f27e1f3.png)
![image](https://user-images.githubusercontent.com/59807704/190631271-c3dca8d3-2963-413b-90d9-637d0de307e0.png)


## Setup
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
(env)$ streamlit run streamlit_app.py
```
