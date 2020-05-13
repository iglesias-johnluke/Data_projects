#Uni_project.py

#DESCRIPTION
This project reads off the CSV file 'College_data.csv' which contains 18 columns of data
regarding about 800 US colleges; this data is then processed into an SQL database 'colleges.'

The database is then queried according to what the user entered as the first argument at 
the command line (valid queries only include one of the 18 columns/variables from the
data base). The entered column name outputs the top 10 colleges according to that
column variable.

The top 10 college results are then visualized into a barchart for the user to see.
If the user wishes to see a list of the top 10 universities along with the graph,
they can enter 'show' as the 2nd argument at the command line when running the program. 

#INSTALL
This program requires several module imports such as:
csv, sqlite3, sys, matplotlib, numpy

#RUN
the program can run at the command line as follows:

python3 Uni_project.py grad_rate show

