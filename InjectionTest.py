import tkinter as tk
import mysql.connector 
from tkinter import *

# connect to mysql  
db = mysql.connector.connect(host="localhost",user="root",passwd="Algonquin",database="SQLInjection")
mycur = db.cursor()


# Select All Useraccount data
def accountInfo():
    my_w = tk.Tk()
    my_w.geometry("580x130") 
    my_w.title("User account information")

    account_res = db.cursor()

    account_res.execute("Select * from useraccount")

    i=0 
    for account in account_res: 
        for j in range(len(account)):
            e = Entry(my_w, width=15) 
            e.grid(row=i, column=j) 
            e.insert(END, account[j])
        i=i+1

# Select All products data
def productInfo():
    pro_w = tk.Tk()
    pro_w.geometry("250x100") 
    pro_w.title("Product")

    mycur.execute("select * from products")

    i=0 
    for products in mycur: 
        for j in range(len(products)):
            e = Entry(pro_w, width=30) 
            e.grid(row=i, column=j) 
            e.insert(END, products[j])
        i=i+1
 
# sign in display
def signIn():
    global root2
    root2 = Toplevel(root)
    root2.title("Sign in")
    root2.geometry("300x300")
    global username_varify
    global password_varify
    Label(root2, text="Sign in", bg="grey", fg="black", font="bold",width=300).pack()
    username_varify = StringVar()
    password_varify = StringVar()
    Label(root2, text="").pack()
    Label(root2, text="Username :", font="bold").pack()
    Entry(root2, textvariable=username_varify).pack()
    Label(root2, text="").pack()
    Label(root2, text="Password :", font="bold").pack()
    Entry(root2, textvariable=password_varify).pack()
    Label(root2, text="").pack()
    Button(root2, text="Sign in", font="bold", command=signIn_varify).pack()
    Label(root2, text="")

# sign in display
def injectionSql():
    global root2
    root2 = Toplevel(root)
    root2.title("Sql Injection test")
    root2.geometry("300x300")
    global username_varify
    global password_varify
    Label(root2, text="Sql Injection test", bg="grey", fg="black", font="bold",width=300).pack()
    username_varify= StringVar()
    password_varify= StringVar()
    Label(root2, text="").pack()
    Label(root2, text="Username :", font="bold").pack()
    Entry(root2, textvariable=username_varify).pack()
    Label(root2, text="").pack()
    Label(root2, text="Password :", font="bold").pack()
    Entry(root2, textvariable=password_varify).pack()
    Label(root2, text="").pack()
    Button(root2, text="Sign in", font="bold", command=injection_sql).pack()
    Label(root2, text="")


def logg_destroy():
    logg.destroy()
    root2.destroy()


def fail_destroy():
    fail.destroy()

# Successed sign in
def signed():
    global logg
    logg = Toplevel(root2)
    logg.title("Welcome")
    logg.geometry("800x100")

    user_varify = username_varify.get()
    sql = "select * from useraccount u where u.username = %s"
    mycur.execute( sql, [(user_varify)])
    results = mycur.fetchall()

    Label(logg, text="Welcome {} ".format(results), font="bold").pack()
    Label(logg, text="").pack()
    Button(logg, text="Sign Out", bg="grey", width=10, height=2, command=logg_destroy).pack()

# failed sign in
def failed():
    global fail
    fail = Toplevel(root2)   
    fail.title("Invalid")
    fail.geometry("200x100")
    Label(fail, text="Sorry,,", fg="red", font="bold").pack()
    Label(fail, text="").pack()
    Button(fail, text="Ok", bg="grey", width=8, height=1, command=fail_destroy).pack()

# check the sign in info with data
def signIn_varify():
    user_varify = username_varify.get()
    pas_varify = password_varify.get()
    sql = "SELECT * FROM useraccount WHERE username = %s and password = %s"
    mycur.execute(sql,[(user_varify),(pas_varify)])
    results = mycur.fetchall()
    if results:
        for i in results:
            signed()
            break
    else:
        failed()

# injection sql
def injection_sql():
    user_varify = username_varify.get()
    pas_varify = password_varify.get()
    # # Enter " or ""=" (both id, password)
    sql = 'SELECT * FROM useraccount WHERE username ="'+ user_varify + ' "AND password = "'+ pas_varify + '"'
    
    # #----------- another sql -------------------------------------------------------
    # # Enter 105; DROP TABLE Products (only id)
    # # ther is an error, but product table is deleted 
    # sql ="SELECT * FROM useraccount WHERE username =" + user_varify 

    mycur.execute(sql)  
    results = mycur.fetchall()
    if results:
        for i in results:
            accountInfo()
            productInfo()
            break
    else:
        failed()

# Recover the data
def rec_products():
    sql = "CREATE TABLE IF NOT EXISTS `SQLInjection`.`products`(`product_name` VARCHAR(60) NOT NULL)ENGINE = InnoDB; "
    mycur.execute(sql)

    sql = "INSERT INTO `SQLInjection`.`products`(`product_name`) VALUES ('Oracle 19C Cracked Key'), ('Unlimited Burger King Coupons'), ('TempleOS Key'),('Bulk Supply of Werthers Original'),('iPhone 14 Pro Max')"
    mycur.execute(sql)

# main display
def main_screen():
    global root
    root = Tk()
    root.title("SQLinjection Test")
    root.geometry("300x350")
    Label(root,text="SQLInjection Test",font="bold",bg="grey",fg="black",width=300).pack()
    Label(root,text="").pack()
    Button(root,text="User Accounts",width="15",height="1",font="bold",command=accountInfo).pack()
    Label(root,text="").pack()
    Button(root,text="Products",width="8",height="1",font="bold",command=productInfo).pack()
    Label(root,text="").pack()
    Button(root,text="Sign in",width="8",height="1",font="bold" , fg = "blue",command=signIn).pack()
    Label(root,text="").pack()
    Button(root,text="SQLInjection",width="15",height="1",font="bold", fg= "red",command=injectionSql).pack()
    Label(root,text="").pack()
    Button(root,text="Recover products",width="15",height="1",font="bold",command=rec_products).pack()
    Label(root,text="").pack()


main_screen()
root.mainloop()