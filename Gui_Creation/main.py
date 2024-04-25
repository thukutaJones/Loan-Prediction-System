import os.path
import tkinter as tk
from PIL import Image, ImageTk
import joblib
import pandas as pd
import numpy as np
from tkinter.messagebox import showerror, showinfo
import threading
import sys
import os

gender_option = None
marital_option = None
education_option = None
property_area = None
employed = None
dependencies = None
full_name = None
applicant_income = None
co_applicant_income = None
loan_amount = None
loan_term = None
root = tk.Tk()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def predict_approval():
    gender = {"Male": 1, "Female": 0}
    marital_status = {"Single": 0, "Married": 1}
    education = {"Graduate": 0, "Non-Graduate": 1}
    employment_status = {"Self-Employed": 1, "Employed": 0}
    property_area_status = {"Rural": 0, "Urban": 1, "Semi-Urban": 2}
    dependencies_ = {"No dependencies": 0, "One": 1, "Two": 2, "More than Three": 3}

    try:
        values = [np.log(float(value)) for value in [applicant_income.get() + co_applicant_income.get(),
                                                     applicant_income.get(), loan_amount.get(),
                                                     loan_term.get()]]
    except ValueError:
        showerror("Incorrect Input", "Please make sure you enter\nin correct values")
        return None
    else:
        independent_variables = pd.DataFrame({"Gender": [gender[gender_option.get()], ],
                                              "Married": [marital_status[marital_option.get()], ],
                                              "Dependents": [dependencies_[dependencies.get()], ],
                                              "Education": [education[education_option.get()], ],
                                              "Self_Employed": [employment_status[employed.get()]],
                                              "Credit_History": [1.0, ],
                                              "Property_Area": [property_area_status[property_area.get()], ],
                                              "TotalApplicantIncome_log": [values[0], ],
                                              "ApplicantIncome_log": [values[1], ],
                                              "LoanAmount_log": [values[2], ],
                                              "Loan_Amount_Term_log": [values[3], ]})

        model = joblib.load("loan_prediction_model.pkl")
        prediction = model.predict(independent_variables)
        if prediction[0]:
            showinfo("Loan Approved", "Congratulations!!\nYour loan has been APPROVED")
        else:
            showerror("Loan Declined", "Sorry!!Your loan has been Declined")



def make_prediction():
    thread = threading.Thread(target=predict_approval)
    thread.start()


def second_page(window, current_label):
    if len(full_name.get()) and gender_option.get() in ["Male", "Female"] and \
            marital_option.get() in ["Single", "Married"] and education_option.get() in ["Graduate", "Non-Graduate"] \
            and property_area.get() in ["Rural", "Urban", "Semi-Urban"] and \
            employed.get() in ["Self-Employed", "Employed"]:

        current_label.place_forget()

        global applicant_income
        global co_applicant_income
        global loan_amount
        global loan_term

        applicant_income = tk.StringVar()
        co_applicant_income = tk.StringVar()
        loan_amount = tk.StringVar()
        loan_term = tk.StringVar()

        bg_image = ImageTk.PhotoImage(Image.open(resource_path('loan_apk_bg.jpg')).resize((700, 500)))
        second_label = tk.Label(image=bg_image)
        second_label.image = bg_image
        second_label.place(in_=window, relwidth=1, relheight=1, rely=0, relx=0)

        back_button = tk.Button(second_label, text="Back", bg="#bee0e8", font=("Arial", 13, "italic"), border=0,
                                command=lambda: home(window, second_label))
        back_button.place(in_=second_label, relx=0, rely=0, relheight=0.06, relwidth=0.1)

        fields = ["Applicant's Income", "CoApplicant's Income", "Loan Amount", "Loan Amount Term (days)"]
        variables = [applicant_income, co_applicant_income, loan_amount, loan_term]
        rel_y = 0.2
        rel_x = 0.04

        for variable, field in zip(variables, fields):
            label = tk.Label(text=field, font=("Arial", 15, "italic", "bold"))
            label.place(in_=second_label, relx=rel_x, rely=rel_y)

            label_field = tk.Entry(font=("Arial", 18, "italic"), bg="#bee0e8", border=0, textvariable=variable)
            label_field.place(in_=second_label, relx=rel_x + 0.01, rely=rel_y + 0.05, relheight=0.07, relwidth=0.4)
            rel_y += 0.15

        global dependencies
        dependencies = tk.StringVar()
        dependencies.set(value="No dependencies")

        dependencies_field = tk.OptionMenu(second_label, dependencies,
                                           *["No dependencies", "One", "Two", "More than Three"],
                                           command=None)
        dependencies_field.place(in_=second_label, relx=0.04, rely=0.8, relheight=0.06, relwidth=0.2)

        submit_button = tk.Button(second_label, text="Submit", bg="#bee0e8", font=("Arial", 15, "italic"), border=0,
                                  command=make_prediction)
        submit_button.place(in_=second_label, relx=0.3, rely=0.9, relheight=0.08, relwidth=0.15)
    else:
        showerror("Incomplete Data", "Please fill in all the fields")


def generate_fields(field_1_details, field_2_details, rel_y):
    field_1 = tk.Radiobutton(field_1_details[0], text=field_1_details[1], variable=field_1_details[2],
                             value=field_1_details[1], font=("Arial", 15, "italic"))
    field_1.place(in_=field_1_details[0], relx=field_1_details[3], rely=rel_y)

    field_2 = tk.Radiobutton(field_2_details[0], text=field_2_details[1], variable=field_2_details[2],
                             value=field_2_details[1], font=("Arial", 15, "italic"))
    field_2.place(in_=field_2_details[0], relx=field_2_details[3] + 0.2, rely=rel_y)


def home(window, current_label):
    global gender_option
    global marital_option
    global education_option
    global property_area
    global employed
    global full_name

    try:
        current_label.place_forget()
    except AttributeError:
        ...

    bg_image = ImageTk.PhotoImage(Image.open(resource_path('loan_apk_bg.jpg')).resize((700, 500)))
    bg_label = tk.Label(image=bg_image)
    bg_label.image = bg_image
    bg_label.place(in_=window, relwidth=1, relheight=1, rely=0, relx=0)

    full_name_label = tk.Label(text="Full Name", font=("Arial", 15, "italic", "bold"))
    full_name_label.place(in_=bg_label, relx=0.04, rely=0.2)

    full_name_field = tk.Entry(font=("Arial", 18, "italic"), bg="#bee0e8", border=0, textvariable=full_name)
    full_name_field.place(in_=bg_label, relx=0.04, rely=0.25, relheight=0.07,
                          relwidth=0.3)

    rel_x = 0.04
    rel_y = 0.33

    radio_buttons_details = [(bg_label, "Male", gender_option, rel_x, rel_y),
                             (bg_label, "Female", gender_option, rel_x, rel_y),
                             (bg_label, "Married", marital_option, rel_x, rel_y),
                             (bg_label, "Single", marital_option, rel_x, rel_y),
                             (bg_label, "Graduate", education_option, rel_x, rel_y),
                             (bg_label, "Non-Graduate", education_option, rel_x, rel_y),
                             (bg_label, "Employed", employed, rel_x, rel_y),
                             (bg_label, "Self-Employed", employed, rel_x, rel_y),
                             (bg_label, "Urban", property_area, rel_x, rel_y),
                             (bg_label, "Rural", property_area, rel_x, rel_y)]

    for index in range(0, len(radio_buttons_details), 2):
        generate_fields(radio_buttons_details[index], radio_buttons_details[index + 1], rel_y)
        rel_y += 0.1
    sem_urban = tk.Radiobutton(bg_label, text="Semi-Urban", variable=property_area,
                               value="Semi-Urban", font=("Arial", 15, "italic"))
    sem_urban.place(in_=bg_label, relx=rel_x + 0.32, rely=0.73)

    next_button = tk.Button(bg_label, text="Next", bg="#bee0e8", font=("Arial", 15, "italic"), border=0,
                            command=lambda: second_page(window, bg_label))
    next_button.place(in_=bg_label, relx=0.32, rely=0.85, relheight=0.08, relwidth=0.15)


def main():
    root.destroy()
    window = tk.Tk()
    window.iconbitmap(resource_path("icon.ico"))
    global gender_option
    gender_option = tk.StringVar(value=str(0))

    global marital_option
    marital_option = tk.StringVar(value=str(0))

    global education_option
    education_option = tk.StringVar(value=str(0))

    global property_area
    property_area = tk.StringVar(value=str(0))

    global employed
    employed = tk.StringVar(value=str(0))

    global full_name
    full_name = tk.StringVar(value=str(""))

    window.title("Loan Approval Prediction System")
    window.configure(bg="white")

    window.geometry("700x500")
    window.resizable(False, False)
    home(window, None)
    window.mainloop()


if __name__ == '__main__':
    root.configure(bg="white")
    root.iconbitmap(resource_path("icon.ico"))
    root.title("Loan Approval Prediction System")
    root.geometry("700x500")
    image = ImageTk.PhotoImage(Image.open("preview.png").resize((200, 200)))
    preview_label = tk.Label(image=image)
    preview_label.image = image
    preview_label.place(in_=root, relwidth=1, relheight=1.3, rely=-0.3)
    title_label = tk.Label(text="LOAN APPROVAL PREDICTION", font=("Arial Black", 20, "italic", "bold"))
    title_label.place(in_=preview_label, relx=0.2, rely=0.66)
    dev_label = tk.Label(text="Developed by: Jones Thukuta", font=("Arial", 10, "italic"))
    dev_label.place(in_=preview_label, relx=0.65, rely=0.91)
    lec_label = tk.Label(text="Lecturer: Mr. Rueben C. Moyo", font=("Arial", 13, "italic", "bold"))
    lec_label.place(in_=preview_label, relx=0.65, rely=0.95)
    root.after(3000, main)
    root.mainloop()
