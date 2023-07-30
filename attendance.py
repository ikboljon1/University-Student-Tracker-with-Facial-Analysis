# import
import re
from sys import path
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
import os
import mysql.connector
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
import csv
from tkinter import filedialog

#Глобальная переменная для функции importCsv 
mydata=[]
class Attendance:
    
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title("Панель посещаемости")

        #-----------Переменные-------------------
        self.var_id=StringVar()
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_dep=StringVar()
        self.var_time=StringVar()
        self.var_date=StringVar()
        self.var_attend=StringVar()

        # Эта часть является началом настройки меток изображений.
        # первое изображение заголовка 
        img=Image.open(r"C:\Users\ikbol\OneDrive\Рабочий стол\Python-FYP\Python_Test_Projects\Images_GUI\banner.jpg")
        img=img.resize((1366,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        # установить изображение в качестве метки
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # изображение на заднем плане 
        bg1=Image.open(r"Images_GUI\bg2.jpg")
        bg1=bg1.resize((1366,768),Image.ANTIALIAS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # установить изображение в качестве метки
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)


        #раздел заголовка
        title_lb1 = Label(bg_img,text="Добро пожаловать в панель посещаемости",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        #========================Section Creating==================================

        # Создание кадра 
        main_frame = Frame(bg_img,bd=2,bg="white") #bd означает границу 
        main_frame.place(x=5,y=55,width=1355,height=510)

        # Левая рамка этикетки 
        left_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Сведения о студенте",font=("verdana",12,"bold"),fg="navyblue")
        left_frame.place(x=10,y=10,width=660,height=480)

        

        # ==================================Текстовые поля и поля со списком====================

        #Студенческий билет
        studentId_label = Label(left_frame,text="Std-ID:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        studentId_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)

        studentId_entry = ttk.Entry(left_frame,textvariable=self.var_id,width=15,font=("verdana",12,"bold"))
        studentId_entry.grid(row=0,column=1,padx=5,pady=5,sticky=W)

        #Студенческий список
        student_roll_label = Label(left_frame,text="Roll.No:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_roll_label.grid(row=0,column=2,padx=5,pady=5,sticky=W)

        student_roll_entry = ttk.Entry(left_frame,textvariable=self.var_roll,width=15,font=("verdana",12,"bold"))
        student_roll_entry.grid(row=0,column=3,padx=5,pady=5,sticky=W)

        #Имя студента
        student_name_label = Label(left_frame,text="Std-Name:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_name_label.grid(row=1,column=0,padx=5,pady=5,sticky=W)

        student_name_entry = ttk.Entry(left_frame,textvariable=self.var_name,width=15,font=("verdana",12,"bold"))
        student_name_entry.grid(row=1,column=1,padx=5,pady=5,sticky=W)

        #Отделение
        # dep_label = Label(left_frame,text="Department:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        # dep_label.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        # dep_entry = ttk.Entry(left_frame,textvariable=self.var_dep,width=15,font=("verdana",12,"bold"))
        # dep_entry.grid(row=1,column=3,padx=5,pady=5,sticky=W)

        #время
        time_label = Label(left_frame,text="Time:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        time_label.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        time_entry = ttk.Entry(left_frame,textvariable=self.var_time,width=15,font=("verdana",12,"bold"))
        time_entry.grid(row=1,column=3,padx=5,pady=5,sticky=W)

        #Дата
        date_label = Label(left_frame,text="Date:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        date_label.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        date_entry = ttk.Entry(left_frame,textvariable=self.var_date,width=15,font=("verdana",12,"bold"))
        date_entry.grid(row=2,column=1,padx=5,pady=5,sticky=W)

        #Посещаемость
        student_attend_label = Label(left_frame,text="Attend-status:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_attend_label.grid(row=2,column=2,padx=5,pady=5,sticky=W)

        attend_combo=ttk.Combobox(left_frame,textvariable=self.var_attend,width=13,font=("verdana",12,"bold"),state="readonly")
        attend_combo["values"]=("Статус","настоящее время","Отсутствующий")
        attend_combo.current(0)
        attend_combo.grid(row=2,column=3,padx=5,pady=5,sticky=W)

        # ===============================Представление данных таблицы Sql==========================
        table_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=10,y=100,width=635,height=310)

        #полоса прокрутки 
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        #создать таблицу 
        self.attendanceReport_left = ttk.Treeview(table_frame,column=("ID","Roll_No","Name","Time","Date","Attend"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.attendanceReport_left.xview)
        scroll_y.config(command=self.attendanceReport_left.yview)

        self.attendanceReport_left.heading("ID",text="Std-ID")
        self.attendanceReport_left.heading("Roll_No",text="Roll.No")
        self.attendanceReport_left.heading("Name",text="Std-Name")
        self.attendanceReport_left.heading("Time",text="Time")
        self.attendanceReport_left.heading("Date",text="Date")
        self.attendanceReport_left.heading("Attend",text="Attend-status")
        self.attendanceReport_left["show"]="headings"


        # Установить ширину столбцов
        self.attendanceReport_left.column("ID",width=100)
        self.attendanceReport_left.column("Roll_No",width=100)
        self.attendanceReport_left.column("Name",width=100)
        self.attendanceReport_left.column("Time",width=100)
        self.attendanceReport_left.column("Date",width=100)
        self.attendanceReport_left.column("Attend",width=100)
        
        self.attendanceReport_left.pack(fill=BOTH,expand=1)
        self.attendanceReport_left.bind("<ButtonRelease>",self.get_cursor_left)
    

        # =========================секция кнопок========================

        #Рамка кнопки
        btn_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        btn_frame.place(x=10,y=390,width=635,height=60)

        #Кнопка импорта
        save_btn=Button(btn_frame,command=self.importCsv,text="Import CSV",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        save_btn.grid(row=0,column=0,padx=6,pady=10,sticky=W)

        #Кнопка экспорта
        update_btn=Button(btn_frame,command=self.exportCsv,text="Export CSV",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        update_btn.grid(row=0,column=1,padx=6,pady=8,sticky=W)

        #Кнопка обновления
        del_btn=Button(btn_frame,command=self.action,text="Обновить",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        del_btn.grid(row=0,column=2,padx=6,pady=10,sticky=W)

        #кнопка сброса
        reset_btn=Button(btn_frame,command=self.reset_data,text="Перезагрузить",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        reset_btn.grid(row=0,column=3,padx=6,pady=10,sticky=W)



        # Правая часть=======================================================

        # Правая рамка метки 
        right_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Сведения о студенте",font=("verdana",12,"bold"),fg="navyblue")
        right_frame.place(x=680,y=10,width=660,height=480)


        # -----------------------------Table Frame-------------------------------------------------
        #Каркас таблица
        #Система поиска в правой рамке метки
        table_frame = Frame(right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=10,y=90,width=635,height=360)

        #полоса прокрутки
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        #создать таблицу 
        self.attendanceReport = ttk.Treeview(table_frame,column=("ID","Roll_No","Name","Time","Date","Attend"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.attendanceReport.xview)
        scroll_y.config(command=self.attendanceReport.yview)

        self.attendanceReport.heading("ID",text="Std-ID")
        self.attendanceReport.heading("Roll_No",text="Roll.No")
        self.attendanceReport.heading("Name",text="Std-Name")
        self.attendanceReport.heading("Time",text="Time")
        self.attendanceReport.heading("Date",text="Date")
        self.attendanceReport.heading("Attend",text="Attend-status")
        self.attendanceReport["show"]="headings"


        # Установить ширину столбцов
        self.attendanceReport.column("ID",width=100)
        self.attendanceReport.column("Roll_No",width=100)
        self.attendanceReport.column("Name",width=100)
        self.attendanceReport.column("Time",width=100)
        self.attendanceReport.column("Date",width=100)
        self.attendanceReport.column("Attend",width=100)
        
        self.attendanceReport.pack(fill=BOTH,expand=1)
        self.attendanceReport.bind("<ButtonRelease>",self.get_cursor_right)
        self.fetch_data()
    # =================================обновить кнопку mysql================
    #Кнопка обновления
        del_btn=Button(right_frame,command=self.update_data,text="Обновить",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        del_btn.grid(row=0,column=1,padx=6,pady=10,sticky=W)
    #Кнопка обновления
        del_btn=Button(right_frame,command=self.delete_data,text="Удалить",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        del_btn.grid(row=0,column=2,padx=6,pady=10,sticky=W)
    # ===============================функция обновления для базы данных mysql=================
    def update_data(self):
        if self.var_id.get()=="" or self.var_roll.get=="" or self.var_name.get()=="" or self.var_time.get()=="" or self.var_date.get()=="" or self.var_attend.get()=="Status":
            messagebox.showerror("Ошибка","Пожалуйста, заполните все обязательные поля!",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Обновить","Вы хотите обновить эту посещаемость студентов!",parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(username='root', password='Ik507727280',host='localhost',database='face_recognition',port=3306)
                    mycursor = conn.cursor()
                    mycursor.execute("update stdattendance set std_id=%s,std_roll_no=%s,std_name=%s,std_time=%s,std_date=%s,std_attendance=%s where std_id=%s",( 
                    self.var_id.get(),
                    self.var_roll.get(),
                    self.var_name.get(),
                    self.var_time.get(),
                    self.var_date.get(),
                    self.var_attend.get(),
                    self.var_id.get()  
                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Успешно","Успешно обновлено!",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Ошибка",f"Из-за: {str(es)}",parent=self.root)
    # =============================Удалить посещаемость из mysql============================
    def delete_data(self):
        if self.var_id.get()=="":
            messagebox.showerror("Ошибка","Требуется студенческий билет!",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Удалть","Вы хотите удалить?",parent=self.root)
                if delete>0:
                    conn = mysql.connector.connect(username='root', password='Ik507727280',host='localhost',database='face_recognition',port=3306)
                    mycursor = conn.cursor() 
                    sql="delete from stdattendance where std_id=%s"
                    val=(self.var_id.get(),)
                    mycursor.execute(sql,val)
                else:
                    if not delete:
                        return

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Удалить","Успешно удалено!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Ошибка",f"Из-за: {str(es)}",parent=self.root)  
    # ===========================получить данные о посещаемости mysql===========

    def fetch_data(self):
        conn = mysql.connector.connect(username='root', password='Ik507727280',host='localhost',database='face_recognition',port=3306)
        mycursor = conn.cursor()

        mycursor.execute("select * from stdattendance")
        data=mycursor.fetchall()

        if len(data)!= 0:
            self.attendanceReport.delete(*self.attendanceReport.get_children())
            for i in data:
                self.attendanceReport.insert("",END,values=i)
            conn.commit()
        conn.close()

    #============================Сбросить данные======================
    def reset_data(self):
        self.var_id.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attend.set("Status")

    # =========================Получить данные Импортировать данные ===============

    def fetchData(self,rows):
        global mydata
        mydata = rows
        self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
        for i in rows:
            self.attendanceReport_left.insert("",END,values=i)
            print(i)
        

    def importCsv(self):
        mydata.clear()
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
        self.fetchData(mydata)
            

    #==================Экспорт CSV=============
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("Ошибка","Данные не найдены!",parent=self.root)
                return False
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write=csv.writer(myfile,delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Успешно","Экспорт данных успешно!")
        except Exception as es:
                messagebox.showerror("Ошибка",f"Из-за: {str(es)}",parent=self.root)    

    #=============Курсорная функция для CSV========================

    def get_cursor_left(self,event=""):
        cursor_focus = self.attendanceReport_left.focus()
        content = self.attendanceReport_left.item(cursor_focus)
        data = content["values"]

        self.var_id.set(data[0]),
        self.var_roll.set(data[1]),
        self.var_name.set(data[2]),
        self.var_time.set(data[3]),
        self.var_date.set(data[4]),
        self.var_attend.set(data[5])  

     #=============Курсорная функция для mysql========================

    def get_cursor_right(self,event=""):
        cursor_focus = self.attendanceReport.focus()
        content = self.attendanceReport.item(cursor_focus)
        data = content["values"]

        self.var_id.set(data[0]),
        self.var_roll.set(data[1]),
        self.var_name.set(data[2]),
        self.var_time.set(data[3]),
        self.var_date.set(data[4]),
        self.var_attend.set(data[5])    
    #=========================================Обновить CSV-файл============================

    # экспортировать обновление
    def action(self):
        if self.var_id.get()=="" or self.var_roll.get=="" or self.var_name.get()=="" or self.var_time.get()=="" or self.var_date.get()=="" or self.var_attend.get()=="Status":
            messagebox.showerror("Ошибка","Пожалуйста, заполните все обязательные поля!",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(username='root', password='Ik507727280',host='localhost',database='face_recognition',port=3306)
                mycursor = conn.cursor()
                mycursor.execute("insert into stdattendance values(%s,%s,%s,%s,%s,%s)",(
                self.var_id.get(),
                self.var_roll.get(),
                self.var_name.get(),
                self.var_time.get(),
                self.var_date.get(),
                self.var_attend.get()
                ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Успешно","Все записи сохраняются в базе данных!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Ошибка",f"Из-за: {str(es)}",parent=self.root)






    #     conn = mysql.connector.connect(username='root', password='Ik507727280',host='localhost',database='face_recognition',port=3306)
    #     mycursor = conn.cursor()
    #     if messagebox.askyesno("Confirmation","Are you sure you want to save attendance on database?"):
    #         for i in mydata:
    #             uid = i[0]
    #             uroll = i[1]
    #             uname = i[2]
    #             utime = i[3]
    #             udate = i[4]
    #             uattend = i[5]
    #             qury = "INSERT INTO stdattendance(std_id, std_roll_no, std_name, std_time, std_date, std_attendance) VALUES(%s,%s,%s,%s,%s,%s)"
    #             mycursor.execute(qury,(uid,uroll,uname,utime,udate,uattend))
    #         conn.commit()
    #         conn.close()
    #         messagebox.showinfo("Success","Successfully Updated!",parent=self.root)
    #     else:
    #         return False




        # 









if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()