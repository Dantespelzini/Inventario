# INVENTORY by srdantespelzini using python and sqlite3

# MODULES

import sqlite3 # DATABASE
import os      # OS
from time import localtime, strftime

database = "database.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()
isdatabase = os.getcwd()
finduser = ("SELECT * FROM `admin` WHERE `password` = ?")
retry = str



def SetupDatabase():
    if not os.path.isfile(isdatabase + "/database.db"):
        f = open(database,"w")
        f.close
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (password TEXT PRIMARY KEY NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `products` (name_product TEXT PRIMARY KEY NOT NULL, price_product INTEGER, stock_product INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `sells` (sell_time TEXT PRIMARY KEY NOT NULL, sell_product TEXT , sell_qty INTEGER, sell_price INTEGER, sell_type TEXT, sell_total INTEGER) ")

def SetAdminPassword():  
    cursor.execute("SELECT * FROM `admin` WHERE `password`")
    print(cursor.fetchone())
    if cursor.fetchone() == None:
        while True:
            password = input("Ingrese una nueva contraseña para el usuario: ")
            passwordre = input ("Ingrese denuevo la contraseña: ")
            if password == passwordre:
                break
        cursor.execute("INSERT INTO `admin` (password) VALUES (?)",[(passwordre)])
        conn.commit()
    input("algo")

def Loginadmin():

    while False:
        password = input("Ingrese la contraseña: ")
        cursor.execute(finduser,[(password)])
        results = cursor.fetchall

        if not results:
            True
            print("Contraseña incorrecta")
            while retry.lower() != "y" or retry.lower() != "n":
                retry = input("Desea reintentar? s/n :")
                if retry.lower() == "n":
                    break
        else: False

# MENU 

def menu():
    while True:
        os.system("clear")
        print(" 1. Ventas \n 2. Productos y Stock \n 0. Salir")
        operation = input("\n Ingrese el numero de la operacion deseada: ")
        if operation == "1":
            sellsmenu()
        elif operation == "2":
            os.system("clear")
            productmenu()
        elif operation == "0":
            os.system("clear")
            menu()

def sellsmenu():
    while True:
        print(" 1. Ingresar una venta \n 2. Ver informe de ventas \n 3. Vaciar el informe de ventas \n 0. Atras")
        operation = input("\n Ingrese el numero de la operacion deseada: ")
        os.system("clear")
        if operation == "1":
            os.system("clear")
            newsell()
        elif operation == 2:
            os.system("clear")
            sellinfo()
        elif operation == 3:
            os.system("clear")
            clearsells()
        elif operation == 0:
            menu()

def newsell():
    #sell_time TEXT, sell_product TEXT PRIMARY KEY NOT NULL, sell_qty INTEGER, sell_price INTEGER, sell_type TEXT, sell_totalattime
    selltime = strftime("%d-%m-%Y %H:%M:%S", localtime())
    productname = input("nombre del producto vendido")
    sellquantity = input("cantidad vendida")
    selltype = input("efectivo tarjeta de credito o debito")
    sellprice = (cursor.execute("SELECT price_product FROM `products` WHERE name_product = ? ", [productname] ),
    (cursor.fetchall()))
    print(sellprice[1][0][0])
    cursor.execute("INSERT INTO `sells` (sell_time, sell_product, sell_qty, sell_price, sell_type, sell_total) VALUES (?, ?, ?, (SELECT price_product FROM `products` WHERE name_product = ? ), ?, ?)", [selltime, productname, sellquantity, productname, selltype, (sellquantity * sellprice[1][0][0] ) ])
    conn.commit()

def productmenu(): 
    while True:
        os.system("clear")
        print(" 1. Agregar producto \n 2. Eliminar producto \n 3. Agregar al stock \n 4. Eliminar del stock \n 5. Ver productos y stock \n 0. Atras")
        operation = input("\n Ingrese el numero de la operacion deseada: ")
        os.system("clear")
        if operation == "1":
            os.system("clear")
            newproduct()
        elif operation == "2":
            os.system("clear")
            delproduct()
        elif operation == "3":
            os.system("clear")
            newstock()
        elif operation == "4":
            os.system("clear")
            delstock()
        elif operation == "5":
            os.system("clear")
            viewstock()
        elif operation == "0":
            menu()

def newproduct():
    nameproduct = input("ingrese el nombre: ")
    priceproduct =input("ingrese el precio: ")
    stockproduct = input("ingrese la cantidad: ")
    os.system("clear")
    cursor.execute("INSERT INTO `products` (name_product, price_product, stock_product) VALUES (?, ?, ?)", [nameproduct, priceproduct, stockproduct])
    conn.commit()
    menu()

def viewstock():
    os.system("clear")
    cursor.execute("SELECT * FROM `products` ORDER BY `name_product`")
    productlist = cursor.fetchall()
    i=0
    while i < len(productlist):
        print(productlist[i][0]," "* (20 - len(str(productlist[i][0]))), productlist[i][1]," "* (20 - len(str(productlist[i][1]))), productlist[i][2])
        i= i + 1    
    input("\npresione cualquier tecla")

def delproduct():
    os.system("clear")
    nameproduct = input("nombre del producto que desea borrar")
    cursor.execute("DELETE FROM `products` WHERE `name_product` = ? ", [nameproduct])
    conn.commit()

def newstock():
    nameproduct = input("nombre del producto")
    stockproduct = input("ingrese la cantidad a agregar")
    cursor.execute("UPDATE `products` SET `stock_product` = `stock_product` + ? WHERE `name_product`= ?", [stockproduct, nameproduct])
    conn.commit()

def delstock():
    nameproduct = input("nombre del producto")
    stockproduct = input("ingrese la cantidad a retirar")
    cursor.execute("UPDATE `products` SET `stock_product` = `stock_product` - ? WHERE `name_product`= ?", [stockproduct, nameproduct])
    conn.commit()

# BEGIN
SetupDatabase()
#SetAdminPassword()
menu()






    







