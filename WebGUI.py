from flask import Flask, send_file,url_for,render_template,request,redirect,url_for,session,flash
import subprocess
from login import UserDAO, User

from CaptureGUI import *


def run_recognize_program():
    try:
        # Run the program with subprocess
        result = subprocess.run(
            ["python", "RecognizeGUI.py"], check=True, text=True, capture_output=True)

        # Print the output of the program
        print("Program output:")
        print(result.stdout)

        # Print the program's return code
        print(f"Return Code: {result.returncode}")

    except subprocess.CalledProcessError as e:
        # If the program exits with a non-zero return code, print an error message
        print(f"Error: {e}")
        print(f"Error Output: {e.output}")


app = Flask(__name__)
app.secret_key = "pthttm"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('action') == 'captureButton':
        # Handle the button click here (add your Python command)
        print("Button 1 clicked!")
        username = request.form.get('newusername', '')
        userid = request.form.get('newuserid', '')
        capture_square_webcam_image(userid, username)

    if request.method == 'POST' and request.form.get('action') == 'recognizeButton':
        # Handle the button click here (add your Python command)
        print("Button 2 clicked!")
        run_recognize_program()

    return render_template('index.html')

def read_csv_file(file_path):
    data_list = []

    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            data = {
                'id': row['id'],
                'name': row['name'],
                'last_attendance_time': row['last_attendance_time']
            }
            data_list.append(data)

    return data_list


@app.route('/admin')
def admin():
    # Đường dẫn đến file CSV
    csv_file_path = 'templates/thoi_gian.csv'

    # Gọi hàm để đọc dữ liệu từ file CSV
    data_from_csv = read_csv_file(csv_file_path)

    # Truyền dữ liệu vào template 'admin.html'
    return render_template('admin.html', csv_data=data_from_csv)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        userDAO = UserDAO()
        user = userDAO.login(username, password)
        if user:
            # if user.role=='1':
            session["username"] = user.username
            session["role"] = user.role
            if session["role"] == 1:
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("home"))
        else:
            flash("Username or password is wrong", "warning")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)
