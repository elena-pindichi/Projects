from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import pyodbc

ballroom = Flask(__name__)

def connection():
    conn = pyodbc.connect('DRIVER={SQL Server};'
                      'Server=DESKTOP-KDJE0UI\SQLEXPRESS;'
                      'Database=Ballroom_Events;'
                      'Trusted_Connection=yes;')
    return conn

@ballroom.route("/") #For default route
def main():
    return render_template("index.html")

@ballroom.route("/login", methods = ['GET', 'POST']) # For Login route
def login():
    error = ''
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        email = request.form["Email"]
        password = request.form["Password"]
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TblParticipants")
        for row in cursor:
            if row[1] == email and row[2] == password:
                conn.commit()
                conn.close()
                return redirect('/home')

        error = 'Incorrect credentials! Try again!'
    return render_template('login.html', error = error)
            
@ballroom.route("/register", methods = ['GET', 'POST']) # For Registration route
def registration():
    error = None
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        email = request.form["Email"]
        password = request.form["Password"]
        conf_password = request.form["Confirm Password"]
        conn = connection()
        cursor = conn.cursor()
        if password == conf_password:
            cursor.execute("SELECT * FROM TblParticipants")
            for row in cursor:
                if row[1] == email:
                    conn.commit()
                    conn.close()
                    error = 'This account already exists!'
                    return render_template("register.html", error = error)
            cursor.execute("INSERT INTO TblParticipants (Email, Password) VALUES (?, ?)", email, password)
            conn.commit()
            conn.close()
            return redirect('/login')
        else:
            error = 'Wrong Password! Try again!'
    return render_template("register.html", error = error)
 
@ballroom.route("/home", methods = ['GET', 'POST']) #For default route
def home():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Nume, Data, Ora, Locatie, Pret FROM Eveniment")
        data = cursor.fetchall()
        headings = ("Name", "Date", "Time", "Location", "Price") 
        return render_template("home.html", headings = headings, data = data)

@ballroom.route('/delete/<string:id>')
def delete(id):
    conn = connection()
    cursor = conn.cursor()
    
    c = "SELECT EvenimentID FROM Eveniment WHERE Nume = '{}'".format(id)
    cursor.execute(c)
    data1 = cursor.fetchone()
    
    c = "SELECT ParticipantID FROM ParticipantEveniment WHERE EvenimentID = '{}'".format(data1[0])
    cursor.execute(c)
    data = cursor.fetchone()
    if data != None:
        c = "delete from ParticipantEveniment where EvenimentID = '{}'".format(data1[0])
        cursor.execute(c)
        
        for participant in data:
            c = "select ParticipantID from ParticipantEveniment where ParticipantID = '{}'".format(participant)
            cursor.execute(c)
            find = cursor.fetchall()
            if find == None:
                c = "DELETE FROM Participant WHERE ParticipantID = '{}'".format(participant)
                cursor.execute(c)
    
    c = "select EvenimentID from Eveniment where Nume = '{}'".format(id)
    cursor.execute(c)
    data = cursor.fetchone()
    
    c = "DELETE FROM DepartamentEveniment WHERE EvenimentID = '{}'".format(data1[0])
    cursor.execute(c)
    
    cursor.execute("DELETE FROM Eveniment WHERE Nume = ?", id)
    conn.commit()
    conn.close()
    return redirect('/home')

@ballroom.route('/update/<string:id>', methods = ['GET', 'POST'])
def update(id):
    error = None
    if request.method == 'POST':
        partnerid = request.form["PartenerID"]
        name = request.form["Nume"]
        date = request.form["Data"]
        time = request.form["Ora"]
        location = request.form["Locatie"]
        price = request.form["Pret"]
        
        conn = connection()
        cursor = conn.cursor()
        
        c = "SELECT EvenimentID FROM Eveniment WHERE Nume = '{}'".format(id)
        cursor.execute(c)
        eventid = cursor.fetchone()
        
        c = "SELECT PartenerID from Partener WHERE Nume = ?"
        cursor.execute(c,(partnerid,))
        t = cursor.fetchone()

        if t == None:
            error = 'Partner does not exist!'
            c = "SELECT Partener.Nume, Eveniment.Nume, Eveniment.Data, Eveniment.Ora, Eveniment.Locatie, Eveniment.Pret FROM Eveniment inner join Partener on Partener.PartenerID = Eveniment.PartenerID where Eveniment.Nume = ? "
            cursor.execute(c,(id,))
            data =cursor.fetchone()
            return render_template("update_event.html", partnerid = data[0],name = data[1],date = data[2],time = data[3],location = data[4],price = data[5], error = error)
        else:
            c = "UPDATE Eveniment SET PartenerID = '{}', Nume = '{}', Data = '{}', Ora = '{}', Locatie = '{}', Pret = '{}' WHERE EvenimentID = '{}'".format(t[0], name, date, time, location, price, eventid[0])
            cursor.execute(c)
            conn.commit()
            conn.close()
            return redirect('/home')
    if request.method == 'GET':
        conn = connection()
        cursor = conn.cursor()

        c = "SELECT Partener.Nume, Eveniment.Nume, Eveniment.Data, Eveniment.Ora, Eveniment.Locatie, Eveniment.Pret FROM Eveniment inner join Partener on Partener.PartenerID = Eveniment.PartenerID where Eveniment.Nume = ? "
        cursor.execute(c,(id,))
        data =cursor.fetchone()
        return render_template("update_event.html", partnerid = data[0],name = data[1],date = data[2],time = data[3],location = data[4],price = data[5])

@ballroom.route("/add_event", methods = ['GET', 'POST']) #For tickets route
def add_event():
    error = None
    if request.method == 'GET':
        return render_template("add_event.html")
    if request.method == 'POST':
        name_dep = request.form["NumeDepartament"]
        partner = request.form["PartenerID"]
        name = request.form["Nume"]
        dates = request.form["Data"]
        time = request.form["Ora"]
        location = request.form["Locatie"]
        price = request.form["Pret"]
        conn = connection()
        cursor = conn.cursor()
        
        c = "SELECT PartenerID from Partener where Nume = '{}'".format(partner)
        cursor.execute(c)
        t = cursor.fetchone()
        if t == None:
            error = 'Partner does not exist!'
            return render_template("add_event.html", error = error)
        else:   
            cursor.execute("SELECT * FROM Eveniment")
            for row in cursor:
                if row[2] == name:
                    conn.commit()
                    conn.close()
                    error = 'This event already exists!'
                    return render_template("add_event.html", error = error)
            cursor.execute("INSERT INTO Eveniment (PartenerID, Nume, Data, Ora, Locatie, Pret) VALUES (?, ?, ?, ?, ?, ?)", t[0], name, dates, time, location, price)
            
            c = "select D.DepartamentID from Departament D where D.NumeDepartament = '{}'".format(name_dep)
            cursor.execute(c)
            data1 = cursor.fetchone()
            
            c = "select EvenimentID from Eveniment where Nume = '{}'".format(name)
            cursor.execute(c)
            data2 = cursor.fetchone()
            
            cursor.execute("insert into DepartamentEveniment (DepartamentID, EvenimentID) values(?, ?)", data1[0], data2[0])
            
            conn.commit()
            conn.close()
            return redirect('/home')
    else:
        error = 'Wrong values! The values you introduced, do not match the element types!'
    return render_template("add_event.html", error = error)
    
@ballroom.route("/tickets/<string:id>", methods = ['GET', 'POST']) #For tickets route
def tickets(id):
    error = None
    if request.method == 'GET':
        return render_template("tickets.html")
    if request.method == 'POST':
        surname = request.form["Nume"]
        firstname = request.form["Prenume"]
        cnp = request.form["CNP"]
        sex = request.form["Sex"]
        email = request.form["Email"]
        conn = connection()
        cursor = conn.cursor()
        
        c = "SELECT Email FROM TblParticipants WHERE Email = '{}'". format(email)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        if t == ():
            error = 'This account does not exist!'
            return render_template("tickets.html", error = error)
        else:
            c = "select ParticipantID from Participant where Nume = '{}'and Prenume = '{}' and CNP = '{}' and Email = '{}'".format(surname, firstname, cnp, email)
            cursor.execute(c)
            data = cursor.fetchone()
            
            if data == None: 
                c = "select CNP from Participant where Email = '{}' and CNP = '{}'".format(email, cnp)
                cursor.execute(c)
                find = cursor.fetchall()
                if find != []:
                    error = 'Incorrect credentials!'
                    return render_template("tickets.html", error = error)
                else:
                    cursor.execute("INSERT INTO Participant (Nume, Prenume, CNP, Sex, Email) VALUES (?, ?, ?, ?, ?)", (surname, firstname, cnp, sex, email))
            
                    c = "SELECT ParticipantID FROM Participant WHERE Nume = '{}' and Prenume = '{}' and Email = '{}'".format(surname, firstname, email)
                    cursor.execute(c)
                    data1 = cursor.fetchone()
            
                    c = "SELECT EvenimentID from Eveniment WHERE Nume = '{}'".format(id)
                    cursor.execute(c)
                    data2 = cursor.fetchone()
            
                    c = "INSERT INTO ParticipantEveniment (ParticipantID, EvenimentID) VALUES ('{}', '{}')".format(data1[0], data2[0])
                    cursor.execute(c)
            
                    conn.commit()
                    conn.close()
                    return redirect('/home')
            else:                
                c = "SELECT ParticipantID FROM Participant WHERE Nume = '{}' and Prenume = '{}' and Email = '{}'".format(surname, firstname, email)
                cursor.execute(c)
                data1 = cursor.fetchone()
            
                c = "SELECT EvenimentID from Eveniment WHERE Nume = '{}'".format(id)
                cursor.execute(c)
                data2 = cursor.fetchone()
            
                c = "INSERT INTO ParticipantEveniment (ParticipantID, EvenimentID) VALUES ('{}', '{}')".format(data1[0], data2[0])
                cursor.execute(c)
            
                conn.commit()
                conn.close()
                return redirect('/home')
                
@ballroom.route("/delete-participant/<string:id>", methods = ['GET', 'POST'])
def delete_participant(id):
    error = None
    if request.method == 'GET':
        return render_template("delete-participant.html")
    if request.method == 'POST':
        surname = request.form["Nume"]
        firstname = request.form["Prenume"]
        email = request.form["Email"]
        conn = connection()
        cursor = conn.cursor()
        c = "SELECT * FROM Participant P join TblParticipants TP on P.Email = TP.Email WHERE P.Email = '{}' and P.Nume = '{}' and P.Prenume = '{}'".format(email, surname, firstname)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        
        if t == ():
            error = 'No ticket acquired!'
            return render_template("delete-participant.html", error = error)
        else:
            c = "SELECT ParticipantID FROM Participant P WHERE P.Nume = '{}' and P.Prenume = '{}'and P.Email = '{}'".format(surname, firstname, email)
            cursor.execute(c)
            data1 = cursor.fetchone()
            
            c = "select EvenimentID from Eveniment where Nume = '{}'".format(id)
            cursor.execute(c)
            data2 = cursor.fetchone()
            
            c = "DELETE FROM ParticipantEveniment WHERE ParticipantID = '{}' and EvenimentID = '{}'".format(data1[0], data2[0])
            cursor.execute(c)
            
            c = "select ParticipantID from ParticipantEveniment where ParticipantID = '{}'".format(data1[0])
            cursor.execute(c)
            data = cursor.fetchall()
            
            if data == []:
                c = "DELETE FROM Participant WHERE ParticipantID = '{}' ".format(data1[0])
                cursor.execute(c)
                conn.commit()
                conn.close()
                return redirect('/home')
            else:
                conn.commit()
                conn.close()
                return redirect('/home')
   
@ballroom.route("/partners", methods = ['GET', 'POST']) #For partners route
def partners():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Nume, Buget FROM Partener")
        data = cursor.fetchall()
        headings = ("Name", "Budget") 
        return render_template("partners.html", headings = headings, data = data)

@ballroom.route('/update-partner/<string:id>', methods = ['GET', 'POST'])
def update_partner(id):
    error = None
    if request.method == 'POST':
        name = request.form["Nume"]
        budget = request.form["Buget"]
        
        conn = connection()
        cursor = conn.cursor()
        
        c = "SELECT PartenerID FROM Partener WHERE Nume = '{}'".format(id)
        cursor.execute(c)
        partnerid = cursor.fetchone()

        if partnerid == None:
            error = 'Partner does not exist!'
            c = "SELECT Nume, Buget FROM Partener where Nume = ? "
            cursor.execute(c,(id,))
            data =cursor.fetchone()
            return render_template("update-partner.html", name = data[0], budget = data[1], error = error)
        else:
            c = "UPDATE Partener SET Nume = '{}', Buget = '{}' WHERE PartenerID = '{}'".format(name, budget, partnerid[0])
            cursor.execute(c)
            conn.commit()
            conn.close()
            return redirect('/partners')
    if request.method == 'GET':
        conn = connection()
        cursor = conn.cursor()
        c = "SELECT Nume, Buget FROM Partener where Nume = ? "
        cursor.execute(c,(id,))
        data =cursor.fetchone()
        return render_template("update-partner.html", name = data[0], budget = data[1])

@ballroom.route("/participants", methods = ['GET', 'POST']) #For participants route
def participants():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT P.Nume, P.Prenume, P.CNP, P.Email, E.Nume FROM Participant P join ParticipantEveniment PE on Pe.ParticipantID = P.ParticipantID join Eveniment E on PE.EvenimentID = E.EvenimentID order by P.Nume ASC")
        data = cursor.fetchall()
        headings = ("Surname", "Firstname", "CNP", "Email", "Event") 
        return render_template("participants.html", headings = headings, data = data)

@ballroom.route("/type_event", methods = ['GET', 'POST'])
def type_event():
    error = None
    if request.method == 'GET':
        return render_template("type_event.html")
    if request.method == 'POST':
        name = request.form["Nume"]
        conn = connection()
        cursor = conn.cursor()
        
        c = "SELECT P.Nume, P.Prenume, P.CNP, P.Email, E.Nume FROM Participant P join ParticipantEveniment PE on P.ParticipantID = PE.ParticipantID join Eveniment E on PE.EvenimentID = E.EvenimentID WHERE E.Nume = '{}' ORDER BY P.Nume ASC".format(name)
        cursor.execute(c)
        data = cursor.fetchall()
        if data == None:
            error = 'There are no participants at this event!'
            return render_template("type_event.html", error = error)
        else:
            headings = ("Surname", "Firstname", "CNP", "Email", "Event") 
            conn.commit()
            conn.close()
            return render_template("event_participants.html", headings = headings, data = data)

@ballroom.route("/organizatori")
def organizator_page():
    return render_template("organizatori.html")

@ballroom.route("/event-angajat", methods = ['GET', 'POST'])
def employee_type_event():
    error = None
    if request.method == 'GET':
        return render_template("event-angajat.html")
    if request.method == 'POST':
        name = request.form["Nume"] 
        conn = connection()
        cursor = conn.cursor()
        
        
        c = "select A.Nume, A.Prenume from Angajati A where A.DepartamentID in (select D.DepartamentID from Departament D join DepartamentEveniment DE on D.DepartamentID = DE.DepartamentID join Eveniment E on E.EvenimentID = DE.EvenimentID where E.Nume = '{}' group by D.DepartamentID)".format(name)
        cursor.execute(c)
        data = cursor.fetchall()
        if data == None:
            error = 'There are no organizers at this event!'
            return render_template("event-angajat.html", error = error)
        else:
            headings = ("Surname", "Firstname") 
            conn.commit()
            conn.close()
            return render_template("here-organizator.html", headings = headings, data = data)

@ballroom.route("/add-department/<string:id>", methods = ['GET', 'POST'])
def add_department(id):
    error = None
    if request.method == 'GET':
        return render_template("add-department.html")
    if request.method == 'POST':
        name = request.form["Nume"]
        conn = connection()
        cursor = conn.cursor()
        
        c = "select DepartamentID from Departament where NumeDepartament = '{}'".format(name)
        cursor.execute(c)
        data = cursor.fetchone()
        if data == None:
            error = 'There is no such department!'
            return render_template("add-department.html", error = error)
        else:
            c = "select EvenimentID from Eveniment where Nume = '{}'".format(id)
            cursor.execute(c)
            data1 = cursor.fetchone()
            
            cursor.execute("insert into DepartamentEveniment (DepartamentID, EvenimentID) values (?, ?)", data[0], data1[0])
            
            conn.commit()
            conn.close()
            return redirect('/home')

@ballroom.route("/free-department", methods = ['GET', 'POST'])
def free_department():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("select D.NumeDepartament from Departament D where D.DepartamentID not in (select distinct D2.DepartamentID from Departament D2, DepartamentEveniment DE where D2.DepartamentID = DE.DepartamentID)")
        data = cursor.fetchall()
        return render_template("free-department.html", data = data)

@ballroom.route("/old-employee", methods = ['GET', 'POST'])
def old_employees():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("select A.Nume, A.Prenume, A.DataAngajarii from Angajati A, Departament D, DepartamentEveniment DE where A.DepartamentID = D.DepartamentID and year(A.DataAngajarii)<=2010 and D.DepartamentID = DE.DepartamentID and DE.EvenimentID in (select DE2.EvenimentID from DepartamentEveniment DE2, Angajati A2, Departament D2 where D2.ManagerID = A2.AngajatID and A2.DepartamentID = D2.DepartamentID and D2.DepartamentID = DE2.DepartamentID) group by A.Nume, A.Prenume, A.DepartamentID, A.AngajatID, A.DataAngajarii")
        data = cursor.fetchall()
        headings = ("Surname", "Firstname", "Employment Date")
        return render_template("old-employee.html", headings = headings, data = data)

@ballroom.route("/employee-salary", methods = ['GET', 'POST'])
def employee_salary():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("select A.Nume, A.Prenume, A.Salariu, D.NumeDepartament from Angajati A join Departament D on D.DepartamentID = A.DepartamentID where A.AngajatID in (select AngajatID from Angajati where Salariu >= 2000) group by A.Nume, A.Prenume, A.Salariu, D.NumeDepartament order by A.Nume")
        data = cursor.fetchall()
        headings = ("Surname", "Firstname", "Salary", "Department")
        return render_template("employee-salary.html", headings = headings, data = data)

@ballroom.route("/free-event", methods = ['GET', 'POST'])
def free_events():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("select E.Nume from Eveniment E left join ParticipantEveniment PE on E.EvenimentID = PE.EvenimentID group by E.Nume having count(PE.ParticipantID) = 0")
        data = cursor.fetchall()
        return render_template("free-event.html", data = data)

@ballroom.route("/event-budget-type", methods = ['GET', 'POST'])
def type_event_budget():
    error = None
    if request.method == 'GET':
        return render_template("event-budget-type.html")
    if request.method == 'POST':
        name = request.form["Nume"]
        conn = connection()
        cursor = conn.cursor()
        
        c = "select P.Nume, P.Buget from Partener P inner join Eveniment E on P.PartenerID = E.PartenerID where E.Nume = '{}' and P.Buget >= all(select avg(Buget) from Partener)".format(name)
        cursor.execute(c)
        data = cursor.fetchall()
        if data == []:
            error = 'There are no partners at this event with budget over average!'
            return render_template("event-budget-type.html", error = error)
        else:
            headings = ("Name", "Budget") 
            conn.commit()
            conn.close()
            return render_template("event-budget-partner.html", headings = headings, data = data)

@ballroom.route("/number-events", methods = ['GET', 'POST'])
def count_events():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("select P.Nume, P.Buget, count(E.EvenimentID) from Partener P left join Eveniment E on E.PartenerID = P.PartenerID group by P.Nume, P.Buget order by P.Buget DESC")
        data = cursor.fetchall()
        headings = ("Name", "Budget", "Events Number") 
        return render_template("number-events.html", headings = headings, data = data)

@ballroom.route("/event-organizator", methods = ['GET', 'POST'])
def event_organizator():
    error = None
    if request.method == 'GET':
        return render_template("event-organizator.html")
    if request.method == 'POST':
        name = request.form["Nume"]
        conn = connection()
        cursor = conn.cursor()
        
        c = "select P.Nume, D.NumeDepartament from Partener P join Eveniment E on P.PartenerID = E.PartenerID join DepartamentEveniment DE on DE.EvenimentID = E.EvenimentID join Departament D on D.DepartamentID = DE.DepartamentID where E.Nume = 'SpaceShip'"
        cursor.execute(c)
        data = cursor.fetchall()
        if data == None:
            error = 'There is no such event!'
            return render_template("event-organizator.html", error = error)
        else:
            headings = ("Partner", "Department") 
            conn.commit()
            conn.close()
            return render_template("partner-dep.html", headings = headings, data = data)


if(__name__ == "__main__"):
    ballroom.run(debug=True)
