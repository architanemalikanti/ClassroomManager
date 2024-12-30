from db import db
from flask import Flask, request
import dao
from db import db
from db import Course, Assignment, Users
import json


#define db filename
app = Flask(__name__)
db_filename = "cms.db"

#set up config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

#initialize app
db.init_app(app)
with app.app_context():
    db.create_all()


#generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# your routes here

#route #1: get all courses.
@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    courses = [t.simple_serialize() for t in Course.query.all()]
    return success_response(courses)


#route #2: create a course
@app.route("/api/courses/", methods=["POST"])
def create_course():
    body = json.loads(request.data)
    #create a course object with the input data:

    new_course=Course(
        code=body.get('code'),
        name=body.get('name')
    )

    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


#route3: get a course
@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("course not found!")
    return success_response(course.simple_serialize())

#route4: delete a specific course
@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_task(course_id):
    """
    Endpoint for deleting a task by id
    """
    course= Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Task not found!")
    
    db.session.delete(course)
    db.session.commit()
    return success_response(course.simple_serialize())

#route 5: create a user
@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user- they're not in any courses just yet tho
    """
    
    body = json.loads(request.data)
    new_user = Users(
        name=body.get("name"),
        netid= body.get("netid"),
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


#route 6: get a specific user
@app.route("/api/users/<int:course_id>/", methods=["GET"])
def get_specific_user(user_id):
    """
    Endpoint for getiing a specific user
    """
 
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found!")
    return success_response(user.serialize())



#route 7: add a user to a course
@app.route("/api/users/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding an existing user to a course.
    """
    
    body = json.loads(request.data)
    user_id = body.get("user_id")
    type= body.get("type")

    #get the course first
    course=Course.query.filter_by(id=course_id).first()

    if course is None:
        return failure_response("course not found!")
    

    #now, get the user:
    user= Users.query.filter_by(id=user_id)

    #add "user" to the students array for the course
    course.students.append(user)
    db.session.commit()
    return success_response(course.serialize())




#route 8: add a an assignment to a course
@app.route("/api/users/<int:course_id>/assignment/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding an assignment to a course.
    """
    
    body = json.loads(request.data)
    title = body.get("title")
    due_date= body.get("due_date")

    #get the course first
    course=Course.query.filter_by(id=course_id).first()

    if course is None:
        return failure_response("course not found!")
    

    #now, create the assignment:
    assignment= Assignment(
        title=body.get("name"),
        due_date=body.get("due_date")
    )
    #add this newly created assignment to a course_id

    course.assignments.append(assignment)
    db.session.commit()
    return success_response(assignment.serialize())






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
