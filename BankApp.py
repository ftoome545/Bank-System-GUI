# here we'll importing the tkinter 
from tkinter import *
import os
from PIL import ImageTk, Image

# Main screen
master = Tk()
master.title('Banking App')

#Functions
def finish_reg():
    name = tem_name.get()
    age = tem_age.get()
    gender = tem_gender.get()
    password = tem_password.get()
    all_accounts = os.listdir()
    
    if name == "" or age == "" or gender == "" or password == "":
        notif.config(fg="red",text="All fields required *")
        return
    
    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red",text="Account already exists")
            return 
        else:
            new_file = open(name,'w')
            new_file.write(name+'\n')
            new_file.write(password+'\n')
            new_file.write(age+'\n')
            new_file.write(gender+'\n')
            new_file.write('0')
            notif.config(fg="green",text="Account has been created")
            
        
def register():
    # Vars
    global tem_name
    global tem_age
    global tem_gender
    global tem_password
    global notif
    tem_name = StringVar()
    tem_age = StringVar()
    tem_gender = StringVar()
    tem_password = StringVar()
    # register_screen
    register_screen = Toplevel(master)
    register_screen.title('Register')
    # Labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(register_screen, text="Name: ", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(register_screen, text="Age: ", font=('Calibri',12)).grid(row=2,sticky=W)
    Label(register_screen, text="Gender: ", font=('Calibri',12)).grid(row=3,sticky=W)
    Label(register_screen, text="Password: ", font=('Calibri',12)).grid(row=4,sticky=W)
    notif = Label(register_screen,font=('Calibri',12))
    notif.grid(row=6,sticky=N,pady=10) #notify the row is 6 because we need it to be under the regiseter button
    # Entry
    Entry(register_screen, textvariable=tem_name).grid(row=1,column=0)
    Entry(register_screen, textvariable=tem_age).grid(row=2,column=0)
    Entry(register_screen, textvariable=tem_gender).grid(row=3,column=0)
    Entry(register_screen, textvariable=tem_password,show="*").grid(row=4,column=0)
    # Button
    Button(register_screen,text='Register',width=15,font=('Calibri',12),command=finish_reg).grid(row=5,sticky=N,pady=10)

def login_session():
    global login_name
    all_accounts = os.listdir()
    login_name = tem_login_name.get()
    login_password = tem_login_password.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name,'r')
            file_data = file.read()
            file_data = file_data.split('\n')
            password = file_data[1]
            #Account Dashboard
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                #Labels
                Label(account_dashboard,text="Account Dashboard",font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
                Label(account_dashboard,text="Welcome "+name,font=('Calibri',12)).grid(row=1,sticky=N,pady=5)
                #Buttons
                Button(account_dashboard,text="Personal Details",font=('Calibri',12),width=30,command=personal_details).grid(row=2,sticky=N,padx=10)
                Button(account_dashboard,text="Deposit",font=('Calibri',12),width=30,command=deposit).grid(row=3,sticky=N,padx=10)
                Button(account_dashboard,text="Withdraw",font=('Calibri',12),width=30,command=withdraw).grid(row=4,sticky=N,padx=10)
                Label(account_dashboard).grid(row=5,sticky=N,pady=10)
                return
            #rom here 
            elif login_password != password:
                login_notif.config(fg="red",text="Password incorrect!!")
            return   
        else:
            login_notif.config(fg="red",text="No account found!!") #untill here I changed not the same to the old code


def deposit():
    #Vars
    global amount
    global deposit_notif
    global current_balance_label
    amount = StringVar()
    file = open(login_name,'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]
    #Deposit Screen
    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')
    #Label
    Label(deposit_screen,text='Deposit',font=('Calibri',12)).grid(row=0,sticky=N,pady=10)#pady it is 10 units of space from top and bottom
    current_balance_label = Label(deposit_screen,text='Currnet Balance: $ '+details_balance,font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(deposit_screen,text='Amount: ',font=('Calibri',12)).grid(row=2,sticky=W)
    deposit_notif = Label(deposit_screen,font=('Calibri',12))
    deposit_notif.grid(row=4,sticky=N,pady=5)
    #Entry
    Entry(deposit_screen,textvariable=amount,font=('Calibri',12)).grid(row=2,column=1,padx=2)
    #Button
    Button(deposit_screen,text='Finish',font=('Calibri',12),width=15,command=finish_deposit).grid(row=3,sticky=W,pady=5,padx=5)
def finish_deposit():
    if amount.get() == "":
        deposit_notif.config(fg='red',text="Amount is required!")
        return
    if float(amount.get()) <=0:
        deposit_notif.config(fg='red',text="Negative currency is not accepted")
        return
    
    file = open(login_name,'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    #now we write the updated balance in the file 
    # and to do that we've to replace the old balance to the new balance
    # by using replace method
    file_data = file_data.replace(current_balance,str(updated_balance))
    #now we've to delete the old value then put the new balance
    file.seek(0)
    file.truncate(0) #becuase we want to start from zero
    file.write(file_data)
    file.close() 
    #and now we've to update the balance label 
    current_balance_label.config(text="Current Balance: $"+str(updated_balance),fg='green')

    deposit_notif.config(text="Balance Updated",fg='green')
def withdraw():
    #Vars
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    withdraw_amount = StringVar()
    file = open(login_name,'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]
    #withdraw Screen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')
    #Label
    Label(withdraw_screen,text='Withdraw',font=('Calibri',12)).grid(row=0,sticky=N,pady=10)#pady it is 10 units of space from top and bottom
    current_balance_label = Label(withdraw_screen,text='Currnet Balance: $ '+details_balance,font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(withdraw_screen,text='Amount: ',font=('Calibri',12)).grid(row=2,sticky=W)
    withdraw_notif = Label(withdraw_screen,font=('Calibri',12))
    withdraw_notif.grid(row=4,sticky=N,pady=5)
    #Entry
    Entry(withdraw_screen,textvariable=withdraw_amount,font=('Calibri',12)).grid(row=2,column=1,padx=2)
    #Button
    Button(withdraw_screen,text='Finish',font=('Calibri',12),width=15,command=finish_withdraw).grid(row=3,sticky=W,pady=5,padx=5)
def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notif.config(fg='red',text="Amount is required!")
        return
    if float(withdraw_amount.get()) <=0:
        withdraw_notif.config(fg='red',text="Negative currency is not accepted")
        return
    
    file = open(login_name,'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())
    #now we write the updated balance in the file 
    # and to do that we've to replace the old balance to the new balance
    # by using replace method
    file_data = file_data.replace(current_balance,str(updated_balance))
    #now we've to delete the old value then put the new balance
    file.seek(0)
    file.truncate(0) #becuase we want to start from zero
    file.write(file_data)
    file.close() 
    #and now we've to update the balance label 
    current_balance_label.config(text="Current Balance: $"+str(updated_balance),fg='green')

    withdraw_notif.config(text="Balance Updated",fg='green')
def personal_details():
    #Vars
    file = open(login_name,'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_name = user_details[0]
    details_age = user_details[2]
    details_gender = user_details[3]
    details_balance = user_details[4]
    #Personal details screen
    personal_details_screen = Toplevel(master)
    personal_details_screen.title("Personal Details")
    #Labels
    Label(personal_details_screen,text="Pesonal Details",font=('Calibri',14),width=30).grid(row=0,sticky=N,pady=10)
    Label(personal_details_screen,text="Name: "+details_name,font=('Calibri',12)).grid(row=1,sticky=W,padx=5,pady=10)
    Label(personal_details_screen,text="Age: "+details_age,font=('Calibri',12)).grid(row=2,sticky=W,padx=5,pady=10)
    Label(personal_details_screen,text="Gender: "+details_gender,font=('Calibri',12)).grid(row=3,sticky=W,padx=5,pady=10)
    Label(personal_details_screen,text="Balance: $ "+details_balance,font=('Calibri',12)).grid(row=4,sticky=W,padx=5,pady=10)
    
def login():
    #Vars
    global tem_login_name
    global tem_login_password
    global login_notif
    global login_screen
    tem_login_name = StringVar()
    tem_login_password = StringVar()
    #Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login')
    #Labels
    Label(login_screen,text="Login to your account",font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(login_screen,text="Username: ",font=('Calibri',12)).grid(row=1,sticky=W)
    Label(login_screen,text="Password: ",font=('Calibri',12)).grid(row=2,sticky=W)
    login_notif = Label(login_screen,font=('Calibri',12))
    login_notif.grid(row=4,sticky=N)
    #Entry
    Entry(login_screen,textvariable=tem_login_name).grid(row=1,column=1,padx=5)
    Entry(login_screen,textvariable=tem_login_password,show='*').grid(row=2,column=1,padx=5)
    #Button
    Button(login_screen,text="Login",width=15,font=('Calibri',12),command=login_session).grid(row=3,sticky=N,padx=5,pady=5)

# Image import 
img = Image.open('secure.png')
img = img.resize((150,150))
img = ImageTk.PhotoImage(img)

# Labels
Label(master, text = "Custom Banking Beta", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
Label(master, text = "The most secure bank you've probably used", font=('Calibri',12)).grid(row=1,sticky=N)
Label(master, image=img).grid(row=2, sticky=N, pady=15)

# Buttons
Button(master, text="Register", font=('Calibri',12),width=20,command=register).grid(row=3,sticky=N)
Button(master, text="Login", font=('Calibri',12),width=20,command=login).grid(row=4,sticky=N,pady=10)

master.mainloop()