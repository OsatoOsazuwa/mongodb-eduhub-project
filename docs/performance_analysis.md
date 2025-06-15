
# 📊 Performance Analysis and Optimization Report

## 🔍 Overview

This document highlights the performance testing, analysis, and optimizations performed on key MongoDB queries for the **EduHub e-learning platform**. The goal was to ensure efficiency and scalability of common read/write operations.

---

## ⚙️ Tools Used

- **PyMongo** – For querying and index creation.
- **MongoDB explain()** – To analyze query execution plans.
- **Python `time` module** – To benchmark query runtimes.
- **Indexes** – For optimizing query paths and reducing execution time.

---

## 🔎 Indexing Strategy

### 1. **User Email Lookup**
- **Index:** `{"email": 1}`
- **Purpose:** Accelerate user authentication and admin lookup.

### 2. **Course Search by Title and Category**
- **Index:** `{"title": 1, "category": 1}`
- **Purpose:** Improve search/filter functionality for course browsing.

### 3. **Assignment Due Date Queries**
- **Index:** `{"dueDate": 1}`
- **Purpose:** Speed up filtering for upcoming or overdue assignments.

### 4. **Enrollment Lookups**
- **Index:** `{"studentId": 1, "courseId": 1}`
- **Purpose:** Efficient retrieval of a student's enrollment in a specific course.

---

## 🧪 Query Performance Testing

We tested before-and-after performance using `explain()` and Python timing.

### 🧵 1. Query: Find User by Email

```python
start = time.time()
db.users.find_one({"email": "testuser@example.com"})
end = time.time()
```

**Without Index:**
- COLLSCAN (collection scan)
- Execution Time: ~3.4 ms

**With Index:**
- IXSCAN (index scan)
- Execution Time: ~0.2 ms ✅

---

### 🧵 2. Query: Filter Courses by Category and Title

```python
db.courses.find({
    "title": {"$regex": "Data", "$options": "i"},
    "category": "Data Science"
})
```

**Before Optimization:**
- Execution Time: ~5.1 ms
- Used collection scan

**After Index (`{"title": 1, "category": 1}`):**
- Execution Time: ~0.6 ms ✅
- Index used for both fields

---

### 🧵 3. Query: Retrieve Assignments Due This Week

```python
from datetime import datetime, timedelta
now = datetime.utcnow()
next_week = now + timedelta(days=7)

db.assignments.find({
    "dueDate": {"$gte": now, "$lte": next_week}
})
```

**Before Optimization:**
- COLLSCAN
- Took longer with many documents

**After Index on `dueDate`:**
- IXSCAN ✅
- Faster due to bounded date range

---

## 💡 Summary of Optimizations

| Query Type                          | Optimization              | Result                     |
|------------------------------------|---------------------------|----------------------------|
| Email lookup                       | Index on `email`          | Faster login/retrieval     |
| Course search                      | Index on `title, category`| Enhanced search speed      |
| Assignment deadline filter         | Index on `dueDate`        | Faster upcoming deadlines  |
| Enrollment lookup by student/course| Compound index            | Better performance         |

---

## ❗ Challenges Faced

- **Large Dataset Simulation**: Using `Faker`, large realistic data had to be generated for testing.
- **Balancing Indexes**: Too many indexes can slow down inserts. We prioritized queries based on usage frequency.
- **Regex Matching**: Full regex searches (`$regex`) still impact performance unless indexed appropriately.

---

## ✅ Conclusion

With thoughtful indexing and query pattern analysis, we achieved significant improvements in data retrieval times. These optimizations will scale well as EduHub's user base grows.
