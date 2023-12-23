import cv2
import time
from tkinter import *
from datetime import datetime
import subprocess


def run_program(program_path):
    try:
        # Run the program with subprocess
        result = subprocess.run(
            ["python", program_path], check=True, text=True, capture_output=True)

        # Print the output of the program
        print("Program output:")
        print(result.stdout)

        # Print the program's return code
        print(f"Return Code: {result.returncode}")

    except subprocess.CalledProcessError as e:
        # If the program exits with a non-zero return code, print an error message
        print(f"Error: {e}")
        print(f"Error Output: {e.output}")


def save_image():
    saveImageBox = Toplevel(root)
    saveImageBox.geometry("400x300")
    saveImageBox.title("Save User")

    id_var = StringVar()
    id_label = Label(saveImageBox, text='ID', font=('calibre', 10, 'bold'))
    id_entry = Entry(saveImageBox, textvariable=id_var,
                     font=('calibre', 10, 'normal'))
    id_label.grid(row=0, column=0)
    id_entry.grid(row=0, column=1)

    name_var = StringVar()
    name_label = Label(saveImageBox, text='Username',
                       font=('calibre', 10, 'bold'))
    name_entry = Entry(saveImageBox, textvariable=name_var,
                       font=('calibre', 10, 'normal'))
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)

    sub_btn = Button(saveImageBox, text='Submit',
                     command=lambda: submit(id_var, name_var, saveImageBox))
    sub_btn.grid(row=2, column=1)

    saveImageBox.mainloop()


def submit(id_var, name_var, saveImageBox):
    data = {}

    id = id_var.get()
    data[id] = {}

    name = name_var.get()
    data[id]["name"] = name

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data[id]["last_attendance_time"] = formatted_datetime

    data[id]["total_attendance"] = 1

    print(data)
    name_var.set("")
    saveImageBox.destroy()


def capture_square_webcam_image():

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        global checkSaveImage
        checkSaveImage = False
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Get the dimensions of the frame
        height, width, _ = frame.shape

        # Calculate the coordinates to crop a square from the center
        size = min(height, width)
        start_x = (width - size) // 2
        start_y = (height - size) // 2

        # Crop the frame to a square
        square_frame = frame[start_y:start_y+size, start_x:start_x+size]

        # Resize the frame for display (optional)
        display_frame = cv2.resize(square_frame, (500, 500))

        # Display the frame
        cv2.imshow("Webcam", display_frame)

        # Check for key presses
        key = cv2.waitKey(1)

        # Break the loop if the escape key is pressed
        if key == 27:  # 27 is the ASCII code for the escape key
            break

        # Capture and save the image if the space key is pressed
        elif key == 32:  # 32 is the ASCII code for the space key
            square_frame = cv2.resize(square_frame, (216, 216))
            cv2.imwrite("captured_image.png", square_frame)
            print("Image captured!")
            checkSaveImage = True
            break

    # Release the webcam and close the window
    cap.release()
    time.sleep(2)
    cv2.destroyAllWindows()
    if (checkSaveImage == True):
        save_image()


if __name__ == "__main__":
    program_path = "main.py"
    # capture_square_webcam_image()
    root = Tk()
    captureButton = Button(root, text="Capture image",
                           command=capture_square_webcam_image)
    captureButton.place(x=0, y=0)
    recognizeButton = Button(root, text="Recognize",
                             command=lambda: run_program(program_path))
    recognizeButton.place(x=0, y=30)
    root.mainloop()
