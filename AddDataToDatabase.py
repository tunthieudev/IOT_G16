import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://iot-n11-faceattendance-default-rtdb.firebaseio.com/"
})

ref = db.reference("Students")

data = {
    "10001":
        {
            "name": "obama",
            "total_attendance": 1,
            "last_attendance_time": "2022-12-1 00:00:00"
        },
    "10002":
        {
            "name": "trump",
            "total_attendance": 1,
            "last_attendance_time": "2022-12-1 00:00:00"
        },
    "10003":
        {
            "name": "biden",
            "total_attendance": 1,
            "last_attendance_time": "2022-12-1 00:00:00"
        },
    '10004':
        {
            'name': 'tr anh',
            'last_attendance_time': '2023-12-21 16:09:58',
            'total_attendance': 1
        },
}

for key, value in data.items():
    ref.child(key).set(value)
