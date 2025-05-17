from flask import jsonify
import mysql.connector
import unidecode
from mysql.connector import Error
from exception import AddTeacherUnsuccessfully

def generate_email(name):
    name = unidecode.unidecode(name.lower())
    name = ''.join(name.split())
    return f"{name}@university.edu"

def get_all_teacher():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password MySQL của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )
    cursor = conn.cursor()
    query = "SELECT teacher.* FROM teacher where teacher.IsDeleted = FALSE"
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return result

def get_all_faculty():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Thay bằng username MySQL của bạn
        password="thanhtam2409@",  # Thay bằng password MySQL của bạn
        database="universitydatabase"  # Thay bằng tên database của bạn
    )
    cursor = conn.cursor()
    query = "SELECT Faculty.FName FROM Faculty"
    
    cursor.execute(query,)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return result
    


def add_new_teacher(name, department):
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor()
    email = generate_email(name)
    try:
        query1 = """
        INSERT INTO User (Email, Passwords, Roles) VALUES (%s, 'password123', 'Teacher')
        """
        query2 = """
        INSERT INTO TEACHER (Name, FName, Email) VALUES (%s, %s, %s)
        """

        cursor.execute(query1, (email,))
        
        cursor.execute(query2, (name, department, email,))
    except Error as e:
        raise AddTeacherUnsuccessfully()
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def view_teacher_info(teacherID):
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor() 
    query = """
        SELECT 
        c.ClassID,
        c.SubjectID,
        c.SemID,
        c.Status,
        s.Name        AS SubjectName,
        t.Name        AS TeacherName,
        t.Department  AS TeacherDept
        FROM Class AS c
        JOIN teach AS te
        ON c.ClassID   = te.ClassID
        AND c.SubjectID = te.SubjectID
        JOIN Teacher AS t
        ON te.TeacherID = t.TeacherID
        JOIN Subject AS s
        ON c.SubjectID = s.SubjectID
        WHERE t.TeacherID = %s;
    
    """
    cursor.execute(query, (teacherID,))
    result = cursor.fetchall()
    print(result)
    # query1 = """
    # SELECT Teacher.Name, Teacher.Department FROM Teacher WHERE Teacher.TeacherID = %s
    # """
    # result = cursor.execute(query1, (teacherID,))
    conn.commit()
    cursor.close()
    conn.close()
    return result

def delete_old_teacher(teacherID):
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor()
    cursor.execute("SELECT Email FROM Teacher WHERE TeacherID = %s", (teacherID,))
    email = cursor.fetchone()
    email = email[0]
    # query = """
    #     DELETE FROM User
    #     WHERE User.Email = %s AND User.Roles = 'Teacher'
    # """
    # cursor.execute(query, (email,))
    # query1 = """
    #     DELETE FROM Teacher WHERE Teacher.TeacherID = %s
    #     """
    query1 = """
        UPDATE Teacher
        SET isdeleted = TRUE
        WHERE TeacherID = %s
    """
    cursor.execute(query1, (teacherID,))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def view_course_info(courseID):
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Course WHERE CourseID = %s", (courseID,))
    course_info = cursor.fetchone()
    email = email[0]
    query = """
        DELETE FROM User
        WHERE User.Email = %s AND User.Roles = 'Teacher'
    """
    cursor.execute(query, (email,))
    query1 = """
        DELETE FROM Teacher WHERE Teacher.TeacherID = %s
        """
    
    cursor.execute(query1, (teacherID,))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def add_new_course(courseID, Name, Credits, RequiredCredits):
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Subject (SubjectID, Name, Credits, RequiredCredits) VALUES (%s, %s, %s, %s)", (courseID, Name, Credits, RequiredCredits))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_all_teachers():
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor()
    cursor.execute("SELECT Teacher.TeacherID, Teacher.Name FROM Teacher",())
    teacher = cursor.fetchall()
    cursor.close()
    conn.close()
    return teacher

def add_class_to_db(course_id, class_id, teacher_id, start_time, end_time, day, room):
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor()
    #kiểm tra coi có trùng class_id không
    try:
        check_q = """
                SELECT 1 FROM Class
                WHERE ClassID=%s AND SubjectID=%s AND SemID=%s
            """
        cursor.execute(check_q, (class_id, course_id, "HK242"))
        if cursor.fetchone():
            return False
        insert_class = """
                INSERT INTO Class (ClassID, SubjectID, SemID, Status, MaxStudent, CurrentStudent)
                VALUES (%s, %s, %s, 'Active', 50, 0)
            """
        cursor.execute(insert_class, (class_id, course_id, "HK242"))

        # 5. Chèn vào Lecture
        insert_lec = """
            INSERT INTO Lecture (ClassID, SubjectID, SemID, Start, End, DAY, Room)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_lec, (class_id, course_id, "HK242", start_time, end_time, day, room))

        # 6. Chèn vào Teach
        insert_teach = """
            INSERT INTO Teach (TeacherID, ClassID, SubjectID, SemID)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_teach, (teacher_id, class_id, course_id, "HK242"))

        # 7. Commit nếu tất cả OK
        conn.commit()
        return True

    except Error as e:
        conn.rollback()
        # Có thể log e.errno, e.msg
        raise
    finally:
        cursor.close()
        conn.close()
        
def get_class_of_teacher(teacher_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor()
    query = """
      SELECT c.ClassID, s.Name, c.SemID,c.Status
      FROM class c
      JOIN teach t ON c.ClassID = t.ClassID AND c.SubjectID = t.SubjectID
      JOIN Subject s ON c.SubjectID = s.SubjectID
      WHERE t.TeacherID = %s
    """
    cursor.execute(query, (teacher_id,))
    result = cursor.fetchall()
    cursor.close(); conn.close()
    # Trả về JSON
    return jsonify({
      'classes': [
        {'class_id': r[0], 'subject_name': r[1], 'sem_id': r[2], 'status':r[3]}
        for r in result
      ]
    })
    
def toggle_class(class_id, course_id, sem_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="thanhtam2409@",  
        database="universitydatabase"  
    )
    cursor = conn.cursor()
    cursor.execute(
      "SELECT Status FROM Class WHERE ClassID=%s AND SubjectID = %s AND SemID=%s",
      (class_id, course_id, sem_id)
    )
    current = cursor.fetchone()[0]
    # 2) Đổi ngược lại
    new_status = 'Inactive' if current == 'Active' else 'Active'
    cursor.execute(
      "UPDATE Class SET Status=%s WHERE ClassID=%s AND SemID=%s",
      (new_status, class_id, sem_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return new_status

# def get_course_through_faculty_and_semester(FName, SemID):
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",  # Thay bằng username MySQL của bạn
#         password="thanhtam2409@",  # Thay bằng password MySQL của bạn
#         database="universitydatabase"  # Thay bằng tên database của bạn
#     )
#     cursor = conn.cursor()
#     query = """
#     SELECT Subject.* 
#     FROM Subject 
#     WHERE Subject.FName = %s AND Subject.
#     """
    
#     cursor.execute(query,)
#     result = cursor.fetchall()
#     cursor.close()
#     conn.close()
    
#     return result