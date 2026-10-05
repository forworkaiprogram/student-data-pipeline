"""setup_mongodb.py — تجهيز MongoDB بالبيانات."""
from pymongo import MongoClient


def seed_mongodb():
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    db = client['students_db']
    collection = db['student_activities']

    collection.delete_many({})

    activities = [
        {"student_id": 1001, "clubs": ["Robotics"], "library_visits": 12,
         "participation_score": 85, "behavior": "Excellent", "scholarship": False},
        {"student_id": 1002, "clubs": ["AI Club", "Debate"], "library_visits": 25,
         "participation_score": 95, "behavior": "Excellent", "scholarship": True},
        {"student_id": 1003, "clubs": ["Sports"], "library_visits": 5,
         "participation_score": 70, "behavior": "Good", "scholarship": False},
        {"student_id": 1004, "clubs": ["Art", "Reading"], "library_visits": 18,
         "participation_score": 82, "behavior": "Very Good", "scholarship": False},
        {"student_id": 1005, "clubs": [], "library_visits": 2,
         "participation_score": 55, "behavior": "Average", "scholarship": False},
        {"student_id": 1006, "clubs": ["AI Club", "Robotics"], "library_visits": 30,
         "participation_score": 98, "behavior": "Excellent", "scholarship": True},
        {"student_id": 1008, "clubs": ["Sports"], "library_visits": 4,
         "participation_score": 60, "behavior": "Good", "scholarship": False},
        {"student_id": 1010, "clubs": ["Cybersecurity Club"], "library_visits": 15,
         "participation_score": 88, "behavior": "Very Good", "scholarship": False},
        {"student_id": 1011, "clubs": ["Reading"], "library_visits": 20,
         "participation_score": 90, "behavior": "Excellent", "scholarship": False},
        {"student_id": 1012, "clubs": ["Sports"], "library_visits": 3,
         "participation_score": 50, "behavior": "Average", "scholarship": False},
        {"student_id": 1013, "clubs": ["Robotics", "Math"], "library_visits": 10,
         "participation_score": 80, "behavior": "Very Good", "scholarship": False},
        {"student_id": 1014, "clubs": ["AI Club"], "library_visits": 22,
         "participation_score": 92, "behavior": "Excellent", "scholarship": True},
        {"student_id": 1015, "clubs": ["Sports"], "library_visits": 6,
         "participation_score": 75, "behavior": "Good", "scholarship": False},
        {"student_id": 1016, "clubs": ["Reading", "Debate"], "library_visits": 16,
         "participation_score": 87, "behavior": "Very Good", "scholarship": False},
        {"student_id": 1017, "clubs": ["Math Club", "Robotics"], "library_visits": 28,
         "participation_score": 96, "behavior": "Excellent", "scholarship": True},
        {"student_id": 1018, "clubs": ["Art"], "library_visits": 11,
         "participation_score": 78, "behavior": "Good", "scholarship": False},
        {"student_id": 1019, "clubs": [], "library_visits": 1,
         "participation_score": 45, "behavior": "Average", "scholarship": False},
        {"student_id": 1020, "clubs": ["AI Club", "Reading"], "library_visits": 19,
         "participation_score": 91, "behavior": "Excellent", "scholarship": False},
    ]

    collection.insert_many(activities)
    print(f"✅ Inserted {len(activities)} records into MongoDB")
    client.close()


if __name__ == '__main__':
    seed_mongodb()