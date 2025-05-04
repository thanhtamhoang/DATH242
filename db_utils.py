import mysql.connector
#check max student in class
#check coi lớp có active hong 
def get_all_data(universitydatabase):
    # Kết nối với cơ sở dữ liệu MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password MySQL của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )

    cursor = conn.cursor()

    # Truy vấn tất cả dữ liệu trong bảng
    query = f"SELECT * FROM {universitydatabase}"
    cursor.execute(query)

    # Lấy tất cả dữ liệu
    result = cursor.fetchall()

    # Đóng kết nối
    cursor.close()
    conn.close()

    return result

def get_courses():
    # Kết nối với cơ sở dữ liệu MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password MySQL của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )

    cursor = conn.cursor()

    # Truy vấn tất cả dữ liệu trong bảng 'courses'
    query = "SELECT * FROM subject"
    cursor.execute(query)

    # Lấy tất cả dữ liệu
    result = cursor.fetchall()

    # Đóng kết nối
    cursor.close()
    conn.close()

    return result

def search_course_by_code(course_code):
    # Kết nối với cơ sở dữ liệu MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )
    cursor = conn.cursor()
    
    # Sử dụng tham số để tránh SQL Injection
    query1ToGetClassID = """
        SELECT class.*, subject.SubjectID 
        FROM class 
        JOIN subject ON class.SubjectID = subject.SubjectID 
        WHERE class.SubjectID = %s
    """
    cursor.execute(query1ToGetClassID, (course_code,))
    class_info = cursor.fetchall()
    
    query2ToGetTime = """
            SELECT lecture.*, class.ClassID 
            FROM lecture 
            JOIN class ON class.classID = lecture.ClassID 
            WHERE class.SubjectID = %s
        """
    cursor.execute(query2ToGetTime, (course_code,))
    time_info=cursor.fetchall()
    
    query3ToGetTeacher = """
            SELECT teacher.Name
            FROM teacher
            JOIN teach ON teacher.TeacherID = teach.TeacherID 
            JOIN class ON class.SubjectID = teach.SubjectID
            WHERE class.classID = %s
        """
    cursor.execute(query3ToGetTeacher, (class_info[0][0],))
    teacher_name = cursor.fetchall()
    # Đóng kết nối
    cursor.close()
    conn.close()
    
    return class_info, time_info, teacher_name

def search_registered_course_by_student_code(student_code):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )
    cursor = conn.cursor()
    
    # Sử dụng tham số để tránh SQL Injection
    query1ToGetSubjectID = """
        SELECT register.ClassID, register.SubjectID, register.SemID
        FROM register
        WHERE register.StudentID =%s
    """
    cursor.execute(query1ToGetSubjectID, (student_code,))
    registered_class = cursor.fetchall()
    # Đóng kết nối
    cursor.close()
    conn.close()
    
    return registered_class
    
def add_registered(student_id, class_id, subject_id, sem_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="thanhtam2409@",
        database="universitydatabase"
    )
    cursor = conn.cursor()
    query = """
        INSERT INTO register (StudentID, ClassID, SubjectID, SemID)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, class_id, subject_id, sem_id))
    conn.commit()
    cursor.close()
    conn.close()


def check_login(email, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="thanhtam2409@",
        database="universitydatabase"
    )
    cursor = conn.cursor()

    try:
        query = """
            SELECT Roles, Email
            FROM User
            WHERE Email = %s AND Passwords = %s
        """
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        if not result:
            return None, None

        role, email_db = result
        student_id = None

        if role == "Student":
            cursor.execute("SELECT StudentID FROM Student WHERE Email = %s", (email_db,))
            sid_row = cursor.fetchone()
            if sid_row:
                student_id = sid_row[0]

        return role, student_id

    except Exception as e:
        print(f"[check_login] Error: {e}")
        return None, None

    finally:
        cursor.close()
        conn.close()
