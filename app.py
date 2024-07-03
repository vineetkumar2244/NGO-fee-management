import tkinter as tk
from tkinter import messagebox, ttk

import json
import os

# File to store student data
DATA_FILE = 'students.json'

# Load data from file
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Add a student
def add_student(name, roll_number, fee_amount, date_of_birth, parents_names, address, disability_type):
    data = load_data()
    data.append({
        'name': name,
        'roll_number': roll_number,
        'fee_amount': fee_amount,
        'date_of_birth': date_of_birth,
        'parents_names': parents_names,
        'address': address,
        'disability_type': disability_type,
        'fees_paid': {}
    })
    save_data(data)
    messagebox.showinfo("Success", f"Student {name} added successfully.")

# Delete a student
def delete_student(roll_number, delete_window):
    data = load_data()
    data = [student for student in data if student['roll_number'] != roll_number]
    save_data(data)
    messagebox.showinfo("Success", f"Student with roll number {roll_number} deleted successfully.")
    # Refresh the delete window after deletion
    delete_window.destroy()
    delete_student_ui()

# Pay fee
def pay_fee():
    pay_fee_window = tk.Toplevel(root)
    pay_fee_window.title("Pay Fee")
    pay_fee_window.geometry('1200x900')  # Adjusted size
    pay_fee_window.configure(bg='#f0f0f0')

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    label_month = tk.Label(pay_fee_window, text="Month:", font=('Arial', 12), bg='#f0f0f0')
    label_month.pack(pady=5)
    combo_month = ttk.Combobox(pay_fee_window, values=months, font=('Arial', 12))
    combo_month.pack()

    label_year = tk.Label(pay_fee_window, text="Year:", font=('Arial', 12), bg='#f0f0f0')
    label_year.pack(pady=5)
    entry_year = tk.Entry(pay_fee_window, font=('Arial', 12))
    entry_year.pack()

    def mark_fee_paid(roll_number):
        data = load_data()
        month = combo_month.get()
        year = entry_year.get()
        date = f"{month}-{year}"

        for student in data:
            if student['roll_number'] == roll_number:
                if date not in student['fees_paid']:
                    student['fees_paid'][date] = True
                    save_data(data)
                    messagebox.showinfo("Success", f"Fee for {student['name']} marked as paid.")
                    # Update UI to reflect changes
                    show_students_with_due_fees()
                    break
                else:
                    messagebox.showinfo("Info", f"Fee for {student['name']} is already paid for {date}.")
                    break

    def show_students_with_due_fees():
        month = combo_month.get()
        year = entry_year.get()
        if not month or not year:
            messagebox.showerror("Error", "Please select both month and enter year.")
            return
        
        data = load_data()
        students_with_due_fees = [student for student in data if not student['fees_paid'].get(f"{month}-{year}")]

        # Clear previous list if exists
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if not students_with_due_fees:
            label_no_records = tk.Label(scrollable_frame, text="No records left to mark as paid.", font=('Arial', 12), bg='#f0f0f0')
            label_no_records.pack(pady=10)
        else:
            label_students = tk.Label(scrollable_frame, text="Students with due fees:", font=('Arial', 14, 'bold'), bg='#f0f0f0')
            label_students.pack(pady=10)

            for student in students_with_due_fees:
                frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
                frame.pack(fill='x', padx=5, pady=5)
                
                label_name = tk.Label(frame, text=f"Name: {student['name']}", font=('Arial', 12), bg='#f0f0f0')
                label_name.pack(side='left', padx=10)

                label_roll_number = tk.Label(frame, text=f"Roll Number: {student['roll_number']}", font=('Arial', 12), bg='#f0f0f0')
                label_roll_number.pack(side='left', padx=10)

                label_fee_amount = tk.Label(frame, text=f"Fee Amount: {student['fee_amount']}", font=('Arial', 12), bg='#f0f0f0')
                label_fee_amount.pack(side='left', padx=10)

                label_parent_names = tk.Label(frame, text=f"Parent's Names: {student['parents_names']}", font=('Arial', 12), bg='#f0f0f0')
                label_parent_names.pack(side='left', padx=10)

                label_disability_type = tk.Label(frame, text=f"Disability Type: {student['disability_type']}", font=('Arial', 12), bg='#f0f0f0')
                label_disability_type.pack(side='left', padx=10)
                
                button = tk.Button(frame, text="Mark as Paid", command=lambda roll_number=student['roll_number']: mark_fee_paid(student['roll_number']), bg='#66b3ff', fg='white', font=('Arial', 10, 'bold'))
                button.pack(side='right')

    button_show_students = tk.Button(pay_fee_window, text="Show Students", command=show_students_with_due_fees, bg='#66b3ff', fg='white', font=('Arial', 12, 'bold'))
    button_show_students.pack(pady=10)

    # Scrollbar for student list
    canvas = tk.Canvas(pay_fee_window, bg='#f0f0f0')
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar = ttk.Scrollbar(pay_fee_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

# Total fee collected in a month
def total_fee_collected(month, year):
    data = load_data()
    total = sum(student['fee_amount'] for student in data if student['fees_paid'].get(f"{month}-{year}"))
    messagebox.showinfo("Total Fee Collected", f"Total fee collected in {month}-{year}: {total}")

def total_fee_collected_ui():
    total_fee_entry_window = tk.Toplevel(root)
    total_fee_entry_window.title("Total Fee Collected")
    total_fee_entry_window.geometry('600x450')  # Adjusted size
    total_fee_entry_window.configure(bg='#f0f0f0')

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    label_month = tk.Label(total_fee_entry_window, text="Month:", font=('Arial', 12), bg='#f0f0f0')
    label_month.pack(pady=5)
    combo_month = ttk.Combobox(total_fee_entry_window, values=months, font=('Arial', 12))
    combo_month.pack()

    label_year = tk.Label(total_fee_entry_window, text="Year:", font=('Arial', 12), bg='#f0f0f0')
    label_year.pack(pady=5)
    entry_year = tk.Entry(total_fee_entry_window, font=('Arial', 12))
    entry_year.pack()

    def total_fee_command():
        month = combo_month.get()
        year = entry_year.get()
        total_fee_collected(month, year)
        total_fee_entry_window.destroy()

    button = tk.Button(total_fee_entry_window, text="Total Fee Collected", command=total_fee_command, bg='#66b3ff', fg='white', font=('Arial', 12, 'bold'))
    button.pack(pady=10)

# Add Student UI
def add_student_ui():
    add_student_window = tk.Toplevel(root)
    add_student_window.title("Add Student")
    add_student_window.geometry('600x600')  # Adjusted size
    add_student_window.configure(bg='#f0f0f0')

    label_name = tk.Label(add_student_window, text="Name:", font=('Arial', 12), bg='#f0f0f0')
    label_name.pack(pady=5)
    entry_name = tk.Entry(add_student_window, font=('Arial', 12))
    entry_name.pack()

    label_roll = tk.Label(add_student_window, text="Roll Number:", font=('Arial', 12), bg='#f0f0f0')
    label_roll.pack(pady=5)
    entry_roll = tk.Entry(add_student_window, font=('Arial', 12))
    entry_roll.pack()

    label_fee = tk.Label(add_student_window, text="Fee Amount:", font=('Arial', 12), bg='#f0f0f0')
    label_fee.pack(pady=5)
    entry_fee = tk.Entry(add_student_window, font=('Arial', 12))
    entry_fee.pack()

    label_dob = tk.Label(add_student_window, text="Date of Birth:", font=('Arial', 12), bg='#f0f0f0')
    label_dob.pack(pady=5)
    entry_dob = tk.Entry(add_student_window, font=('Arial', 12))
    entry_dob.pack()

    label_parents = tk.Label(add_student_window, text="Parents' Names:", font=('Arial', 12), bg='#f0f0f0')
    label_parents.pack(pady=5)
    entry_parents = tk.Entry(add_student_window, font=('Arial', 12))
    entry_parents.pack()

    label_address = tk.Label(add_student_window, text="Address:", font=('Arial', 12), bg='#f0f0f0')
    label_address.pack(pady=5)
    entry_address = tk.Entry(add_student_window, font=('Arial', 12))
    entry_address.pack()

    label_disability = tk.Label(add_student_window, text="Disability Type:", font=('Arial', 12), bg='#f0f0f0')
    label_disability.pack(pady=5)
    entry_disability = tk.Entry(add_student_window, font=('Arial', 12))
    entry_disability.pack()

    def add_student_command():
        name = entry_name.get()
        roll_number = entry_roll.get()
        fee_amount = float(entry_fee.get())
        date_of_birth = entry_dob.get()
        parents_names = entry_parents.get()
        address = entry_address.get()
        disability_type = entry_disability.get()
        add_student(name, roll_number, fee_amount, date_of_birth, parents_names, address, disability_type)
        add_student_window.destroy()

    button = tk.Button(add_student_window, text="Add Student", command=add_student_command, bg='#66b3ff', fg='white', font=('Arial', 12, 'bold'))
    button.pack(pady=10)

# Delete Student UI
def delete_student_ui():
    data = load_data()
    delete_student_window = tk.Toplevel(root)
    delete_student_window.title("Delete Student")
    delete_student_window.geometry('900x600')  # Adjusted size
    delete_student_window.configure(bg='#f0f0f0')

    # Create a canvas widget
    canvas = tk.Canvas(delete_student_window, bg='#f0f0f0')
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a frame inside the canvas for scrollable content
    scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
    scrollable_frame.pack(fill='both', expand=True)

    # Add scrollbar to the right of the canvas
    scrollbar = ttk.Scrollbar(delete_student_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    # Bind mouse wheel event to the canvas
    canvas.bind_all('<MouseWheel>', on_mousewheel)

    for student in sorted(data, key=lambda x: x['roll_number']):
        frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        frame.pack(fill='x', padx=5, pady=5)

        label_name = tk.Label(frame, text=f"Name: {student['name']}, Roll Number: {student['roll_number']}", font=('Arial', 12), bg='#f0f0f0')
        label_name.pack(side='left', padx=10)

        button = tk.Button(frame, text="Delete", command=lambda roll_number=student['roll_number']: delete_student(roll_number, delete_student_window), bg='#ff6666', fg='white', font=('Arial', 10, 'bold'))
        button.pack(side='right')

    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    scrollable_frame.bind('<Configure>', configure_scroll_region)

    def destroy_scrollable_frame(event):
        canvas.unbind_all('<MouseWheel>')
        delete_student_window.destroy()

    delete_student_window.bind('<Destroy>', destroy_scrollable_frame)

# Main UI
root = tk.Tk()
root.title("Student Fee Management")
root.geometry('1200x900')  # Adjusted size
root.configure(bg='#f0f0f0')

# Organization Name and Logo
org_name = "GARDEN REACH INSTITUTE FOR THE REHABILITATION AND RESEARCH"
label_org_name = tk.Label(root, text=org_name, font=('Arial', 20, 'bold'), bg='#f0f0f0')
label_org_name.pack(pady=10)

try:
    logo_image = tk.PhotoImage(file='logo.gif')  # Adjust path based on your actual directory structure
    label_logo = tk.Label(root, image=logo_image, bg='#f0f0f0')
    label_logo.pack()
except tk.TclError:
    print("Logo image file not found.")

label_title = tk.Label(root, text="Student Fee Management System", font=('Arial', 16, 'bold'), bg='#f0f0f0')
label_title.pack(pady=20)

button_add = tk.Button(root, text="Add Student", command=add_student_ui, bg='#66b3ff', fg='white', font=('Arial', 12, 'bold'))
button_add.pack(pady=10)

button_delete = tk.Button(root, text="Delete Student", command=delete_student_ui, bg='#ff6666', fg='white', font=('Arial', 12, 'bold'))
button_delete.pack(pady=10)

button_pay_fee = tk.Button(root, text="Pay Fee", command=pay_fee, bg='#66b3ff', fg='white', font=('Arial', 12, 'bold'))
button_pay_fee.pack(pady=10)

button_total_fee = tk.Button(root, text="Total Fee Collected", command=total_fee_collected_ui, bg='#66b3ff', fg='white', font=('Arial', 12, 'bold'))
button_total_fee.pack(pady=10)

root.mainloop()
