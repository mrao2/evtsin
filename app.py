from flask import Flask, request, redirect, render_template, send_file, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://eventsignin:pass@localhost:3306/eventsignin'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#db.Model.metadata.reflect(db.engine)

class member_info(db.Model):

    # __table__ = db.Model.metadata.tables['member_info']
     Row_NumberString = db.Column(db.String(5))
     Row_Number = db.Column(db.Integer, primary_key=True)
     Membership_Status = db.Column(db.String(80))
     Payment_method = db.Column(db.String(80))
     Renewed_On = db.Column(db.String(80))
     Membership_Type = db.Column(db.String(80))
     Fees = db.Column(db.String(80))
     Newer_Member = db.Column(db.String(80))
     Phone_Primary = db.Column(db.String(80))
     Phone_Secondary = db.Column(db.String(80))
     Full_Name = db.Column(db.String(80))
     Last_Name = db.Column(db.String(80))
     Children_Name = db.Column(db.String(80))
     Children_Age_Gender = db.Column(db.String(80))
     Address = db.Column(db.String(80))
     City = db.Column(db.String(80))
     State = db.Column(db.String(3))
     ZipCode = db.Column(db.String(80))
     EMail_Primary = db.Column(db.String(80))
     EMail_Secondary = db.Column(db.String(80))
     AdultTicket = db.Column(db.String(80))
     KidTicket = db.Column(db.String(80))
     TicketPayMethod = db.Column(db.String(80))
     Total = db.Column(db.String(80))
     Comment = db.Column(db.String(80))
     Kannada_Shale = db.Column(db.String(80))
     Food_Bank = db.Column(db.String(80))
     Kid_Smart = db.Column(db.String(80))
     LastUpdated = db.Column(db.String(80))
     Membership_Status_2015_16 = db.Column(db.String(80))



     def __init__(self, EMail_Primary, Full_Name, Last_Name, Phone_Primary, Membership_Status, Comment, Membership_Type, Newer_Member):
         self.EMail_Primary = EMail_Primary
         self.Full_Name = Full_Name
         self.Last_Name = Last_Name
         self.Phone_Primary = Phone_Primary
         self.Membership_Status = Membership_Status
         self.Comment = Comment
         self.Membership_Type = Membership_Type
         self.Newer_Member = Newer_Member

@app.route('/', methods=['POST', 'GET'])
def index():
    userlist =  member_info.query.all()
    return render_template('member_list.html',userlist=userlist)

@app.route('/member', methods=['GET', 'POST'])
def member():

    if request.args.get('id'):
        print("test2")
        info = member_info.query.filter_by(Row_Number=request.args.get('id')).first()
        print("test3")
    elif request.args.get('user'):
        print("test4")
        comment = request.form['comment']
        info = member_info.query.filter_by(Row_Number=request.args.get('user')).first()
        info.Comment = comment
        db.session.commit()

    return render_template('singlemember.html', info=info)

@app.route('/new_member', methods=['POST', 'GET'])
def new_member():
    if request.method == 'POST':
        email = request.form['email']
        name= request.form['fullname']
        lname = request.form['lastname']
        phone = request.form['phnumber']
        memstat = request.form['memstat']
        comment = request.form['comment']
        memtype = request.form['memtype']

        new_person = member_info(EMail_Primary=email,Full_Name=name,Last_Name=lname,Phone_Primary=phone,Membership_Status=memstat, Comment=comment, Membership_Type=memtype)
        db.session.add(new_person)
        db.session.commit()
        return redirect('/member?id=' + str(new_person.Row_Number))

    return render_template('new_member.html',title="Member Sign Up")

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_entry = request.form['query']
    #info = member_info.member_info()
    #lastname = member_info.query.filter(literal(search_string).contains(Full_Name=request.form['query']))
    sql = text("SELECT * FROM member_info WHERE Full_Name LIKE '%" + search_entry + "%' OR Last_Name LIKE '%" + search_entry + "%'")
    lastname = db.engine.execute(sql)
    print(lastname)
    return render_template('result.html', lastname=lastname)

if __name__ == '__main__':
    app.run()
