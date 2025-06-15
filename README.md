
# EduHub MongoDB Project

EduHub is an e-learning platform backend designed with MongoDB and PyMongo to support a robust and scalable architecture for managing users, courses, lessons, assignments, enrollments, and submissions. This project demonstrates end-to-end MongoDB operations including CRUD, aggregation, indexing, schema validation, and performance optimization.

---

## 📁 Project Structure

```
mongodb-eduhub-project/
├── README.md
├── notebooks/
│   └── eduhub_mongodb_project.ipynb
├── src/
│   └── eduhub_queries.py
├── data/
│   ├── sample_data.json
│   └── schema_validation.json
├── docs/
│   ├── performance_analysis.md
│   └── presentation.pptx
└── .gitignore
```

---

## ⚙️ Project Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/mongodb-eduhub-project.git
   cd mongodb-eduhub-project
   ```

2. **Install Required Packages**:
   ```bash
   pip install pymongo pandas faker
   ```

3. **Start MongoDB Server**:
   Ensure that MongoDB is installed and running locally on `mongodb://localhost:27017/`.

4. **Run the Notebook**:
   Open and execute the `notebooks/eduhub_mongodb_project.ipynb` file to walk through data insertion, operations, and analysis.

---

## 🧱 Database Schema Documentation

Schema validation is enforced using MongoDB's `$jsonSchema` validator.

### `users` Collection
- Fields: `userId`, `email`, `firstName`, `lastName`, `role`, `profile`, `isActive`, `dateJoined`
- Enum: `role` → `["student", "instructor"]`
- Validations: email format, required fields, embedded profile object (bio, avatar, skills)

### `courses` Collection
- Fields: `courseId`, `title`, `description`, `instructorId`, `level`, `price`, `tags`, `rating`, `createdAt`
- Enum: `level` → `["beginner", "intermediate", "advanced"]`

### Other Collections:
- **`lessons`**: content, order, course linkage
- **`assignments`**: linked to course/lesson, due date, points
- **`submissions`**: content, grade, feedback
- **`enrollments`**: student-course relation, progress, status

👉 Full schema definitions are available in [`data/schema_validation.json`](data/schema_validation.json)

---

## 🔍 Query Explanations

### ✅ CRUD Operations:
- **Create**: Add users, courses, lessons, enrollments, assignments
- **Read**: Filter by status, category, course title (case-insensitive), join with `$lookup`
- **Update**: Profile info, course publication, grades, tags
- **Delete**: Soft delete users, remove lessons and enrollments

### ⚡ Advanced Queries:
- Price range filtering, recent users, tagged courses
- Upcoming assignments (7-day window)
- Text search using regex and `$options: 'i'`

👉 Detailed examples in [`src/eduhub_queries.py`](src/eduhub_queries.py)

---

## 🚀 Performance Analysis

1. **Indexes Created On**:
   - `users.email`
   - `courses.title`, `courses.category`
   - `assignments.dueDate`
   - `enrollments.studentId`, `enrollments.courseId`

2. **Query Optimization**:
   - Used `.explain("executionStats")` to analyze query plans
   - Indexed fields with frequent lookups or filters
   - Results: Avg query time reduced from ~120ms to ~15ms on filtered data
     
3. **Full-Text Search on Courses**:
```python
db.courses.find({ "$text": { "$search": "machine learning" } })
```
- **Text Index Used**
- **Result:** Relevant matches across title and description in < 1 ms ✅
  
## 🗃️ Data Archiving Strategy

To maintain performance and reduce collection size:

- **Old Records Migration**: Outdated assignments and inactive enrollments are moved to archival collections (e.g., `archived_assignments`, `archived_enrollments`).
- **Archiving Criteria**: Based on timestamps (e.g., completed > 6 months ago).
- **Automation**: Scheduled script runs monthly to offload data.

**Benefits:**
- Keeps active collections lightweight.
- Improves query speed for current data.
- Ensures historical data remains accessible for audits/reports.

👉 Full analysis documented in [`docs/performance_analysis.md`](docs/performance_analysis.md)

---

## ⚠️ Challenges Faced & Solutions

| Challenge | Solution |
|----------|----------|
| Enabling validation without dropping collections | Used `collMod` with `$jsonSchema` to update validators |
| Handling deprecated `utcnow` | Replaced with `datetime.now(timezone.utc)` |
| Exporting all schemas and sample data | Wrote Python scripts to extract and save as JSON |
| Optimizing slow queries | Created compound indexes, avoided `$regex` where possible |

---

## 📦 Sample Data

Sample data is provided for testing and demonstration purposes:
- [`data/sample_data.json`](data/sample_data.json): All documents from each collection
- Automatically generated using `Faker` and custom seed scripts

---

## 🧑‍🏫 Presentation

- A brief walkthrough and demo slides are available in [`docs/presentation.pptx`](docs/presentation.pptx)

---

## 📌 Author

**Osato Osazuwa**  
GitHub: [@yourusername](https://github.com/yourusername)  
Email: osato.osazuwa@gmail.com

---

## 📄 License

This project is licensed for academic and demonstration purposes only.
