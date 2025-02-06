from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Student, Discipline

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    students = Student.query.all()  # Получаем всех студентов
    return render_template('index.html', students=students)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':  # Пример проверки
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    students = Student.query.all()
    disciplines = Discipline.query.all()

    if request.method == 'POST':
        # Добавление новой дисциплины
        if 'discipline_name' in request.form:
            try:
                discipline_name = request.form['discipline_name']
                control_points = request.form['control_points']
                if control_points.isdigit() and int(control_points) > 0:
                    new_discipline = Discipline(name=discipline_name, control_points=int(control_points))
                    db.session.add(new_discipline)
                    db.session.commit()
                    flash("Дисциплина добавлена.")
                else:
                    flash("Количество контрольных точек должно быть положительным числом.")
            except Exception as e:
                flash(f"Ошибка при добавлении дисциплины: {e}")

        # Добавление нового студента
        if 'student_name' in request.form:
            student_name = request.form['student_name']
            discipline_id = request.form['discipline_id']
            new_student = Student(name=student_name, discipline_id=discipline_id)
            db.session.add(new_student)
            db.session.commit()
            flash("Студент добавлен.")

        # Установка факта сдачи задания
        if 'student_id' in request.form:
            student_id = request.form['student_id']
            student = Student.query.get(student_id)
            student.tasks += 1  # Увеличиваем количество заданий
            db.session.commit()
            flash("Задание успешно добавлено.")

    # Сортировка студентов по алфавиту или рейтингу
    sort_by = request.args.get('sort_by', 'name')  # 'name' или 'tasks'
    if sort_by == 'tasks':
        students = Student.query.order_by(Student.tasks.desc()).all()
    else:
        students = Student.query.order_by(Student.name).all()

    return render_template('dashboard.html', students=students, disciplines=disciplines)

@app.route('/set_grade/<int:student_id>', methods=['POST'])
def set_grade(student_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    student = Student.query.get(student_id)
    if request.method == 'POST':
        grade = request.form['grade']
        if grade.isdigit() and 1 <= int(grade) <= 5:
            student.grade = grade
            db.session.commit()
            flash("Оценка установлена.")
        else:
            flash("Оценка должна быть в диапазоне от 1 до 5.")

    return redirect(url_for('dashboard'))

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Студент удален.")
    return redirect(url_for('dashboard'))

@app.route('/delete_discipline/<int:discipline_id>', methods=['POST'])
def delete_discipline(discipline_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    discipline = Discipline.query.get(discipline_id)
    db.session.delete(discipline)
    db.session.commit()
    flash("Дисциплина удалена.")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание базы данных и таблиц
    app.run(debug=True)