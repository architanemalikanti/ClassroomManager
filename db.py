from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table("association", db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"))
)

# your classes here


#class for a course:
class Course(db.Model):
    #name of model
    __tablename__ = "courses"
    #columns
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    instructor = db.Column(db.String, nullable=False)
    

    #relationships
    assignments = db.relationship("Assignment", cascade="delete")
    students = db.relationship("Users", secondary=association_table,back_populates="courses")



    #now we need to initialize this object
    #initialize:
    def __init__(self, **kwargs):
        """
        initialize an assignment object
        """
        self.code=kwargs.get("code", "")
        self.name=kwargs.get("name", "")
        self.instructor = kwargs.get("instructor", "")




    #serialize method
    def serialize(self):
        return{
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [s.serialize() for s in self.assignment],
            "students": [c.simple_serialize() for c in self.users],
            "instructor": self.instructor
        }
    
    #simple serialize method:
    def simple_serialize(self):
        return{
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "instructor": self.instructor
        }


#class for an assignment:
class Assignment(db.Model):
    #name of model:
    __tablename__= "assignment"

    #columns:
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    #initialize:
    def __init__(self, **kwargs):
        """
        initialize an assignment object
        """
        self.title=kwargs.get("title", "")
        self.due_date=kwargs.get("due_date", None)
        self.course_id=kwargs.get("course_id") #raise an exeption, we will never have a case where field is empty. 


    #serialize:
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date.strftime("%Y-%m-%d %H:%M:%S"),
            "course_id": self.course_id

        }


#class for the Users: many to many relationship between users and course
class Users(db.Model):
    __tablename__= "users"
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    courses = db.relationship("Course", secondary=association_table, back_populates='students')


    #initialize: a users object:
    def __init__(self, **kwargs):
        """
        initialize a users object
        """
        self.name= kwargs.get("name")
        self.netid= kwargs.get("netid")


    #serialize method:
    def serialize(self):
        """
        serialize a category object
        """
        return{
            "id": self.id,
            "name": self.name,
            "netid": self.netid,

            #all the courses that user has
            "courses": [c.simple_serialize(self) for c in self.courses]
        }
    
    #simple serialize for the users model
    def simple_serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }
