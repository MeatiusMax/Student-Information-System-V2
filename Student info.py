from tkinter import *                                                                                                                                   #To do List: Make courses like the student, Use previous crud for students and courses,
import tkinter as tk                                                                                                                                    
from tkinter import ttk                                                                                                                                
from tkinter import font
import tkinter.messagebox
import sqlite3
import customtkinter

#========================Main Frame========================================
class sisV2(tk.Tk):#Main window for SISv2, Shows courses first
    #pass
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        Sisframe = tk.Frame(self)
        Sisframe.pack(side="top", fill="both",expand = True )
        Sisframe.rowconfigure(0, weight=1)
        Sisframe.columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Students, Courses):
            frame = F(Sisframe, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show(Courses)
        #pass
    def show(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()
        #pass

#======================================Student Class=========================================================
class Students(tk.Frame):#student class                                                                                                          Note:Use the improve version for the crud here/ Stackoverflow

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Student Information System")
        
        label = tk.Label(self, text="STUDENT REGISTRATION ", font=("Prestige Elite Std", 50), bg="Lightgray")
        label.place(x=200,y=15)
        
        Coursesbutton = customtkinter.CTkButton(self, text="COURSES",text_font=("Nueva Std",18),bd=0, width = 7, command=lambda: controller.show(Courses))
        Coursesbutton.place(x=50,y=35)
        
        Stu_ID = StringVar()
        Stu_Name = StringVar()       
        Stu_YearLevel = StringVar()
        Stu_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()
        
        def tables():
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                        Student_YearLevel TEXT, Student_Gender TEXT, \
                        FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def add_stud():#add student
            if Stu_ID.get() == "" or Stu_Name.get() == "" or Course_Code.get() == "" or Stu_YearLevel.get() == "" or Stu_Gender.get() == "": 
                tkinter.messagebox.showinfo("SIS", "Fill in the box")
            else:  
                ID = Stu_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("SIS", "Invalid ID")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("SIS", "Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("sis_v2.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO students(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Stu_ID.get(),Stu_Name.get(),Course_Code.get(),Stu_YearLevel.get(), Stu_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("SIS", "Student Added")
                                    conn.commit() 
                                    clear()
                                    display_stud()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("sis_v2.db")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM students")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    if ID in ids:
                                       tkinter.messagebox.showerror("SIS", "ID already exists")
                                    else: 
                                       tkinter.messagebox.showerror("SIS", "Course Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("SIS", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("SIS", "Invalid ID")
            #pass     
        def update_stud():
            if Stu_ID.get() == "" or Stu_Name.get() == "" or Course_Code.get() == "" or Stu_YearLevel.get() == "" or Stu_Gender.get() == "": 
                tkinter.messagebox.showinfo("SIS", "Select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("sis_v2.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE students SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Stu_ID.get(),Stu_Name.get(),Course_Code.get(),Stu_YearLevel.get(), Stu_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("SIS", "Updated!")
                    display_stud()
                    clear()
                    conn.close()
            #pass
        def delete_stud():   
            try:
                messageDelete = tkinter.messagebox.askyesno("SIS", "Are you sure you want to remove this Student?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sis_v2.db")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM students WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("SIS", "Deleted!")
                    display_stud()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
            #pass   
        def search_stud():
            Stu_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("sis_v2.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM students")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Stu_ID):
                        self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("SIS", "No ID Found")           
            #pass   
        def display_stud():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
            #pass             
            
        def clear():
            Stu_ID.set('')
            Stu_Name.set('') 
            Stu_YearLevel.set('')
            Stu_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Stu_ID.set(values[0])
            Stu_Name.set(values[1])
            Course_Code.set(values[2])
            Stu_YearLevel.set(values[3])
            Stu_Gender.set(values[4])
        

        self.lblid = tk.Label(self, font=("Roboto Medium", 12), text="ID Number:", padx=5, pady=5,fg="Gray" )
        self.lblid.place(x=200,y=120)
        self.txtid = customtkinter.CTkEntry(self, text_font=("Arial", 13), textvariable=Stu_ID,placeholder_text="YYYY-NNNN", width=300)
        self.txtid.place(x=200,y=150)

        self.lblname = tk.Label(self, font=("Roboto Medium", 12), text="Name:", padx=5, pady=5,fg="Gray" )
        self.lblname.place(x=200,y=180)
        self.txtname = customtkinter.CTkEntry(self, text_font=("Arial", 13), placeholder_text="Sur,First,M.I",textvariable=Stu_Name, width=300)
        self.txtname.place(x=200,y=210)
        
        self.lblc = tk.Label(self, font=("Roboto Medium", 12), text="Course Code:", padx=5, pady=5,fg="Gray" )
        self.lblc.place(x=200,y=240)
        self.txtyear = ttk.Combobox(self, value=["BS STAT", "BS MATH", "BS IT", "BSCS","BSA","BS Bio","BS Chem","BSCE","BSHM","BS Micr","BA Hist","BAPhil","BA PoSc"], state="readonly", font=("Roboto Medium", 12), textvariable=Course_Code, width=28)
        self.txtyear.place(x=200,y=270)
        

        self.lblyear = tk.Label(self, font=("Roboto Medium", 12), text="Year Level:", padx=5, pady=5,fg="Gray")
        self.lblyear.place(x=200,y=300)
        self.txtyear = ttk.Combobox(self, value=["1st Year", "2nd Year", "3rd Year", "4th Year"], state="readonly", font=("Roboto Medium", 13), textvariable=Stu_YearLevel, width=31)
        self.txtyear.place(x=200,y=330)
        
        self.lblgender = tk.Label(self, font=("Roboto Medium", 13), text="Gender:", padx=5, pady=5,fg="Gray")
        self.lblgender.place(x=200,y=360)
        self.txtgender = ttk.Combobox(self, value=["Male", "Female","Other"], font=("Roboto Medium", 13), state="readonly", textvariable=Stu_Gender, width=28)
        self.txtgender.place(x=200,y=390)

        self.SearchBar = customtkinter.CTkEntry(self, text_font=("Roboto Medium", 11), textvariable=SearchBar_Var,placeholder_text="YYYY-NNNN", width=300)
        self.SearchBar.place(x=750,y=100)

        #===============================================Treeview Table=======================================
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1215,y=140,height=390)

        self.studentlist = ttk.Treeview(self, columns=("ID Number", "Name", "Course", "Year Level", "Gender"), height = 18, yscrollcommand=scrollbar.set)

        self.studentlist.heading("ID Number", text="ID Number", anchor=W)
        self.studentlist.heading("Name", text="Name",anchor=W)
        self.studentlist.heading("Course", text="Course",anchor=W)
        self.studentlist.heading("Year Level", text="Year Level",anchor=W)
        self.studentlist.heading("Gender", text="Gender",anchor=W)
        self.studentlist['show'] = 'headings'

        self.studentlist.column("ID Number", width=100, anchor=W, stretch=False)
        self.studentlist.column("Name", width=200, stretch=False)
        self.studentlist.column("Course", width=130, anchor=W, stretch=False)
        self.studentlist.column("Year Level", width=100, anchor=W, stretch=False)
        self.studentlist.column("Gender", width=100, anchor=W, stretch=False)
        
        self.studentlist.bind("<Double-1>",OnDoubleClick)
        
        

        self.studentlist.place(x=575,y=140)
        scrollbar.config(command=self.studentlist.yview)
        
        
        #============================================== Student Buttons =================================================
        
        self.add = customtkinter.CTkButton(self, text="REGISTER", text_font=('Roboto Medium', 11), height=1, width=10, bd=1,command=add_stud)
        self.add.place(x=200,y=450)

        self.update = customtkinter.CTkButton(self, text="UPDATE", text_font=('Roboto Medium', 11), height=1, width=10, bd=1,command=update_stud)
        self.update.place(x=350,y=450)

        self.clear = customtkinter.CTkButton(self, text="CLEAR", text_font=('Roboto Medium', 11), height=1, width=10, bd=1, command=clear)
        self.clear.place(x=200,y=500)

        self.delete = customtkinter.CTkButton(self, text="DELETE", text_font=('Roboto Medium', 11), height=1, width=10, bd=1,command=delete_stud)
        self.delete.place(x=350,y=500)

        self.search = customtkinter.CTkButton(self, text="SEARCH", text_font=('Roboto Medium', 11, 'bold'),bd=0,command=search_stud)
        self.search.place(x=1100,y=100)

        self.display = customtkinter.CTkButton(self, text="DISPLAY", text_font=('Roboto Medium', 11, 'bold'), height=1, width=11,command = display_stud)
        self.display.place(x=575,y=100)

        tables()
        display_stud()
#==========================================Class Courses=======================================================================

class Courses(tk.Frame):#Course class
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Student Information System")
        
        label = tk.Label(self,text="COURSES", font=("Prestige Elite Std", 50),bg="Lightgray")
        label.place(x=230,y=20)
        
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        #pass
        def coursetable():#table for courses
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            #pass

        def add_course():#add course
            if Course_Code.get() == "" or Course_Name.get() == "" : 
                tkinter.messagebox.showinfo("Message", "Entries are empty!")
            else:
                conn = sqlite3.connect("sis_v2.db")
                c = conn.cursor()         
                c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",(Course_Code.get(),Course_Name.get()))        
                conn.commit()           
                conn.close()
                Course_Code.set('')
                Course_Name.set('') 
                tkinter.messagebox.showinfo("Message", "Course Added!")
                display_course()
            #pass

        def display_course():#display
            self.course.delete(*self.course.get_children())
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.course.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
            #pass
        def update_course():#update
            for selected in self.course.selection():
                conn = sqlite3.connect("sis_v2.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", (Course_Code.get(),Course_Name.get(), self.course.set(selected, '#1')))  
                conn.commit()
                tkinter.messagebox.showinfo("Message", "Updated!")
                display_course()
                clear()
                conn.close()
            #pass    
         
        def delete_course(): #delete
            try:
                messageDelete = tkinter.messagebox.askyesno("Message", "Delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sis_v2.db")
                    cur = con.cursor()
                    x = self.course.selection()[0]
                    id_no = self.course.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.course.delete(x)
                    tkinter.messagebox.showinfo("Message", "Deleted!")
                    display_course()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("Message", "This course has students!")
            #pass    

        def search_course():#search
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("sis_v2.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.course.delete(*self.course.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.course.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
            #pass
            
        def clear():#make the entries empty
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):#for double clicking
            item = self.course.selection()[0]
            values = self.course.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])

        #Button to switch to student frame
        StudentButton = customtkinter.CTkButton(self, text="STUDENTS",text_font=("Nueva Std",18),bd=0, width = 10, command=lambda: controller.show(Students))
        StudentButton.place(x=100,y=35)
        
        #Lable,scrollbar and searchbar
        self.lblccode = tk.Label(self, font=("Roboto Medium", 12, "bold"), text="Course Code:", padx=5, pady=5, fg="Gray")
        self.lblccode.place(x=90,y=120)
        self.txtccode = customtkinter.CTkEntry(self, text_font=("Roboto Medium", 13), placeholder_text="BS**",textvariable=Course_Code, width=300)
        self.txtccode.place(x=90,y=150)

        self.lblcname = tk.Label(self, font=("Roboto Medium", 12,"bold"), text="Course Name:", padx=5, pady=5, fg="Gray")
        self.lblcname.place(x=90,y=180)
        self.txtcname = customtkinter.CTkEntry(self, text_font=("Roboto Medium", 13), textvariable=Course_Name,placeholder_text="BS in ********", width=300)
        self.txtcname.place(x=90,y=210)
        
        self.SearchBar = customtkinter.CTkEntry(self, text_font=("Roboto Medium", 11),placeholder_text="Enter Course Code", textvariable=SearchBar_Var,width=300)
        self.SearchBar.place(x=750,y=100)
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1115,y=140,height=390)

        #Treeview
        self.course = ttk.Treeview(self, columns=("Course Code","Course Name"), height = 18, yscrollcommand=scrollbar.set)

        self.course.heading("Course Code", text="Course Code", anchor=W)
        self.course.heading("Course Name", text="Course Name",anchor=W)
        self.course['show'] = 'headings'

        self.course.column("Course Code", width=250, anchor=W, stretch=False)
        self.course.column("Course Name", width=480, stretch=False)
        
        self.course.bind("<Double-1> ", OnDoubleclick)


        self.course.place(x=400,y=140)
        scrollbar.config(command=self.course.yview)
            
        #=======================================Course Button============================

        self.adds = customtkinter.CTkButton(self, text="ADD", text_font=('Roboto Medium', 11, ), height=1, width=10, bd=1, command=add_course)
        self.adds.place(x=180,y=250)

        self.update = customtkinter.CTkButton(self, text="UPDATE", text_font=('Roboto Medium', 11), height=1, width=10, bd=1,command=update_course) 
        self.update.place(x=280,y=250)
       
        self.clear = customtkinter.CTkButton(self, text="CLEAR", text_font=('Roboto Medium', 11), height=1, width=10, bd=1,command=clear)
        self.clear.place(x=180,y=300)

        self.delete = customtkinter.CTkButton(self, text="DELETE", text_font=('Roboto Medium', 11), height=1, width=10, bd=1, command=delete_course)
        self.delete.place(x=280,y=300)

        self.search = customtkinter.CTkButton(self, text="SEARCH", text_font=('Roboto Medium', 11, 'bold'),bd=0, command=search_course)
        self.search.place(x=1100,y=100)

        self.display = customtkinter.CTkButton(self, text="DISPLAY", text_font=('Roboto Medium', 11, 'bold'), height=1, width=11, command=display_course)
        self.display.place(x=500,y=100)
        
        coursetable()
        display_course()


root = sisV2()
root.geometry("1260x600")

root.mainloop()