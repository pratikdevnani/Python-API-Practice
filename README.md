To create a virtual environment in your root directory

```
python -m venv ./venv
```

Make sure that you set your python interpreter as the 

```
.\venv\Scripts\python.exe
```

To start the virtual environment in the terminal, use the following command:

```
venv\Scripts\activate
```

To stop the virtual environment:

```
deactivate
```

To run the application using fast api:

```
uvicorn main:app --reload
```

Tip: FastAPI matches the first request path with the functions and returns. So if there are 2 or more methods with the same path route, the first one is the one that will always be sent as response.