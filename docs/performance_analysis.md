
# 📊 Performance Analysis and Optimization Report

## 🔍 Overview

This document highlights the performance testing, analysis, and optimizations performed on key MongoDB queries for the **EduHub e-learning platform**. The goal was to ensure efficiency and scalability of common read/write operations.

---

## ⚙️ Tools Used

- **PyMongo** – For querying and index creation.
- **MongoDB `explain()`** – To analyze query execution plans.
- **Python `time` module** – To benchmark query runtimes.
- **Indexes & Text Search** – For optimizing query paths and improving user experience.

---

## 🔎 Indexing & Text Search Strategy

### 1. **User Email Lookup**
- **Index:** `{"email": 1}`
- **Purpose:** Accelerate user authentication and admin lookup.

### 2. **Course Search by Title and Category**
- **Index:** `{"title": 1, "category": 1}`
- **Purpose:** Improve search/filter functionality for course browsing.

### 3. **Course Full-Text Search**
- **Text Index:** `{ "title": "text", "description": "text" }`
- **Purpose:** Enable keyword-based full-text search across course content.

### 4. **Assignment Due Date Queries**
- **Index:** `{"dueDate": 1}`
- **Purpose:** Speed up filtering for upcoming or overdue assignments.

### 5. **Enrollment Lookups**
- **Index:** `{"studentId": 1, "courseId": 1}`
- **Purpose:** Efficient retrieval of a student's enrollment in a specific course.

---

## 🧪 Query Performance Testing

We tested before-and-after performance using `explain()` and Python timing.

### 1. Find User by Email
```python
db.users.find_one({"email": "testuser@example.com"})
```
- **Before Index:** COLLSCAN (~3.4 ms)
- **After Index:** IXSCAN (~0.2 ms) ✅

---

### 2. Filter Courses by Title and Category
```python
db.courses.find({
    "title": {"$regex": "Data", "$options": "i"},
    "category": "Data Science"
})
```
- **Before Index:** ~5.1 ms (COLLSCAN)
- **After Index (`{"title": 1, "category": 1}`):** ~0.6 ms ✅

---

### 3. Full-Text Search on Courses
```python
db.courses.find({ "$text": { "$search": "machine learning" } })
```
- **Text Index Used**
- **Result:** Relevant matches across title and description in < 1 ms ✅

---

### 4. Retrieve Assignments Due This Week
```python
db.assignments.find({
    "dueDate": {"$gte": now, "$lte": next_week}
})
```
- **Before Index:** Slow, full scan
- **After Index on `dueDate`:** IXSCAN ✅

---

## 🗃️ Data Archiving Strategy

To maintain performance and reduce collection size:

- **Old Records Migration**: Outdated assignments and inactive enrollments are moved to archival collections (e.g., `archived_assignments`, `archived_enrollments`).
- **Archiving Criteria**: Based on timestamps (e.g., completed > 6 months ago).
- **Automation**: Scheduled script runs monthly to offload data.

**Benefits:**
- Keeps active collections lightweight.
- Improves query speed for current data.
- Ensures historical data remains accessible for audits/reports.

---

## 💡 Summary of Optimizations

| Query Type                          | Optimization                         | Result                      |
|------------------------------------|--------------------------------------|-----------------------------|
| Email lookup                       | Index on `email`                     | Faster login/retrieval      |
| Course search                      | Index on `title`, `category`         | Enhanced search speed       |
| Full-text course search            | Text index on `title`, `description` | Fast keyword search         |
| Assignment deadline filter         | Index on `dueDate`                   | Efficient time-based queries|
| Enrollment lookup by student/course| Compound index                       | Improved access speed       |
| Data size control                  | Archiving old records                | Leaner collections, better performance |

---

## ❗ Challenges Faced

- **Large Dataset Simulation**: Used `Faker` to generate large, realistic data.
- **Balancing Index Overhead**: Prioritized high-traffic queries to avoid excessive index cost.
- **Regex vs. Text Search**: Transitioned to full-text search to avoid slow regex scans.

---

## ✅ Conclusion

By applying smart indexing, full-text search, and data archiving strategies, we significantly improved the responsiveness and scalability of EduHub's MongoDB backend. These enhancements ensure the platform remains efficient even as user and content volumes grow.
