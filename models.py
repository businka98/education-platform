from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    control_points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Discipline {self.name}>"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.Column(db.Integer, default=0)  # Количество заданий
    grade = db.Column(db.String(10), nullable=True)  # Экзаменационная оценка
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)  # Связь с дисциплиной

    discipline = db.relationship('Discipline', backref='students')

    def __repr__(self):
        return f"<Student {self.name}, Discipline: {self.discipline.name if self.discipline else 'None'}>"

    def increment_tasks(self):
        """Увеличивает количество выполненных заданий на 1."""
        self.tasks += 1

    def set_grade(self, grade):
        """Устанавливает оценку для студента."""
        if 1 <= int(grade) <= 5:  # Проверка, что оценка в пределах 1-5
            self.grade = grade
        else:
            raise ValueError("Оценка должна быть в диапазоне от 1 до 5.")