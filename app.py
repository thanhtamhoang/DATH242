from flask import Flask, render_template, request, session, redirect, url_for 
from db_utils import get_all_data, get_courses, search_course_by_code, search_registered_course_by_student_code, add_registered, check_login  # Hàm xử lý DB

app = Flask(__name__)
app.secret_key = "your_secret_key_here_123456789"
# Route trang chủ

@app.route("/home/login")
def loginpage():
    return render_template("zguess/login.html")

@app.route("/")
def home():
    return render_template("zguess/home.html")

# Route cho trang danh sách khóa học (AAO)
@app.route("/aao/courses")
def aao_courses():
    courses = get_courses()
    return render_template("AAO/CourseManagement.html", courses=courses)

# Route cho trang đăng ký khóa học (Student)
@app.route("/student/register")
def student_register():
    return render_template("student/RegisterCourse.html", student_id=session["student_id"])

# Route cho trang lịch học của sinh viên
@app.route("/student/calendar")
def student_calendar():
    return render_template("student/StudentCalendar.html")

# Route cho trang chủ của sinh viên
@app.route("/student/home")
def student_home():
    return render_template("student/StuHome.html")

# Route cho trang lịch của giáo viên
@app.route("/teacher/calendar")
def teacher_calendar():
    return render_template("teacher/TeacherCalendar.html")

# Route cho trang chủ của giáo viên
@app.route("/teacher/home")
def teacher_home():
    return render_template("teacher/TeacherHome.html")

# Route lấy danh sách khóa học từ DB
@app.route("/aao/courses")
def course_list():
    classes = get_all_data("courses")  # Giả sử "courses" là bảng trong DB
    return render_template("AAO/CourseManagement.html", classes=classes)

@app.route("/aao/home")
def aao_home():
    return render_template("AAO/AAOHome.html")


@app.route("/search_course", methods=["POST"])
def search_course():
    # Lấy input mã môn học từ form
    course_code = request.form.get("course_code")
    class_info, time_info, teacher_name = search_course_by_code(course_code)
    zipped_info = list(zip(class_info, time_info, teacher_name))
    return render_template("student/RegisterCourse.html", zipped_info = zipped_info)

@app.route("/get_registered_course", methods=["POST"])
def get_registered_course():
    # Lấy input mã môn học từ form
    student_code = request.form.get("studentID")
    if student_code.isdigit():
        student_code = int(student_code)
        registered_class = search_registered_course_by_student_code(student_code)
    else:
        student_code = None
        registered_class = []
    return render_template("student/RegisterCourse.html", registered_class = registered_class)

@app.route('/add_register', methods=["POST"])
def add_register():
    student_id = request.form.get("student_id")
    class_id = request.form.get("class_id")
    subject_id = request.form.get("subject_id")
    sem_id = request.form.get("sem_id")
    return add_registered(student_id, class_id, subject_id, sem_id)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["username"]  # <-- đây thực ra đang là email
        password = request.form["password"]

        role, student_id = check_login(email, password)

        if role:
            session["email"] = email
            session["role"] = role
            if role == "Student":
                session["student_id"] = student_id
                return redirect(url_for("student_register"))
            elif role == "Teacher":
                return redirect(url_for("teacher_home"))
            elif role == "AAO":
                return redirect(url_for("aao_dashboard"))
        else:
            return render_template("/zguess/login.html", error="Invalid credentials")

    return render_template("/zguess/login.html")

if __name__ == "__main__":
    app.run(debug=True)
    
