
# John Iglesias
# Final Project
# 5/13/2020
#115913400


import csv
import sqlite3
import sys
from matplotlib import pyplot as plt
import numpy as np

user_column = sys.argv[1].lower()
conn = sqlite3.connect('college_db.sqlite')
cursor = conn.cursor()

 
def create_db():
    '''reads csv file on college data and processes into database
    called colleges
     '''

    with open('College_Data.csv') as fh:
        spreadsheet = csv.DictReader(fh)

         

        create_q = ''' CREATE TABLE IF NOT EXISTS colleges (college TEXT,
                    private TEXT, apps INTEGER, accept INTEGER, enroll INTEGER,
                    top10perc INTEGER, top25perc INTEGER, f_undergrad INTEGER,
                    p_undergrad INTEGER, outstate INTEGER, room_board INTEGER,
                    books INTEGER, personal INTEGER, phd INTEGER, 
                    terminal INTEGER, sf_ratio REAL, perc_alumni INTEGER,
                    expend INTEGER, grad_rate INTEGER) '''
        cursor.execute(create_q)
       

        insert_q = '''INSERT INTO colleges (college, private, apps, accept, 
                        enroll, top10perc, top25perc, f_undergrad,
                        p_undergrad, outstate, room_board,
                        books, personal, phd, 
                        terminal, sf_ratio, perc_alumni,
                        expend, grad_rate)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
        

        for row in spreadsheet:
            uni = row['']
            private = row['Private']
            apps = int(row['Apps'])
            accept = int(row['Accept'])
            enroll = int(row['Enroll'])
            top10 = int(row['Top10perc'])
            top25 = int(row['Top25perc'])
            full_under = int(row['F.Undergrad'])
            part_under = int(row['P.Undergrad'])
            outstate = int(row['Outstate'])       
            roomboard = int(row['Room.Board'])
            books = int(row['Books'])
            personal = int(row['Personal'])
            phd = int(row['PhD'])
            terminal = int(row['Terminal'])
            sf_ratio = float(row['S.F.Ratio'])
            alumni = int(row['perc.alumni'])
            expend = int(row['Expend'])
            grad_rate = int(row['Grad.Rate'])

            columns = (uni, private, apps, accept, enroll, top10, 
                        top25, full_under, part_under, outstate 
                        , roomboard, books, personal, phd, terminal  
                        , sf_ratio, alumni, expend, grad_rate) 

            cursor.execute(insert_q, columns)
            
    conn.commit()
    

class Top_10:
    
    '''Top_10.find() finds the top 10 colleges according to what
    variable the user entered
     '''
     
    def __init__(self, column):
        self.column = column

        #self.titles holds all of the graph titles according to variable
        #entered by user
        self.titles = {'apps':'# of Applications Received',
        'accept':'# of Applications Accepted',
        'enroll':'# of Students Enrolled',
        'top10perc':"Percent of New Students from Top 10 Percent of HS Class",
        'top25perc':'Percent of New Students from Top 10 Percent of HS Class',
        'f_undergrad':'# of Full-time Undergrads',
        'p_undergrad':'# of Part-time Undergrads',
        'outstate':'Out-of-State Tuition',
        'room_board':'Cost of Room & Board',
        'books':'Estimated Book Costs',
        'personal':'Estimated Personal Spending',
        'phd':'Percentage of Faculty w/ PhDs',
        'terminal':'Percentage of Faculty w/ Terminal Degree',
        'sf_ratio':'Student/Faculty Ratio',
        'perc_alumni': 'Pct. of Alumni who Donate',
        'expend':'Instructional Expenditure per Student',
        'grad_rate':'Graduation Rate'

        }
    def __repr__(self):
        return(self.column)

    def find(self):
        try:
            if str(self.column).lower() == 'private':
                
                print('\nSystem does not visualize "Private",', end = ' ')
                print('column please provide a different column name\n')

            else:
                select_q = f'''SELECT College, {self.column} FROM colleges 
                        ORDER BY {self.column} DESC
                        LIMIT 10; '''
                top = cursor.execute(select_q).fetchall()

                return(top)
               

        except:
            print('*Column does not exist, enter valid column*')
        

class Visual(Top_10):
    
    '''Visual class inherits Top_10 instance and then visualizes 
    the top 10 colleges into a bar chart
     '''
   
    def display(self):
        try: 
            schools = []
            y_axis = []
            for pair in self.find():
                school = pair[0]
                value = pair[1]
                schools.append(school)
                y_axis.append(value)
    
                y_pos = np.arange(len(schools))
                plt.bar(y_pos, y_axis, align= 'edge', alpha=.9, width = .5, )
                plt.xticks(y_pos, schools, rotation = 40, size = 5)
                plt.ylabel(f'{self.titles[str(self.column)]}')

       
                plt.title(f'Distribution of Top 10 Universities According to {self.titles[str(self.column)]}', size = 10)

            plt.show()
        except:
            pass

    cursor.execute('DROP table colleges;')
    conn.commit()

class Show(Top_10):

    '''Show class also inherits Top_10 instance and serves to print
    out the list of colleges if the user enters show as the 
    2nd argument at the command line'''

    def results(self):
        try:
            if sys.argv[2].lower() == 'show':
                rank = 1
                print('Top 10 Universities According to', end = ' ')
                print(f'{self.titles[str(self.column)]}\n')
           
                for result in self.find():
                    print(str(rank) + '.', result)
                    rank +=1
               
        
            elif sys.argv[2].lower() != 'show':
                print("\nIf you would like the list of results", end = ' ')
                print("enter 'show' as second command line argument\n")
        except:
            pass

def test_top10():
    '''testing top_10 class for bugs '''

    assert Top_10('apps').column != 'apps'
    assert Top_10('enroll').column == 'enroll'
    assert Top_10('apps').find() == [('Rutgers at New Brunswick', 48094), 
    ('Purdue University at West Lafayette', 21804), 
    ('Boston University', 20192), 
    ('University of California at Berkeley', 19873), 
    ('Pennsylvania State Univ. Main Campus', 19315), 
    ('University of Michigan at Ann Arbor', 19152), 
    ('Michigan State University', 18114), 
    ('Indiana University at Bloomington', 16587), 
    ('University of Virginia', 15849), 
    ('Virginia Tech', 15712)]


if __name__ == "__main__":
    
    
    create_db()
    data = Top_10(user_column)
    Visual(data).display()
    Show(data).results()

    
    conn.close()
