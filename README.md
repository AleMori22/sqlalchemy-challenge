# sqlalchemy-challenge

In the directory called **SurfUp** you'll find:

1. The **Resources** folder holding the **hawaii.sqlite**,  **hawaii_measurements** and **hawaii_stations**. This are the files with the data that is going to be used for the analysis.

2. The file **climate..ipynb** where all the plotting and the query required by the homework are coded.

3. Lastly the **app.py** file that will run the query required and will display them into different routes.

All the code was made by me with the help of the class material. Also by looking at the resources and stack overflow I was able to script the following error message returned in case the date in imput as start or end date is not correct or out of range.

```
try:
        
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')  
        
        last_date = dt.datetime.strptime(end, '%Y-%m-%d') 
    
    except ValueError:
        abort(400, description="Invalid date format. Please use YYYY-MM-DD format.")

    if start_date > last_date:
        abort(400, description="Start date cannot be after end date.")

    if last_date > dt.datetime(2017, 8, 23) or start_date < dt.datetime(2010, 1, 1):
        abort(400, description="Dates out of range. Please provide dates between 2010-01-01 and 2017-08-23.")
```
