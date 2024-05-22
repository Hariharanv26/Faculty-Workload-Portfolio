import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="hari",
  password="1234",
  database="workload"
)

print(mydb.is_connected())

c = mydb.cursor()

def authenticate(email,password):
    q = f"SELECT f_name FROM Users WHERE faculty_id = %s AND password = %s"
    c.execute(q,(email,password))
    name = c.fetchone()
    return name

def isAdmin(email):
    a = f"SELECT entity from users where faculty_id = '{email}'"
    c.execute(a)
    admin = c.fetchone()
    if admin[0] == 'admin':
        return True
    return False


def get_faculty_details(faculty_id):
    lst = [[None, 0, 0, 0]]
    
    q1 = f"SELECT f_name FROM Users WHERE faculty_id = '{faculty_id}'"
    c.execute(q1)
    name = c.fetchone()
    
    if name is None:
        return None
    
    lst[0][0] = name[0]

    q2 = f"SELECT t.course_code, tc.course_name, t.day_of_the_week, t.hour_of_the_week, t.section, t.handled_duration FROM Theory t JOIN TheoryCourse tc ON t.course_code = tc.course_code WHERE t.faculty_id = '{faculty_id}' and t.sessionn = 'feb-jul'"
    c.execute(q2)
    theory_courses = c.fetchall()
    lst[0][1] = len(theory_courses)
    lst.append(theory_courses)

    q3 = f"SELECT p.course_code, pc.course_name, p.day_of_the_week, p.hour_of_the_week_start, p.hour_of_the_week_end, p.section, p.handled_duration FROM Practical p JOIN PracticalCourse pc ON p.course_code = pc.course_code WHERE p.faculty_id = '{faculty_id}' and p.sessionn='feb-jul'"
    c.execute(q3)
    practical_courses = c.fetchall()
    lst[0][2] = len(practical_courses)
    lst.append(practical_courses)

    q4 = f"SELECT p.course_code, p.course_name, p1.day_of_the_week, p1.hour_of_the_week_start, p1.hour_of_the_week_end, p1.section, p1.handled_duration FROM project p1 join projectcourse p ON p.course_code = p1.course_code WHERE p1.faculty_id = '{faculty_id}' and p.sessionn= 'feb-jul'"
    c.execute(q4)
    projects = c.fetchall()
    lst[0][3] = len(projects)
    lst.append(projects)

    return lst


def faculty_courses(faculty_id):
    lst=[]
    q1=f"SELECT DISTINCT(theorycourse.course_name) FROM theorycourse JOIN Theory ON theorycourse.course_code=Theory.course_code WHERE Theory.faculty_id='{faculty_id}' and Theory.sessionn = 'feb-jul'"
    c.execute(q1)
    out=c.fetchall()
    tup=()
    for i in range(len(out)):
        tup+=(out[i][0],)
    lst.append(tup)

    q2=f"SELECT DISTINCT(pc.course_name) FROM project p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}' and p.sessionn = 'feb-jul' UNION SELECT DISTINCT(pc.course_name) FROM practical p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}' and p.sessionn='feb-jul'"
    c.execute(q2)
    out=c.fetchall()
    tup=()
    for i in range(len(out)):
        tup+=(out[i][0],)
    lst.append(tup)
    return lst

def faculty_courses_sort(faculty_id,session):
    if session =='All_Session':
        lst=[]
        q1=f"SELECT DISTINCT(theorycourse.course_name) FROM theorycourse JOIN Theory ON theorycourse.course_code=Theory.course_code WHERE Theory.faculty_id='{faculty_id}'"
        c.execute(q1)
        out=c.fetchall()
        tup=()
        for i in range(len(out)):
            tup+=(out[i][0],)
        lst.append(tup)

        q2=f"SELECT DISTINCT(pc.course_name) FROM project p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}'UNION SELECT DISTINCT(pc.course_name) FROM practical p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}'"
        c.execute(q2)
        out=c.fetchall()
        tup=()
        for i in range(len(out)):
            tup+=(out[i][0],)
        lst.append(tup)
        return lst
    
    
    lst=[]
    q1=f"SELECT DISTINCT(theorycourse.course_name) FROM theorycourse JOIN Theory ON theorycourse.course_code=Theory.course_code WHERE Theory.faculty_id='{faculty_id}' AND Theory.sessionn = '{session}'"
    c.execute(q1)
    out=c.fetchall()
    tup=()
    for i in range(len(out)):
        tup+=(out[i][0],)
    lst.append(tup)

    q2=f"SELECT DISTINCT(pc.course_name) FROM project p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}' AND p.sessionn = '{session}' UNION SELECT DISTINCT(pc.course_name) FROM practical p JOIN practicalcourse pc ON pc.course_code=p.course_code WHERE p.faculty_id='{faculty_id}' AND p.sessionn = '{session}'"
    c.execute(q2)
    out=c.fetchall()
    tup=()
    for i in range(len(out)):
        tup+=(out[i][0],)
    lst.append(tup)
    return lst

def getAllFaculty():
    lst = []
    q1 = f"select faculty_id, f_name from users"
    c.execute(q1)
    output = c.fetchall()
    lst.extend(output)
    return lst

def getAllCourse():
    course_code = []
    course_name = []
    q1 = f"select course_code from theoryCourse"
    c.execute(q1)
    course_code.extend(c.fetchall())

    q2 = f"select course_code from PracticalCourse"
    c.execute(q2)
    course_code.extend(c.fetchall())

    q3 = f"select course_name from theoryCourse"
    c.execute(q3)
    course_name.extend(c.fetchall())

    q4 = f"select course_name from PracticalCourse"
    c.execute(q4)
    course_name.extend(c.fetchall())
    return course_code,course_name

def add_course(type,course_code,course_name,semester,session,hours_per_week=3):
    if type=="Theory":
        q1=f"INSERT INTO TheoryCourse VALUES ('{course_code}','{course_name}',{int(hours_per_week)},{int(semester)},'{session}')"
        c.execute(q1)
        c.execute('commit')
    if type=="Practical" or type=="Project":
        q2=f"INSERT INTO PRACTICALCOURSE VALUES ('{course_code}','{course_name}',{int(hours_per_week)},{int(semester)},'{session}')"
        c.execute(q2)
        c.execute('commit')
  
def remove_course(course_code,course_name,semester,type):
    if type == 'Theory':
        q1=f"SELECT * FROM THEORYCOURSE WHERE COURSE_CODE='{course_code}'"
        c.execute(q1)
        out=c.fetchall()
        if len(out)!=0:
            q2=f"DELETE FROM THEORYCOURSE WHERE COURSE_CODE='{course_code}' and COURSE_NAME = '{course_name}' and SEMESTER = '{int(semester)}'"
            c.execute(q2)
            c.execute('commit')

    if type == "Practical" or type=="Project":
        q1=f"SELECT * FROM PRACTICALCOURSE WHERE COURSE_CODE='{course_code}'"
        c.execute(q1)
        out=c.fetchall()
        if len(out)!=0:
            q2=f"DELETE FROM PRACTICALCOURSE WHERE COURSE_CODE='{course_code}' and COURSE_NAME = '{course_name}' and SEMESTER = '{int(semester)}'"
            c.execute(q2)
            c.execute('commit')

def assign_courses_tt(type,faculty_id,course_code,day_of_the_week,section,sessionn,hour_of_the_week_start,hour_of_the_week_end=None,handled_duration=datetime.datetime.now().year):
    if type=="Theory":
        q1=f"INSERT INTO THEORY VALUES ('{faculty_id}','{course_code}','{day_of_the_week}','{hour_of_the_week_start}','{section}','{handled_duration}','{sessionn}')"
        c.execute(q1)
        c.execute('commit')
    if type=="Practical":
        q2=f"INSERT INTO PRACTICAL VALUES ('{faculty_id}','{course_code}','{day_of_the_week}','{hour_of_the_week_start}','{hour_of_the_week_end}','{section}','{handled_duration}','{sessionn}')"
        c.execute(q2)
        c.execute('commit')
    if type=="Project":
        q3=f"INSERT INTO PROJECT VALUES ('{faculty_id}','{course_code}','{day_of_the_week}','{hour_of_the_week_start}','{hour_of_the_week_end}','{section}','{handled_duration}','{sessionn}')"
        c.execute(q3)
        c.execute('commit')

def remove_assigned_courses(type,faculty_id,course_code):
    if type=="Theory":
        q1=f"DELETE FROM THEORY WHERE COURSE_CODE='{course_code}' AND faculty_id='{faculty_id}'"
    elif type=="Practical":
        q1=f"DELETE FROM PRACTICAL WHERE COURSE_CODE='{course_code}' AND faculty_id='{faculty_id}'"
    elif type=="Project":
        q1=f"DELETE FROM PROJECT WHERE COURSE_CODE='{course_code}' AND faculty_id='{faculty_id}'"
    c.execute(q1)
    c.execute('commit')  

