import mysql.connector
from mysql.connector import Error
from exception import DuplicateRegistrationError, ScheduleConflictError, StudentRegisterCourseDuplicate

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

def search_course_by_code(course_code): #for student
    # Kết nối với cơ sở dữ liệu MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )
    cursor = conn.cursor()
    
    # Sử dụng tham số để tránh SQL Injection
    queryToGetCourseName = """
        SELECT Name 
        From Subject
        WHERE Subject.SubjectID = %s
    """
    cursor.execute(queryToGetCourseName, (course_code,))
    course_name = cursor.fetchall()
    query1ToGetClassID = """
        SELECT class.*
        FROM class 
        WHERE class.SubjectID = %s and class.Status = 'Active' and class.SemID = %s
    """
    cursor.execute(query1ToGetClassID, (course_code,"HK242",))
    class_info = cursor.fetchall()
    if not class_info:
        print(course_code)
        return [], [], [], course_name
    query2ToGetTime = """
                SELECT Start, End, DAY, Room
                FROM lecture 
                WHERE lecture.ClassID = %s AND lecture.SubjectID = %s AND lecture.SemID=%s
            """
    time_info = []
    for eachclass in class_info:
        cursor.execute(query2ToGetTime, (eachclass[0],eachclass[1], eachclass[2],))
        time_info += cursor.fetchall()

    teacher_name = []
    query3ToGetTeacher = """
            SELECT teacher.Name
            FROM teacher
            JOIN teach ON teacher.TeacherID = teach.TeacherID
            WHERE teach.SubjectID = %s AND teach.ClassID = %s
        """
    for eachClass in class_info:
        cursor.execute(query3ToGetTeacher, (course_code, eachClass[0],))
        teacher_name += cursor.fetchall()
    # Đóng kết nối
    cursor.close()
    conn.close()
    return class_info, time_info, teacher_name, course_name

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
    queryToGetCourseName = """
        SELECT Name, Credits
        From Subject
        WHERE Subject.SubjectID = %s
    """
    cursor.execute(queryToGetCourseName, (course_code,))
    course_name = cursor.fetchall()
    query1ToGetClassID = """
        SELECT class.*
        FROM class 
        WHERE class.SubjectID = %s and class.Status = 'Active' and class.SemID = %s
    """
    cursor.execute(query1ToGetClassID, (course_code,"HK242",))
    class_info = cursor.fetchall()
    if not class_info:
        print(course_code)
        return [], [], [], course_name
    query2ToGetTime = """
                SELECT Start, End, DAY, Room
                FROM lecture 
                WHERE lecture.ClassID = %s AND lecture.SubjectID = %s AND lecture.SemID=%s
            """
    time_info = []
    for eachclass in class_info:
        cursor.execute(query2ToGetTime, (eachclass[0],eachclass[1], eachclass[2],))
        time_info += cursor.fetchall()

    teacher_name = []
    query3ToGetTeacher = """
            SELECT teacher.Name
            FROM teacher
            JOIN teach ON teacher.TeacherID = teach.TeacherID
            WHERE teach.SubjectID = %s AND teach.ClassID = %s
        """
    for eachClass in class_info:
        cursor.execute(query3ToGetTeacher, (course_code, eachClass[0],))
        teacher_name += cursor.fetchall()
    # Đóng kết nối
    cursor.close()
    conn.close()
    return class_info, time_info, teacher_name, course_name

def search_all_course_by_code(course_code):
    # Kết nối với cơ sở dữ liệu MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )
    cursor = conn.cursor()
    
    # Sử dụng tham số để tránh SQL Injection
    queryToGetCourseName = """
        SELECT Name 
        From Subject
        WHERE Subject.SubjectID = %s
    """
    cursor.execute(queryToGetCourseName, (course_code,))
    course_name = cursor.fetchall()
    query1ToGetClassID = """
        SELECT class.*
        FROM class 
        WHERE class.SubjectID = %s 
    """
    cursor.execute(query1ToGetClassID, (course_code,))
    class_info = cursor.fetchall()
    if not class_info:
        print(course_code)
        return [], [], [], course_name
    query2ToGetTime = """
                SELECT Start, End, DAY, Room
                FROM lecture 
                WHERE lecture.ClassID = %s AND lecture.SubjectID = %s AND lecture.SemID=%s
            """
    time_info = []
    for eachclass in class_info:
        cursor.execute(query2ToGetTime, (eachclass[0],eachclass[1], eachclass[2],))
        time_info += cursor.fetchall()
    print(time_info,"hi")
    teacher_name = []
    query3ToGetTeacher = """
            SELECT teacher.Name
            FROM teacher
            JOIN teach ON teacher.TeacherID = teach.TeacherID
            WHERE teach.SubjectID = %s AND teach.ClassID = %s
        """
    for eachClass in class_info:
        cursor.execute(query3ToGetTeacher, (course_code, eachClass[0],))
        teacher_name += cursor.fetchall()
    # Đóng kết nối
    cursor.close()
    conn.close()
    return class_info, time_info, teacher_name, course_name

def search_registered_course_by_student_code(student_code):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )
    cursor = conn.cursor()
    query1ToGetSubjectID = """
                SELECT register.ClassID, register.SubjectID, register.SemID
                FROM register
                WHERE register.StudentID =%s
            """
    cursor.execute(query1ToGetSubjectID, (student_code,))
    registered_class = cursor.fetchall()
    query2ToGetTime = """
                SELECT Start, End, DAY, Room
                FROM lecture 
                WHERE lecture.ClassID = %s AND lecture.SubjectID = %s AND lecture.SemID=%s
            """
    time_info = []
    for eachclass in registered_class:
        cursor.execute(query2ToGetTime, (eachclass[0],eachclass[1], eachclass[2],))
        time_info += cursor.fetchall()

    teacher_name = []
    query3ToGetTeacher = """
            SELECT Name
            FROM teacher
            JOIN teach ON teacher.TeacherID = teach.TeacherID
            WHERE teach.SubjectID = %s AND teach.ClassID = %s AND teach.SemID = %s
        """
    for eachClass in registered_class:
        cursor.execute(query3ToGetTeacher, (eachClass[1], eachClass[0],"HK242",))
        teacher_name += cursor.fetchall()
    # Đóng kết nối
    cursor.close()
    conn.close()
    return registered_class, time_info, teacher_name
    
def add_registered(student_id, class_id, subject_id, sem_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="thanhtam2409@",
        database="universitydatabase"
    )
    cursor = conn.cursor()
    query0 = """
            SELECT 1
            FROM register
            WHERE register.StudentID = %s AND register.classID = %s AND register.SubjectID = %s AND register.SemID = %s
            LIMIT 1
        """
    cursor.execute(query0, (student_id, class_id, subject_id, sem_id))
    result = cursor.fetchall()
    if result:
        print("hi")
        raise DuplicateRegistrationError()
    cursor.execute("""
            SELECT `DAY`, `Start`, `End`
            FROM lecture
            WHERE ClassID=%s AND SubjectID=%s AND SemID=%s
        """, (class_id, subject_id, sem_id))
    lec = cursor.fetchone()
    if not lec:
        raise Error(f"No class {class_id}-{subject_id}-{sem_id}")
    new_day, new_start, new_end = lec
    cursor.execute("""SELECT r.ClassID, l.DAY, l.Start, l.End
            FROM register r
            JOIN lecture l
              ON r.ClassID   = l.ClassID
             AND r.SubjectID = l.SubjectID
             AND r.SemID     = l.SemID
            WHERE r.StudentID = %s
              AND l.DAY       = %s
              AND NOT (
                   l.End   <= %s
                OR l.Start >= %s
              )
            LIMIT 1""", (student_id, new_day, new_start, new_end))
    if cursor.fetchall():
        raise ScheduleConflictError()
    try:
        query = """
            INSERT INTO register (StudentID, ClassID, SubjectID, SemID)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (student_id, class_id, subject_id, sem_id))
        conn.commit()
        return False
    except Error as e:
        if e.sqlstate == '45000':
            raise StudentRegisterCourseDuplicate()
        else:
            
            return True 
    finally:
        cursor.close()
        conn.close()
        return True

def delete_registered(student_id, class_id, subject_id, sem_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="thanhtam2409@",
        database="universitydatabase"
    )
    cursor = conn.cursor()
    query0 = """
        SELECT * 
        FROM register
        WHERE register.StudentID = %s AND register.classID = %s AND register.SubjectID = %s AND register.SemID = %s
    """
    cursor.execute(query0, (student_id, class_id, subject_id, sem_id))
    result = cursor.fetchall()
    if not result:
        return False
    query1 = """
        DELETE FROM register 
        WHERE register.StudentID = %s AND register.ClassID = %s AND register.SubjectID = %s AND register.SemID = %s
    """
    cursor.execute(query1, (student_id, class_id, subject_id, sem_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True
    
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
        

        user_id = None

        if role == "Student":
            cursor.execute("SELECT StudentID FROM Student WHERE Email = %s", (email_db,))
            sid_row = cursor.fetchone()
            if sid_row:
                user_id = sid_row[0]
        elif role == "Teacher":
            cursor.execute("SELECT TeacherID FROM Teacher Where Email = %s", (email_db,))
            sid_row = cursor.fetchone()
            if sid_row:
                user_id = sid_row[0]
        return role, user_id

    except Exception as e:
        print(f"[check_login] Error: {e}")
        return None, None

    finally:
        cursor.close()
        conn.close()

def get_all_subjects():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="thanhtam2409@",
        database="universitydatabase"
    )
    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT FName FROM Faculty
        """
        cursor.execute(query,)
        Faculty = cursor.fetchall()
        cursor = conn.cursor()
        query = """
            SELECT SubjectID, Name FROM subject
        """
        cursor.execute(query,)
        results = cursor.fetchall()
        return results, Faculty
    except mysql.connector.Error as e:
        raise
        return []
    # SubjectID, Name = results
    finally:
        if cursor:
            cursor.close()
        conn.close()

def get_course_through_faculty_name(FacultyName):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="thanhtam2409@",
        database="universitydatabase"
    )
    cursor = conn.cursor()
    query = """
        SELECT * FROM subject WHERE FName = %s
    """
    cursor.execute(query,(FacultyName,))
    results = cursor.fetchall()
    # SubjectID, Name = results
    cursor.close()
    conn.close()
    return results  


def search_teaching_code_by_teacher_id(teacher_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",       # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )
    cursor = conn.cursor()
    query1ToGetSubjectID = """
                SELECT teach.ClassID, teach.SubjectID
                FROM teach
                WHERE teach.TeacherID =%s AND teach.SemID = %s
            """
    cursor.execute(query1ToGetSubjectID, (teacher_id,"HK242"))
    teaching_class = cursor.fetchall()
    query2ToGetTime = """
                SELECT Start, End, DAY, Room
                FROM lecture 
                WHERE lecture.ClassID = %s AND lecture.SubjectID = %s AND lecture.SemID=%s
            """
    time_info = []
    for eachclass in teaching_class:
        cursor.execute(query2ToGetTime, (eachclass[0],eachclass[1], "HK242",))
        time_info += cursor.fetchall()

    teacher_name = []
    query3ToGetTeacher = """
            SELECT Name
            FROM teacher
            JOIN teach ON teacher.TeacherID = teach.TeacherID
            WHERE teach.SubjectID = %s AND teach.ClassID = %s AND teach.SemID = %s
        """
    for eachClass in teaching_class:
        cursor.execute(query3ToGetTeacher, (eachClass[1], eachClass[0],"HK242",))
        teacher_name += cursor.fetchall()
    # Đóng kết nối
    cursor.close()
    conn.close()
    return teaching_class, time_info, teacher_name