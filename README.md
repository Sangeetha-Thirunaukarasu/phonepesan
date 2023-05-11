# phonepe pulse data visulization
phonepe pulse data visualiztion and exploration - A user friendly tool using Streamlit and plotly
I have created a phonepe pulse data vislualisation using streamlit and plotly.
**Technologies used:**
Github cloning,
python - 3.9.16,
pandas - 2.0.1 ,
MySQL(sqlalchemy - 2.0.12 , pymysql - 1.0.3),
Streamlit - 1.22.0,
plotly - 5.14.1

**Steps**:
1 Extracted data from the Phonepe pulse Github repository by git clone
2. Transformed the data into pandas dataframe format and performed necessary cleaning
and pre-processing steps(handling missing values, converting datatypes, case conversion).
3. Inserted the transformed data into a MySQL database using sqlalchemy library to insert the dataframe into table for efficient storage and
retrieval.
4. Created a live geo visualization dashboard using Streamlit and Plotly in Python
to display the data in an interactive and visually appealing manner. plotly.express library is used to plot the geo map of india
5. Fetched the data from the MySQL database and converted into dataframe to display in the dashboard.
6. there are many drop down options given to analyse the data with different factors in different visulization methods
