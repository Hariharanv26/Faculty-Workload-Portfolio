from django.shortcuts import render, redirect
from .datas import *

admin = False
name = None


def home(request):
    return render(request, 'workload/login.html', {'invalid': False})


def get_details(email):
    monday_classes = []
    tuesday_classes = []
    wednesday_classes = []
    thursday_classes = []
    friday_classes = []
    faculty_schedule = get_faculty_details(email)
    for i in faculty_schedule[1:3]:
        for j in i:
            j = list(j)
            if (j[2] == 'Monday'):
                monday_classes.append(j)
            elif (j[2] == 'Tuesday'):
                tuesday_classes.append(j)
            elif (j[2] == 'Wednesday'):
                wednesday_classes.append(j)
            elif (j[2] == 'Thursday'):
                thursday_classes.append(j)
            elif (j[2] == 'Friday'):
                friday_classes.append(j)
    return [monday_classes, tuesday_classes, wednesday_classes, thursday_classes, friday_classes]


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        global name
        name = authenticate(email, password)
        if name is None:
            return render(request, 'workload/login.html', {'invalid': True})
        else:
            name = name[0]
            global admin
            admin = isAdmin(email)
            details = get_details(email)
            request.session['email'] = email
            context = {'title': 'Time Table', 'monday': details[0], 'tuesday': details[1], 'wednesday': details[2],
                       'thursday': details[3], 'friday': details[4], 'name': name, 'admin': admin}
            request.session['context'] = context
            return render(request, 'workload/time_table.html', context)


def time(request):
    context = request.session.get('context')
    return render(request, 'workload/time_table.html', context)


def academic(request):
    id = request.session.get('email')
    context_lst = faculty_courses(id)
    context = {'title': 'Academic Workload', 'workload': context_lst, 'name': name, 'admin': admin}
    return render(request, 'workload/academic_workload.html', context)


def filterDetails(request):
    id = request.session.get('email')
    if request.method == 'POST':
        session = request.POST.get('selectedOption')
        context_lst = faculty_courses_sort(id, session)
        context = {'title': 'Academic Workload', 'workload': context_lst, 'name': name, 'admin': admin}
        return render(request, 'workload/academic_workload.html', context)


def viewWorkload(request):
    faculty = getAllFaculty()
    context = {'title': 'Facuty_workload', 'Faculty': faculty, 'name': name, 'admin': admin}
    return render(request, 'workload/view_faculty_workload.html', context)


def get_fac_details(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_name')
        session = request.POST.get('session')
        faculty = getAllFaculty()
        context_lst = faculty_courses_sort(faculty_id, session)
        context = {'title': 'Facuty_workload', 'workload': context_lst, 'Faculty': faculty, 'name': name,
                   'admin': admin}
        return render(request, 'workload/view_faculty_workload.html', context)


def update_workload(request):
    context = {'title': 'Update Workload Details', 'addNewCourse': True, 'name': name, 'admin': admin}
    return render(request, 'workload/update_workload.html', context)


def changeUpdateInfo(request):
    if request.method == 'POST':
        info = request.POST.get('detail')
        
        if (info == 'addNewCourse'):
            context = {'title': 'Update Workload Details', 'addNewCourse': True, 'name': name, 'admin': admin}
            return render(request, 'workload/update_workload.html', context)
        
        elif (info == 'removeCourse'):
            course_code, course_name = getAllCourse()
            context = {'title': 'Update Workload Details', 'course_code': course_code, 'course_name': course_name,
                       'removeCourse': True, 'name': name, 'admin': admin}
            return render(request, 'workload/update_workload.html', context)
        
        elif (info == 'assignCourse'):
            faculty_id = getAllFaculty()
            course_code, course_name = getAllCourse()
            context = {'title': 'Update Workload Details', 'faculty_id': faculty_id, 'course_code': course_code,
                       'assignCourse': True, 'name': name, 'admin': admin}
            return render(request, 'workload/update_workload.html', context)
        
        elif (info == 'removeAssignCourse'):
            faculty_id = getAllFaculty()
            course_code, course_name = getAllCourse()
            context = {'title': 'Update Workload Details', 'faculty_id': faculty_id, 'course_code': course_code,
                       'removeAssignCourse': True, 'name': name, 'admin': admin}
            return render(request, 'workload/update_workload.html', context)
        
        else:
            context = {'title': 'Update Workload Details', 'name': name, 'admin': admin}
            return render(request, 'workload/update_workload.html', context)


def add_courses(request):
    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        course_name = request.POST.get('corse_name')
        semester = request.POST.get('semester')
        session = request.POST.get('session')
        hourse_per_week = request.POST.get('hours_per_week')
        types = request.POST.get('type')
        add_course(type=types, semester=semester, hours_per_week=hourse_per_week, course_name=course_name,
                   course_code=course_code, session=session)
        context = {'title': 'Update Workload Details', 'name': name, 'admin': admin}
        return render(request, 'workload/update_workload.html', context)


def remove_courses(request):
    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        course_name = request.POST.get('course_name')
        semester = request.POST.get('semester')
        type = request.POST.get('type')
        remove_course(course_code=course_code, course_name=course_name, semester=semester, type=type)
        context = {'title': 'Update Workload Details', 'name': name, 'admin': admin}
        return render(request, 'workload/update_workload.html', context)


def assign_courses(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        course_code = request.POST.get('course_code')
        day_of_the_week = request.POST.get('day')
        start_hour = request.POST.get('start_hour')
        end_hour = request.POST.get('end_hour')
        session = request.POST.get('session')
        type = request.POST.get('type')
        section = request.POST.get('section')
        assign_courses_tt(course_code=course_code, faculty_id=faculty_id, day_of_the_week=day_of_the_week,
                          hour_of_the_week_start=start_hour, hour_of_the_week_end=end_hour, sessionn=session, type=type,
                          section=section)
        context = {'title': 'Update Workload Details', 'name': name, 'admin': admin}
        return render(request, 'workload/update_workload.html', context)


def remove_assign_course(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        course_code = request.POST.get('course_code')
        type = request.POST.get('type')
        remove_assigned_courses(course_code=course_code, faculty_id=faculty_id, type=type)
        context = {'title': 'Update Workload Details', 'name': name, 'admin': admin}
    return render(request, 'workload/update_workload.html', context)


def department(request):
    id = request.session.get('email')
    lst = department_duties(id)
    context = {'title': 'Department Portfolio', 'duties': lst, 'name': name, 'admin': admin}
    return render(request, 'workload/department.html', context)


def sendOtp(email):
    import random
    otp = int(random.random() * 10000)
    msg = f'''\
    ... From: hariharasudhan2210659@ssn.edu.in
    ... Subject: One Time Password'...
    ...
    ... {otp} is your one time password '''
    import smtplib
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("hariharasudhan2210659@ssn.edu.in", "Pubgroom#123")
    server.sendmail("hariharasudhan2210659@ssn.edu.in", email, msg)
    server.quit()
