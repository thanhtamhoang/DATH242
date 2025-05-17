from flask import Flask, render_template, request, session, redirect, url_for , flash, jsonify
from db_utils import get_all_data, get_courses, search_course_by_code, search_registered_course_by_student_code, add_registered, check_login, get_all_subjects, delete_registered, search_all_course_by_code, get_course_through_faculty_name, search_teaching_code_by_teacher_id  # Hàm xử lý DB
from aaodb import get_all_teacher, add_new_teacher, view_teacher_info, delete_old_teacher, view_course_info, add_new_course, get_all_teachers, add_class_to_db, get_class_of_teacher, toggle_class, get_all_faculty
from mysql.connector import Error
from exception import DuplicateRegistrationError, ScheduleConflictError, AddTeacherUnsuccessfully, StudentRegisterCourseDuplicate 

app = Flask(__name__)
app.secret_key = "your_secret_key_here_123456789"
# Route trang chủ
days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
time_slots  = ["8:00:00-9:50:00", "10:00:00-11:50:00", "13:00:00-14:50:00", "15:00:00-16:50:00", "17:00:00-18:50:00"]
@app.route("/home/login")
def loginpage():
    return render_template("zguess/login.html")
@app.route("/")
def home():
    return render_template("zguess/home.html")
@app.route("/aao/home")
def aao_home():
    
    return render_template("AAO/AAOHome.html")

@app.route("/aao/TeacherManagement")
def teacher_management():
    
    exist_already = request.args.get("exist_already", type=int) == 1
    teachers = get_all_teacher()
    return render_template("AAO/TeacherManagement.html", teachers = teachers, exist_already = exist_already)
    
@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    exist_flag = False
    name = request.form.get("name")
    department = request.form.get("department")
    print(name, department)
    if name and department:
        try:
            add_new_teacher(name, department) 
        except AddTeacherUnsuccessfully:
            exist_flag = True
            return redirect(url_for("teacher_management", exist_already=int(exist_flag)))
            
    return redirect(url_for("teacher_management",  exist_already=1 if exist_flag else 0))

# @app.route("/view_teacher", methods = ["POST"])
# def view_teacher():
#     teacherID = request.form.get("teacher_id")
#     teacher = view_teacher(teacherID)
#     return render_template("AAO/TeacherManagement", teacher = teacher, teacher_id = teacherID)

@app.route("/teacher/<int:teacher_id>")
def view_teacher(teacher_id):
    # truy vấn DB lấy chi tiết giáo viên
    print(teacher_id)
    teacher = view_teacher_info(teacher_id)
    classes  = get_class_of_teacher(teacher_id)
    return render_template("AAO/TeacherManagement.html",
                           teacher=teacher,
                           teacher_id=teacher_id,
                           classes=classes)
    
@app.route('/teacher_classes/<teacher_id>')
def teacher_classes(teacher_id):
    # Truy vấn DB: lấy class.ClassID, subject.Name, class.SemID
    return get_class_of_teacher(teacher_id)

@app.route("/aao/delete_teacher",methods=["POST"])
def delete_teacher():
    teacherID = request.form.get("teacher_id")
    print(teacherID,"hi")
    delete_old_teacher(int(teacherID))
    teachers = get_all_teacher()
    return redirect(url_for("teacher_management"))

@app.route("/aao/CourseManagement")
def course_management():
    faculty = request.args.get("faculty")
    if faculty:
        courses = get_course_through_faculty_name(faculty) #return course th
    else:
        courses = get_courses()
    Faculty = get_all_faculty()
    return render_template("AAO/CourseManagement.html", courses=courses, Faculty = Faculty)

@app.route("/aao/search_course_through_faculty_aao_function", methods = ["POST"])
def search_course_through_faculty_aao_function():
    faculty = request.form.get("faculty_name")
    return redirect(url_for("course_management", faculty = faculty))

@app.route("/aao/view_course", methods = ["GET"])
def view_course():
    courseID = request.args.get("course_id")
    class_info, time_info, teacher_name, course_name = search_all_course_by_code(courseID) 
    print( class_info, time_info, teacher_name, course_name)
    courses = get_courses()
    course = list(zip(class_info, time_info, teacher_name))
    teachers = get_all_teachers()
    Faculty = get_all_faculty()
    return render_template("AAO/CourseManagement.html", course_id = courseID, course=course, courses = courses, teachers = teachers, course_name = course_name, Faculty = Faculty)
    
@app.route("/aao/add_course", methods = ["POST"])
def add_course():
    Name = request.form.get("course_name")
    courseID = request.form.get("course_id")
    Credits = request.form.get("course_credits")
    RequiredCredits = request.form.get("required_credits")
    course = add_new_course(courseID, Name, Credits, RequiredCredits)
    courses = get_courses()
    return render_template("AAO/CourseManagement.html", course=course, courses = courses)

@app.route("/aao/add_class", methods = ["POST"])
def add_class():
    course_id = request.form.get("course_id")
    class_id = request.form.get("class_id")
    teacher_name = request.form.get("teacher_id")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    day = request.form.get("day")
    room = request.form.get("room")
    courses = get_courses()
    AddSuccessfully = False
    ExistAlready = False
    try:
        if add_class_to_db(course_id, class_id, teacher_name, start_time, end_time, day, room):
            AddSuccessfully = True
        else:
            ExistAlready = True
    except Error as e:
        ExistAlready = True
    Faculty = get_all_faculty()
    return render_template("AAO/CourseManagement.html", Faculty = Faculty, courses = courses, AddSuccessfully = AddSuccessfully,ExistAlready = ExistAlready)

@app.route('/toggle_class_status', methods=['POST'])
def toggle_class_status():
    class_id = request.form['class_id']
    course_id = request.form['course_id']
    sem_id   = request.form['sem_id']
    new_status = toggle_class(class_id, course_id, sem_id)    
    flash(f"Class {class_id} is now {new_status}.", "success")
    return redirect(request.referrer or url_for('course_management'))



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["username"]  # <-- đây thực ra đang là email
        password = request.form["password"]
        role, user_id = check_login(email, password)
        print(role, user_id)
        if role:
            session["email"] = email
            session["role"] = role
            if role == "Student":
                session["student_id"] = user_id
                return redirect(url_for("student_register"))
            elif role == "Teacher":
                session["teacher_id"] = user_id
                return redirect(url_for("teacher_home"))
            elif role == "AAO":
                return redirect(url_for("aao_home"))
        else:
            return render_template("/zguess/login.html", error="Invalid credentials")

    return render_template("/zguess/login.html")

# Route cho trang chủ của sinh viên
@app.route("/student/home")
def student_home():
    return render_template("student/StuHome.html")

# Route cho trang đăng ký khóa học (Student)
@app.route("/student/register")
def student_register():
    student_id = session["student_id"]
    # if student_id.isdigit():
    #     student_id = int(student_id)
    registered_class,rtime_info, rteacher_name = search_registered_course_by_student_code(student_id)
    zipped_registered_info = list(zip(registered_class, rtime_info, rteacher_name))    # else:
    ClassInfo, Faculty = get_all_subjects()
    # zipped_class = list(zip(SubjectID, Name))
    return render_template("student/RegisterCourse.html", student_id=session["student_id"], Faculty = Faculty, ClassInfo = ClassInfo, zipped_registered_info = zipped_registered_info)

# Route cho trang lịch học của sinh viên
@app.route("/student/calendar")
def student_calendar():
    registered_class, time_info, teacher_name = search_registered_course_by_student_code(session["student_id"])
    Schedule = list(zip(registered_class, time_info, teacher_name))
    for time in Schedule:
        print(time[1][0], time[1][1])
    print(Schedule)
    return render_template("student/StudentCalendar.html", Schedule = Schedule, days_of_week=days_of_week, time_slots=time_slots)



# Route cho trang lịch của giáo viên
@app.route("/teacher/calendar")
def teacher_calendar():
    registered_class, time_info, teacher_name = search_teaching_code_by_teacher_id(session["teacher_id"])
    Schedule = list(zip(registered_class, time_info, teacher_name))
    for time in Schedule:
        print(time[1][0], time[1][1])
    print(Schedule)
    return render_template("teacher/TeacherCalendar.html", Schedule = Schedule, days_of_week=days_of_week, time_slots=time_slots)

# Route cho trang chủ của giáo viên
@app.route("/teacher/home")
def teacher_home():
    return render_template("teacher/TeacherHome.html")

@app.route('/api/courses')
def api_courses():
    faculty = request.args.get('faculty')
    # Giả sử bạn có hàm get_courses_by_faculty(faculty) trả list các tuple (CourseID, CourseName)
    courses = get_course_through_faculty_name(faculty)
    # Đưa về JSON: [{"id": "...", "name": "..."}, ...]
    return jsonify([{"id": c[0], "name": c[1]} for c in courses])

@app.route("/search_course_through_faculty", methods=["POST"])
def search_course_through_faculty():
    course_code = request.form.get("course_code")
    facultyName = request.form.get("faculty_name")
    session["course_code"] = course_code
    class_info, time_info, teacher_name, course_name = search_course_by_code(course_code)
    zipped_info =   list(zip(class_info, time_info, teacher_name)) 
    CourseOfFaculty = get_course_through_faculty_name(facultyName)
    ClassInfo, Faculty = get_all_subjects()
    student_id = session["student_id"]
    registered_class,rtime_info, rteacher_name = search_registered_course_by_student_code(student_id)
    zipped_registered_info = list(zip(registered_class, rtime_info, rteacher_name))
    return render_template("student/RegisterCourse.html", Faculty = Faculty, CourseOfFaculty = CourseOfFaculty, zipped_info = zipped_info,ClassInfo=ClassInfo,student_id=session["student_id"], zipped_registered_info = zipped_registered_info, course_name = course_name)


@app.route("/search_course", methods=["POST"])
def search_course():
    course_code = request.form.get("course_code")
    session["course_code"] = course_code
    class_info, time_info, teacher_name, course_name = search_course_by_code(course_code)
    zipped_info =   list(zip(class_info, time_info, teacher_name)) 
    ClassInfo, Faculty = get_all_subjects()
    student_id = session["student_id"]
    registered_class,rtime_info, rteacher_name = search_registered_course_by_student_code(student_id)
    zipped_registered_info = list(zip(registered_class, rtime_info, rteacher_name))
    return render_template("student/RegisterCourse.html", Faculty = Faculty, zipped_info = zipped_info,ClassInfo=ClassInfo,student_id=session["student_id"], zipped_registered_info = zipped_registered_info, course_name = course_name)



@app.route('/add_register', methods=["POST"])
def add_register():
    student_id  = session["student_id"]
    class_id    = request.form.get("class_id")
    subject_id  = request.form.get("subject_id")
    sem_id      = request.form.get("sem_id")
    course_code = session["course_code"]
    
    
    RegisterAlready = False
    FullClass = False
    DuplicateRegistration = False
    ScheduleConflict = False
    RegisterSuccessfully = False
    try:
        RegisterSuccessfully = add_registered(student_id, class_id, subject_id, sem_id)
        print(RegisterAlready)
    except DuplicateRegistrationError:
        DuplicateRegistration = True
    except ScheduleConflictError:
        ScheduleConflict = True
    except StudentRegisterCourseDuplicate:
        RegisterAlready = True
    except Error as e:
        
        if e.sqlstate == '45000':
            FullClass = True
    finally:
        registered_class,rtime_info, rteacher_name = search_registered_course_by_student_code(student_id)
        zipped_registered_info = list(zip(registered_class, rtime_info, rteacher_name))
        class_info, time_info, teacher_name, course_name = search_course_by_code(course_code)
        zipped_info = list(zip(class_info, time_info, teacher_name))
        ClassInfo, Faculty = get_all_subjects()
        return render_template("student/RegisterCourse.html", RegisterSuccessfully = RegisterSuccessfully, DuplicateRegistration = DuplicateRegistration, ScheduleConflict = ScheduleConflict, Faculty = Faculty, ClassInfo=ClassInfo, RegisterAlready = RegisterAlready, zipped_registered_info = zipped_registered_info, zipped_info = zipped_info, FullClass = FullClass, course_name = course_name)
    
@app.route('/delete_register', methods = ["POST"])
def delete_register():
    student_id = session["student_id"]
    class_id = request.form.get("class_id")
    subject_id = request.form.get("subject_id")
    sem_id = request.form.get("sem_id")
    print(student_id, class_id, subject_id, sem_id, "hi")
    course_code = session["course_code"]
    DeleteAlready = delete_registered(student_id, class_id, subject_id, sem_id)
    class_info, time_info, teacher_name, course_name = search_course_by_code(course_code)
    zipped_info = list(zip(class_info, time_info, teacher_name))

    registered_class,rtime_info, rteacher_name = search_registered_course_by_student_code(student_id)
    zipped_registered_info = list(zip(registered_class, rtime_info, rteacher_name))
    ClassInfo, Faculty = get_all_subjects()
    return render_template("student/RegisterCourse.html", Faculty = Faculty, zipped_registered_info = zipped_registered_info, ClassInfo=ClassInfo, DeleteAlready = DeleteAlready, zipped_info = zipped_info, course_name = course_name)



if __name__ == "__main__":
    app.run(debug=True)
    
