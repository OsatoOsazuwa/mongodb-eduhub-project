
# ### Mongodb Eduhub



## Importing libraries
from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timezone, timedelta
import pandas as pd




import uuid
import random


# 



# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["eduhub_db"]




# users Collection — with Validation Rules
db.create_collection(
    "users",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["userId", "email", "firstName", "lastName", "role"],
            "properties": {
                "userId": {"bsonType": "string"},
                "email": {
                    "bsonType": "string",
                    "pattern": "^.+@.+$"
                },
                "firstName": {"bsonType": "string"},
                "lastName": {"bsonType": "string"},
                "role": {
                    "enum": ["student", "instructor"]
                },
                "dateJoined": {"bsonType": "date"},
                "profile": {
                    "bsonType": "object",
                    "properties": {
                        "bio": {"bsonType": "string"},
                        "avatar": {"bsonType": "string"},
                        "skills": {
                            "bsonType": "array",
                            "items": {"bsonType": "string"}
                        }
                    }
                },
                "isActive": {"bsonType": "bool"}
            }
        }
    }
)




# courses Collection — with Validation Rules
db.create_collection(
    "courses",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["courseId", "title", "instructorId", "level"],
            "properties": {
                "courseId": {"bsonType": "string"},
                "title": {"bsonType": "string"},
                "description": {"bsonType": "string"},
                "instructorId": {"bsonType": "string"},
                "category": {"bsonType": "string"},
                "level": {
                    "enum": ["beginner", "intermediate", "advanced"]
                },
                "duration": {"bsonType": "double"},
                "price": {"bsonType": "double"},
                "tags": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"}
                },
                "createdAt": {"bsonType": "date"},
                "updatedAt": {"bsonType": "date"},
                "isPublished": {"bsonType": "bool"},
                "rating": {"bsonType": "double"},
            }
        }
    }
)




enrollments_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["enrollmentId", "studentId", "courseId", "enrolledAt", "status"],
            "properties": {
                "enrollmentId": {"bsonType": "string"},
                "studentId": {"bsonType": "string"},  # Reference to users.userId
                "courseId": {"bsonType": "string"},   # Reference to courses.courseId
                "enrolledAt": {"bsonType": "date"},
                "status": {
                    "enum": ["active", "completed", "dropped"]
                },
                "progress": {
                    "bsonType": "double",
                    "minimum": 0,
                    "maximum": 100
                }
            }
        }
    }
}

lessons_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["lessonId", "courseId", "title", "content", "order"],
            "properties": {
                "lessonId": {"bsonType": "string"},
                "courseId": {"bsonType": "string"},  # Reference to courses.courseId
                "title": {"bsonType": "string"},
                "content": {"bsonType": "string"},
                "resources": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"}
                },
                "order": {"bsonType": "int"},  # Lesson sequence
                "createdAt": {"bsonType": "date"}
            }
        }
    }
}

assignments_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["assignmentId", "courseId", "title", "description", "dueDate"],
            "properties": {
                "assignmentId": {"bsonType": "string"},
                "courseId": {"bsonType": "string"},  # Reference to courses.courseId
                "lessonId": {"bsonType": "string"},  # Optional, for lesson-specific assignments
                "title": {"bsonType": "string"},
                "description": {"bsonType": "string"},
                "dueDate": {"bsonType": "date"},
                "points": {"bsonType": "int"},
                "createdAt": {"bsonType": "date"}
            }
        }
    }
}

submissions_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["submissionId", "assignmentId", "studentId", "submittedAt"],
            "properties": {
                "submissionId": {"bsonType": "string"},
                "assignmentId": {"bsonType": "string"},  # Reference to assignments.assignmentId
                "studentId": {"bsonType": "string"},     # Reference to users.userId
                "content": {"bsonType": "string"},
                "grade": {"bsonType": "double"},
                "feedback": {"bsonType": "string"},
                "submittedAt": {"bsonType": "date"}
            }
        }
    }
}




db.create_collection("enrollments", validator=enrollments_schema["validator"])
db.create_collection("lessons", validator=lessons_schema["validator"])
db.create_collection("assignments", validator=assignments_schema["validator"])
db.create_collection("submissions", validator=submissions_schema["validator"])


# ### Section Title: Task 1.2 – Document Schema Design



# Users Collection Schema
user_schema = {
    "_id": "ObjectId (auto-generated)",
    "userId": "string (unique)",
    "email": "string (unique, required)",
    "firstName": "string (required)",
    "lastName": "string (required)",
    "role": "string (enum: ['student', 'instructor'])",
    "dateJoined": "datetime",
    "profile": {
        "bio": "string",
        "avatar": "string",
        "skills": ["string"]
    },
    "isActive": "boolean"
}

# Courses Collection Schema
course_schema = {
    "_id": "ObjectId (auto-generated)",
    "courseId": "string (unique)",
    "title": "string (required)",
    "description": "string",
    "instructorId": "string (reference to users)",
    "category": "string",
    "level": "string (enum: ['beginner', 'intermediate', 'advanced'])",
    "duration": "number (in hours)",
    "price": "number",
    "tags": ["string"],
    "createdAt": "datetime",
    "updatedAt": "datetime",
    "isPublished": "boolean",
    "rating": "number"
}

# Enrollments Collection Schema
enrollment_schema = {
    "_id": "ObjectId (auto-generated)",
    "enrollmentId": "string (unique)",
    "studentId": "string (reference to users)",
    "courseId": "string (reference to courses)",
    "enrolledAt": "datetime",
    "status": "string (enum: ['active', 'completed', 'dropped'])",
    "progress": "number"
}

# Lessons Collection Schema
lesson_schema = {
    "_id": "ObjectId (auto-generated)",
    "lessonId": "string (unique)",
    "courseId": "string (reference to courses)",
    "title": "string (required)",
    "content": "string",
    "resources": ["string"],
    "order": "number",
    "createdAt": "datetime"
}

# Assignments Collection Schema
assignment_schema = {
    "_id": "ObjectId (auto-generated)",
    "assignmentId": "string (unique)",
    "courseId": "string (reference to courses)",
    "lessonId": "string (reference to lessons)",
    "title": "string (required)",
    "description": "string",
    "dueDate": "datetime",
    "points": "number",
    "createdAt": "datetime"
}

# Submissions Collection Schema
submission_schema = {
    "_id": "ObjectId (auto-generated)",
    "submissionId": "string (unique)",
    "assignmentId": "string (reference to assignments)",
    "studentId": "string (reference to users)",
    "content": "string",
    "grade": "number",
    "feedback": "string",
    "submittedAt": "datetime"
}


# 

# Task 2.1: Insert Sample Data



faker = Faker()





#Inserting sample data in users collection
roles = ["student"] * 14 + ["instructor"] * 6
random.shuffle(roles)

users = []
for i in range(20):
    user = {
        "userId": str(uuid.uuid4()),
        "email": faker.email(),
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "role": roles[i],
        "dateJoined": faker.date_time_this_year(),
        "profile": {
            "bio": faker.text(150),
            "avatar": faker.image_url(),
            "skills": [faker.word() for _ in range(random.randint(1, 4))]
        },
        "isActive": random.choice([True, False])
    }
    users.append(user)

db.users.insert_many(users)




# Inserting sample data in courses collection

instructors = [u for u in users if u["role"] == "instructor"]
categories = ["Data Science", "Web Dev", "Business", "AI", "Cybersecurity"]
levels = ["beginner", "intermediate", "advanced"]

courses = []
for _ in range(8):
    instructor = random.choice(instructors)
    course = {
        "courseId": str(uuid.uuid4()),
        "title": faker.catch_phrase(),
        "description": faker.text(150),
        "instructorId": instructor["userId"],
        "category": random.choice(categories),
        "level": random.choice(levels),
        "duration": round(random.uniform(1.5, 20.0), 1),
        "price": round(random.uniform(10, 100), 2),
        "tags": faker.words(nb=3),
        "createdAt": faker.date_time_this_year(),
        "updatedAt": faker.date_time_this_year(),
        "isPublished": random.choice([True, False])
    }
    courses.append(course)

db.courses.insert_many(courses)




## Inserting 15 Enrollments (studentId + courseId)
students = [u for u in users if u["role"] == "student"]
statuses = ["active", "completed", "dropped"]

enrollments = []
for _ in range(15):
    student = random.choice(students)
    course = random.choice(courses)
    enrollment = {
        "enrollmentId": str(uuid.uuid4()),
        "studentId": student["userId"],
        "courseId": course["courseId"],
        "enrolledAt": faker.date_time_this_year(),
        "status": random.choice(statuses),
        "progress": round(random.uniform(0, 100), 2)
    }
    enrollments.append(enrollment)

db.enrollments.insert_many(enrollments)




# Inserting sample data in lessons collection
lessons = []
for _ in range(25):
    course = random.choice(courses)
    lesson = {
        "lessonId": str(uuid.uuid4()),
        "courseId": course["courseId"],
        "title": faker.sentence(),
        "content": faker.text(300),
        "resources": [faker.url() for _ in range(random.randint(0, 3))],
        "order": random.randint(1, 10),
        "createdAt": faker.date_time_this_year()
    }
    lessons.append(lesson)

db.lessons.insert_many(lessons)




# Inserting sample data in assignments collection
assignments = []

for _ in range(10):  # Generate 10 sample assignments
    course = random.choice(courses)

    assignment = {
        "assignmentId": str(uuid.uuid4()),
        "courseId": course["courseId"],
        "title": faker.sentence(nb_words=6),
        "description": faker.text(max_nb_chars=100),
        "dueDate": faker.future_datetime(end_date="+30d"),
        "points": faker.random_int(min=5, max=20),
        "createdAt": faker.date_time_this_year()
    }

    # Add optional lessonId only if lessons exist and randomly chosen
    if lessons and random.choice([True, False]):
        lesson = random.choice(lessons)
        if "lessonId" in lesson:
            assignment["lessonId"] = lesson["lessonId"]

    assignments.append(assignment)
db.assignments.insert_many(assignments)




# Inserting sample data in submissions collection
submissions = []
for _ in range(12):
    student = random.choice(students)
    assignment = random.choice(assignments)
    submission = {
        "submissionId": str(uuid.uuid4()),
        "assignmentId": assignment["assignmentId"],
        "studentId": student["userId"],
        "content": faker.paragraph(nb_sentences=5),
        "grade": round(random.uniform(0, 100), 2),
        "feedback": faker.sentence(),
        "submittedAt": faker.date_time_this_year()
    }
    submissions.append(submission)

db.submissions.insert_many(submissions)


# ### Section 3: Basic CRUD Operations



### Section 3.1 Create Operations
# 1. Add a new student user
new_student = {
    "userId": str(uuid.uuid4()),
    "email": "newstudent@example.com",
    "firstName": "Ada",
    "lastName": "Okonkwo",
    "role": "student",
    "dateJoined": datetime.now(timezone.utc),
    "isActive": True,
    "profile": {
        "bio": "Excited to learn!",
        "avatar": "https://example.com/avatar/ada.jpg",  # URL or path to avatar image
        "skills": ["Python", "Data Analysis"]
    }
}
db.users.insert_one(new_student)

# 2. Create a new course
new_course = {
    "courseId": str(uuid.uuid4()),
    "title": "Data Analysis with Python",
    "description": "Learn how to analyze data using Python.",
    "instructorId": db.users.find_one({"role": "instructor"})["userId"],
    "category": "Data Science",
    "level": "beginner",
    "duration": 15.0,
    "price": 0.0,
    "tags": ["data", "python"],
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc),
    "isPublished": False
}
db.courses.insert_one(new_course)

# 3. Enroll a student in a course
new_enrollment = {
    "enrollmentId": str(uuid.uuid4()),
    "studentId": new_student["userId"],
    "courseId": new_course["courseId"],
    "enrolledAt": datetime.now(timezone.utc),
    "status": "active",
    "progress": 0.0
}
db.enrollments.insert_one(new_enrollment)

# 4. Add a new lesson to an existing course
new_lesson = {
    "lessonId": str(uuid.uuid4()),
    "courseId": new_course["courseId"],
    "title": "Introduction to Data Analysis",
    "content": "This lesson introduces basic concepts in data analysis.",
    "resources": ["https://docs.python.org"],
    "order": 1,
    "createdAt": datetime.now(timezone.utc)
}
db.lessons.insert_one(new_lesson)




### Section 3.2 Read Operations
# 1. Find all active students
active_students = list(db.users.find({"role": "student", "isActive": True}))

# 2. Retrieve course details with instructor info
course_with_instructor = db.courses.aggregate([
    {
        "$lookup": {
            "from": "users",
            "localField": "instructorId",
            "foreignField": "userId",
            "as": "instructor"
        }
    },
    {"$unwind": "$instructor"}
])
print(list(course_with_instructor))

# 3. Get all courses in a specific category
data_science_courses = list(db.courses.find({"category": "Data Science"}))

# 4. Find students enrolled in a particular course
course_id = new_course["courseId"]
student_ids = db.enrollments.find({"courseId": course_id}, {"studentId": 1})
student_ids = [enr["studentId"] for enr in student_ids]
students = list(db.users.find({"userId": {"$in": student_ids}}))

# 5. Search courses by title (case-insensitive, partial match)
search_term = "data"
matched_courses = list(db.courses.find({"title": {"$regex": search_term, "$options": "i"}}))




### Section 3.3: Update Operatiosn
# 1. Update a user's profile information
db.users.update_one(
    {"userId": new_student["userId"]},
    {"$set": {"profile.bio": "Updated bio for student", "profile.skills": ["Python", "MongoDB"]}}
)

# 2. Mark a course as published
db.courses.update_one(
    {"courseId": new_course["courseId"]},
    {"$set": {"isPublished": True, "updatedAt": datetime.utcnow()}}
)

# 3. Update assignment grades
submission = db.submissions.find_one()
db.submissions.update_one(
    {"submissionId": submission["submissionId"]},
    {"$set": {"grade": 85.0, "feedback": "Great work!"}}
)

# 4. Add tags to an existing course
db.courses.update_one(
    {"courseId": new_course["courseId"]},
    {"$addToSet": {"tags": {"$each": ["analysis", "beginner"]}}}
)




## Section 3.3: Delete Operations
# 1. Remove a user (soft delete)
db.users.update_one(
    {"userId": new_student["userId"]},
    {"$set": {"isActive": False}}
)

# 2. Delete an enrollment
db.enrollments.delete_one({"studentId": new_student["userId"], "courseId": new_course["courseId"]})

# 3. Remove a lesson from a course
db.lessons.delete_one({"courseId": new_course["courseId"], "order": 1})


# ### Section 4: Advanced Queries and Aggregation



## Section 4.1 Complex Queries
## 1. Find courses with price between $50 and $200
courses_in_price_range = list(db.courses.find({
    "price": {"$gte": 50, "$lte": 200}
}))

## 2. Get users who joined in the last 6 months
from datetime import timedelta

six_months_ago = datetime.now(timezone.utc) - timedelta(days=6*30)  # approx 6 months
recent_users = list(db.users.find({
    "dateJoined": {"$gte": six_months_ago}
}))

## 3. Find courses that have specific tags using $in operator
tags_to_search = ["python", "data science"]

courses_with_tags = list(db.courses.find({
    "tags": {"$in": tags_to_search}
}))

## 4. Retrieve assignments with due dates in the next week
today = datetime.now(timezone.utc)
next_week = today + timedelta(days=7)

upcoming_assignments = list(db.assignments.find({
    "dueDate": {"$gte": today, "$lte": next_week}
}))




courses_in_price_range




six_months_ago




courses_with_tags




upcoming_assignments




## Section 4.2: Aggregation Pipelines
## 1a. Course Enrollment Statistics
enrollments_per_course = list(db.enrollments.aggregate([
    {
        "$group": {
            "_id": "$courseId",
            "totalEnrollments": {"$sum": 1}
        }
    }
]))
enrollments_per_course




## b. Calculate average course rating
## Updating courses collections to include ratings first


# Fetch all courses
courses = list(db.courses.find({}))

for course in courses:
    rating = round(random.uniform(1, 5), 1)  # e.g., 3.7
    db.courses.update_one(
        {"_id": course["_id"]},
        {"$set": {"rating": rating}}
    )
print("Assigned random ratings to all courses.")




avg_course_rating = list(db.courses.aggregate([
    {
        "$unwind": "$rating"
    },
    {
        "$group": {
            "_id": "$courseId",
            "avgRating": {"$avg": "$rating"}
        }
    }
]))
avg_course_rating




## c. Group by course category with enrollment count
enrollment_by_category = list(db.enrollments.aggregate([
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "courseId",
            "as": "course"
        }
    },
    {"$unwind": "$course"},
    {
        "$group": {
            "_id": "$course.category",
            "totalEnrollments": {"$sum": 1}
        }
    }
]))
enrollment_by_category




##4.3 Student Performance Analysis
#2a. Average grade per student
avg_grade_per_student = list(db.submissions.aggregate([
    {
        "$group": {
            "_id": "$studentId",
            "averageGrade": {"$avg": "$grade"}
        }
    }
]))
avg_grade_per_student




##b. Completion rate by course
completion_rate_by_course = list(db.enrollments.aggregate([
    {
        "$group": {
            "_id": "$courseId",
            "totalEnrolled": {"$sum": 1},
            "completedCount": {
                "$sum": {
                    "$cond": [{"$eq": ["$status", "completed"]}, 1, 0]
                }
            }
        }
    },
    {
        "$project": {
            "completionRate": {
                "$cond": [
                    {"$eq": ["$totalEnrolled", 0]},
                    0,
                    {"$multiply": [{"$divide": ["$completedCount", "$totalEnrolled"]}, 100]}
                ]
            }
        }
    }
]))
completion_rate_by_course




##c. Top-performing students
top_students = list(db.submissions.aggregate([
    {
        "$group": {
            "_id": "$studentId",
            "avgGrade": {"$avg": "$grade"}
        }
    },
    {"$sort": {"avgGrade": -1}},
    {"$limit": 5}
]))
top_students




## 3. Instructor Analytics
## a. Total students taught by each instructor
students_per_instructor = list(db.enrollments.aggregate([
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "courseId",
            "as": "course"
        }
    },
    {"$unwind": "$course"},
    {
        "$group": {
            "_id": "$course.instructorId",
            "uniqueStudents": {"$addToSet": "$studentId"}
        }
    },
    {
        "$project": {
            "totalStudents": {"$size": "$uniqueStudents"}
        }
    }
]))

students_per_instructor




## b. Average course rating per instructor
avg_rating_per_instructor = list(db.courses.aggregate([
    {
        "$unwind": "$rating"
    },
    {
        "$group": {
            "_id": "$instructorId",
            "avgRating": {"$avg": "$rating"}
        }
    }
]))
avg_rating_per_instructor




## c. Revenue generated per instructor
revenue_per_instructor = list(db.enrollments.aggregate([
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "courseId",
            "as": "course"
        }
    },
    {"$unwind": "$course"},
    {
        "$group": {
            "_id": "$course.instructorId",
            "totalRevenue": {"$sum": "$course.price"}
        }
    }
]))
revenue_per_instructor




##4. Advanced Analytics
##a. Monthly enrollment trends (last 12 months)
monthly_enrollments = list(db.enrollments.aggregate([
    {
        "$match": {
            "enrolledAt": {
                "$gte": datetime.now(timezone.utc) - timedelta(days=365)
            }
        }
    },
    {
        "$group": {
            "_id": {
                "year": {"$year": "$enrolledAt"},
                "month": {"$month": "$enrolledAt"}
            },
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"_id.year": 1, "_id.month": 1}}
]))
monthly_enrollments




##b. Most popular course categories (by enrollment count)
popular_categories = list(db.enrollments.aggregate([
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "courseId",
            "as": "course"
        }
    },
    {"$unwind": "$course"},
    {
        "$group": {
            "_id": "$course.category",
            "enrollmentCount": {"$sum": 1}
        }
    },
    {"$sort": {"enrollmentCount": -1}}
]))
popular_categories




##c. Student engagement metrics
avg_progress_per_student = list(db.enrollments.aggregate([
    {
        "$group": {
            "_id": "$studentId",
            "avgProgress": {"$avg": "$progress"}
        }
    }
]))
avg_progress_per_student


# ### Section 5: Indexing and Performance



## a. Creating appropriate indexes
# Index for user email lookup (unique for quick lookup)
db.users.create_index("email", unique=True)

# Indexes for course search by title (text index) and category
db.courses.create_index([("title", "text"), ("category", 1)])

# Index for assignment queries by due date
db.assignments.create_index("dueDate")

# Compound index for enrollment queries by student and course
db.enrollments.create_index([("studentId", 1), ("courseId", 1)])




##  Task 5.2: Query Optimization
import time

# Before: Check performance without index (you’ve already created the index, but let’s simulate it anyway)
start = time.time()
result = db.users.find_one({"email": "student@example.com"})
end = time.time()
print("User lookup time:", end - start)
print("Explain plan:", db.users.find({"email": "student@example.com"}).explain())




# b. Search courses by title (partial match)
start = time.time()
courses = list(db.courses.find({"$text": {"$search": "python"}}))
end = time.time()
print("Course search time:", end - start)
print("Explain plan:", db.courses.find({"$text": {"$search": "python"}}).explain())




#c. Find assignments due within a week
today = datetime.now(timezone.utc)
next_week = today + timedelta(days=7)

start = time.time()
assignments = list(db.assignments.find({
    "dueDate": {"$gte": today, "$lte": next_week}
}))
end = time.time()
print("Upcoming assignment query time:", end - start)
print("Explain plan:", db.assignments.find({
    "dueDate": {"$gte": today, "$lte": next_week}
}).explain())


# ### Section 6: Data Validation and Error Handling



## 6.1 Schema Validation
# Define validation rules for each collection
validation_commands = [
    {
        "collMod": "users",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["userId", "email", "firstName", "lastName", "role"],
                "properties": {
                    "userId": {"bsonType": "string"},
                    "email": {
                        "bsonType": "string",
                        "pattern": "^.+@.+$"
                    },
                    "firstName": {"bsonType": "string"},
                    "lastName": {"bsonType": "string"},
                    "role": {"enum": ["student", "instructor"]},
                    "dateJoined": {"bsonType": "date"},
                    "profile": {
                        "bsonType": "object",
                        "properties": {
                            "bio": {"bsonType": "string"},
                            "avatar": {"bsonType": "string"},
                            "skills": {
                                "bsonType": "array",
                                "items": {"bsonType": "string"}
                            }
                        }
                    },
                    "isActive": {"bsonType": "bool"}
                }
            }
        },
        "validationLevel": "strict"
    },
    {
        "collMod": "courses",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["courseId", "title", "instructorId", "level"],
                "properties": {
                    "courseId": {"bsonType": "string"},
                    "title": {"bsonType": "string"},
                    "description": {"bsonType": "string"},
                    "instructorId": {"bsonType": "string"},
                    "category": {"bsonType": "string"},
                    "level": {"enum": ["beginner", "intermediate", "advanced"]},
                    "duration": {"bsonType": "double"},
                    "price": {"bsonType": "double"},
                    "tags": {
                        "bsonType": "array",
                        "items": {"bsonType": "string"}
                    },
                    "createdAt": {"bsonType": "date"},
                    "updatedAt": {"bsonType": "date"},
                    "isPublished": {"bsonType": "bool"},
                    "rating": {"bsonType": "double"}
                }
            }
        },
        "validationLevel": "strict"
    },
    {
        "collMod": "assignments",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["assignmentId", "courseId", "title", "description", "dueDate"],
                "properties": {
                    "assignmentId": {"bsonType": "string"},
                    "courseId": {"bsonType": "string"},
                    "lessonId": {"bsonType": "string"},
                    "title": {"bsonType": "string"},
                    "description": {"bsonType": "string"},
                    "dueDate": {"bsonType": "date"},
                    "points": {"bsonType": "int"},
                    "createdAt": {"bsonType": "date"}
                }
            }
        },
        "validationLevel": "strict"
    },
    {
        "collMod": "submissions",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["submissionId", "assignmentId", "studentId", "submittedAt"],
                "properties": {
                    "submissionId": {"bsonType": "string"},
                    "assignmentId": {"bsonType": "string"},
                    "studentId": {"bsonType": "string"},
                    "content": {"bsonType": "string"},
                    "grade": {"bsonType": "double"},
                    "feedback": {"bsonType": "string"},
                    "submittedAt": {"bsonType": "date"}
                }
            }
        },
        "validationLevel": "strict"
    },
    {
        "collMod": "enrollments",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["enrollmentId", "studentId", "courseId", "enrolledAt", "status"],
                "properties": {
                    "enrollmentId": {"bsonType": "string"},
                    "studentId": {"bsonType": "string"},
                    "courseId": {"bsonType": "string"},
                    "enrolledAt": {"bsonType": "date"},
                    "status": {
                        "enum": ["active", "completed", "dropped"]
                    },
                    "progress": {
                        "bsonType": "double",
                        "minimum": 0,
                        "maximum": 100
                    }
                }
            }
        },
        "validationLevel": "strict"
    },
    {
        "collMod": "lessons",
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["lessonId", "courseId", "title", "content", "order"],
                "properties": {
                    "lessonId": {"bsonType": "string"},
                    "courseId": {"bsonType": "string"},
                    "title": {"bsonType": "string"},
                    "content": {"bsonType": "string"},
                    "resources": {
                        "bsonType": "array",
                        "items": {"bsonType": "string"}
                    },
                    "order": {"bsonType": "int"},
                    "createdAt": {"bsonType": "date"}
                }
            }
        },
        "validationLevel": "strict"
    }
]

# Apply validation to each collection
for command in validation_commands:
    db.command(command)

print("Validation rules successfully applied to all collections.")




## 6.2 Error Handling
from pymongo import errors


users = db["users"]

# Ensure unique index on userId to trigger duplicate key errors
users.create_index("userId", unique=True)

# Sample user document
valid_user = {
    "userId": "user123",
    "email": "test@example.com",
    "firstName": "Jane",
    "lastName": "Doe",
    "role": "student",
    "dateJoined": datetime.now(),
    "isActive": True
}

# Duplicate userId
duplicate_user = valid_user.copy()

# Invalid data type (dateJoined should be date, not string)
invalid_type_user = valid_user.copy()
invalid_type_user["userId"] = "user124"
invalid_type_user["dateJoined"] = "2025-06-12"  # Wrong type

# Missing required field (email)
missing_field_user = valid_user.copy()
missing_field_user["userId"] = "user125"
del missing_field_user["email"]

# Insert and handle errors
for user in [valid_user, duplicate_user, invalid_type_user, missing_field_user]:
    try:
        users.insert_one(user)
        print(f"✅ Inserted user: {user['userId']}")
    except errors.DuplicateKeyError as e:
        print(f"❌ Duplicate Key Error for userId '{user['userId']}': {e.details['errmsg']}")
    except errors.WriteError as e:
        print(f"❌ Write Error for userId '{user['userId']}': {e.details['errmsg']}")
    except Exception as e:
        print(f"❌ Unexpected Error for userId '{user.get('userId', 'UNKNOWN')}': {str(e)}")




## exporting data to a sample_data.json file"
import json


# Define all your collections
collections = ["users", "courses", "assignments", "submissions", "enrollments", "lessons"]

# Create a dictionary to hold all data
data_export = {}

for col in collections:
    data_export[col] = list(db[col].find({}, {'_id': True}))  # Include ObjectId

# Export to a single JSON file
with open("sample_data.json", "w") as f:
    json.dump(data_export, f, indent=4, default=str)

print("✅ Exported all collections to sample_data.json")




## exporting schema validation

# List of collections to export validation for
collections = ["users", "courses", "assignments", "submissions", "enrollments", "lessons"]

# Dict to hold validation rules
schema_validations = {}

# Get validation rules for each collection
for collection_name in collections:
    options = db.command("listCollections", filter={"name": collection_name})
    if options["ok"] and options["cursor"]["firstBatch"]:
        coll_info = options["cursor"]["firstBatch"][0]
        validator = coll_info.get("options", {}).get("validator")
        if validator:
            schema_validations[collection_name] = validator

# Save to JSON file
with open("schema_validation.json", "w") as f:
    json.dump(schema_validations, f, indent=4)

print("✅ Schema validation exported to schema_validation.json")


# ### Task 1: Design a Data Archiving Strategy for Old Enrollments
# Soft Archiving (Mark as Archived)
# 
# 



# Define cutoff date (1 year ago)
cutoff_date = datetime.now(timezone.utc) - timedelta(days=365)

db.enrollments.update_many(
    {
        "status": {"$in": ["completed", "dropped"]},
        "enrolledAt": {"$lt": cutoff_date}
    },
    {"$set": {"archived": True}}
)


# ### Task 2: Implement Text Search Functionality for Course Content
# Goal: Enable full-text search on fields like course title, description, and lesson content.



def search_courses_by_keyword(db, keyword):
    """
    Searches the 'courses' collection for documents where the keyword appears
    in either the 'title' or 'description' fields (case-insensitive).

    Parameters:
        db (Database): The connected MongoDB database object.
        keyword (str): The keyword to search for.

    Returns:
        list: List of matching course documents.
    """
    query = {
        "$or": [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}}
        ]
    }

    results = list(db.courses.find(query))
    return results




results = search_courses_by_keyword(db, "python")

for course in results:
    print(f"{course['title']} - {course.get('description', 'No description')}")

