# INVENTORY by srdantespelzini using python and sqlite3

# MODULES

import sqlite3 # DATABASE
import os      # OS
from time import localtime, strftime
import sys

database = "database.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()
isdatabase = os.getcwd()



def SetupDatabase():
    if not os.path.isfile(isdatabase + "/database.db"):
        f = open(database,"w")
        f.close
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (password TEXT PRIMARY KEY NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `products` (name_product TEXT PRIMARY KEY NOT NULL, price_product INTEGER, stock_product INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `sells` (sell_time TEXT PRIMARY KEY NOT NULL, sell_product TEXT , sell_qty INTEGER, sell_price INTEGER, sell_type TEXT, sell_total INTEGER) ")

def SetAdminPassword():  
    os.system("clear")
    cursor.execute("SELECT * FROM `admin`")
    fetchded = cursor.fetchall()
    if not fetchded:
        while True:
            password = input("Ingrese una nueva contraseña para el usuario: ").lower()
            passwordre = input ("Ingrese denuevo la contraseña: ").lower()
            if password == passwordre:
                break
        cursor.execute("INSERT INTO `admin` (password) VALUES (?)",[(passwordre)])
        conn.commit()

def Loginadmin():

    while True:
        os.system("clear")
        password = input("Ingrese la contraseña: ").lower()
        cursor.execute(("SELECT * FROM `admin` WHERE `password` = ?",[(password)]))
        results = cursor.fetchall()

        if not results:
            print("Contraseña incorrecta")
            while retry.lower() != "y" or retry.lower() != "n":
                retry = input("Desea reintentar? s/n :")
                if retry.lower() == "n":
                    menu()
        else:
            False
            return True

def validatenumber(message):
    while True:
        try:
            numberinputs = int(input(message))
        except ValueError:
            print("Ingrese un numero entero")
            continue
        else:
            return numberinputs
            break

def validatename(message):
    while True:
        nameinput = input(message).lower()
        cursor.execute("SELECT * FROM `products` WHERE name_product = ?",[nameinput])
        if not cursor.fetchall():
            retry = str
            print("Nombre de producto erroneo")
            while retry != "y" or retry != "n":
                retry = input("Desea reintentar? s/n :").lower()
                if retry.lower() == "n":
                    menu()
                elif retry.lower() == "s":
                    break
        else:
            return nameinput

def validateselltype(message):
     while True:
        typeinput = input(message).lower()
        if typeinput == "d":
            typeinput = "Debito"
            return typeinput
            break
        elif typeinput == "c":
            typeinput = "Credito"
            return typeinput
            break
        elif typeinput == "e":
            typeinput = "Efectivo"
            return typeinput
            break
        else:
            print("Ingrese una opcion d/c/e")



# MENU 

def menu():
    while True:
        os.system("clear")
        print(" 1. Ventas \n 2. Productos y Stock \n 0. Salir")
        operation = input("\n Ingrese el numero de la operacion deseada: ")
        if operation == "1":
            sellsmenu()
        elif operation == "2":
            productmenu()
        elif operation == "0":
            exitmenu()

def sellsmenu():
    while True:
        os.system("clear")
        print(" 1. Ingresar una venta \n 2. Ver informe de ventas \n 3. Vaciar el informe de ventas \n 0. Atras")
        operation = input("\n Ingrese el numero de la operacion deseada: ")
        if operation == "1":
            newsell()
        elif operation == "2":
            sellinfo()
        elif operation == "3":
            clearsells()
        elif operation == "0":
            menu()

def exitmenu():
    os.system("clear")
    while True:
        exitt = input("Desea salir s/n: ")
        if exitt.lower() == "n":
            menu()
        elif exitt.lower() == "s":
            sys.exit()

def newsell():
    os.system("clear")
    print("Ingresar una venta")
    print("------------------")
    selltime = strftime("%d-%m-%Y %H:%M:%S", localtime())
    productname = validatename("Nombre del producto: ").lower()
    sellquantity = validatenumber("Cantidad vendida: ")
    selltype = validateselltype("Efectivo, credito o debito: ").lower()
    cursor.execute("UPDATE `products` SET stock_product = stock_product - ? WHERE name_product = ?", [sellquantity, productname])
    sellprice = (cursor.execute("SELECT price_product FROM `products` WHERE name_product = ? ", [productname] ), (cursor.fetchall()))
    cursor.execute("INSERT INTO `sells` (sell_time, sell_product, sell_qty, sell_price, sell_type, sell_total) VALUES (?, ?, ?, (SELECT price_product FROM `products` WHERE name_product = ? ), ?, ?)", [selltime, productname, sellquantity, productname, selltype, (int(sellquantity) * int(sellprice[1][0][0]) ) ])
    conn.commit()

def sellinfo():
    os.system("clear")
    cursor.execute("SELECT * FROM `sells` ORDER BY `sell_product`")
    selllist = cursor.fetchall()
    i=0
    print("Fecha y hora"," "*13,"Producto"," "*4,"Cantidad"," "*3,"Precio unidad"," "*4,"Metodo de pago"," "*4,"Total de venta")
    print("-"*108)
    while i < len(selllist):
        print(selllist[i][0]," "* (25 - len(str(selllist[i][0]))), (str(selllist[i][1])).capitalize()," "* (12 - len(str(selllist[i][1]))), selllist[i][2]," "* (11 - len(str(selllist[i][2]))), selllist[i][3]," "* (17 - len(str(selllist[i][3]))), selllist[i][4]," "* (18 - len(str(selllist[i][4]))), selllist[i][5])
        i= i + 1    
    input("\nPresione ENTER")

def clearsells():
    os.system("clear")
    cursor.execute("DELETE FROM `sells`")
    conn.commit()

def productmenu(): 
    while True:
        os.system("clear")
        print(" 1. Agregar producto \n 2. Eliminar producto \n 3. Agregar al stock \n 4. Eliminar del stock \n 5.Agregar propiedades del producto \n 6. Ver productos y stock \n 0. Atras")
        operation = input("\n Ingrese el numero de la operacion deseada: ")
        os.system("clear")
        if operation == "1":
            newproduct()
        elif operation == "2":
            delproduct()
        elif operation == "3":
            newstock()
        elif operation == "4":
            delstock()
        elif operation == "5":
            proproduct()
        elif operation == "6":
            viewstock()
        elif operation == "0":
            menu()

def newproduct():
    os.system("clear")
    print("Agregar producto")
    print("----------------")
    nameproduct = input("Nombre del producto: ").lower()
    priceproduct = validatenumber("Precio del producto: ")
    stockproduct = validatenumber("Cantidad del producto: ")
    cursor.execute("INSERT INTO `products` (name_product, price_product, stock_product) VALUES (?, ?, ?)", [nameproduct, priceproduct, stockproduct])
    conn.commit()
    menu()

def viewstock():
    os.system("clear")
    cursor.execute("SELECT * FROM `products` ORDER BY `name_product`")
    productlist = cursor.fetchall()
    i=0
    print("Producto"," "*7,"Precio"," "*4,"Cantidad en stock")
    print("-"*47)
    while i < len(productlist):
        print((str(productlist[i][0])).capitalize()," "* (15 - len(str(productlist[i][0]))), productlist[i][1]," "* (10 - len(str(productlist[i][1]))), productlist[i][2])
        i= i + 1    
    input("\nPresione cualquier tecla")

def delproduct():
    os.system("clear")
    print("Eliminar producto")
    print("-----------------")
    nameproduct = validatename("Nombre del producto: ").lower()
    cursor.execute("DELETE FROM `products` WHERE `name_product` = ? ", [nameproduct])
    conn.commit()

def newstock():
    os.system("clear")
    print("Agregar al stock")
    print("-------------")
    nameproduct = validatename("Nombre del producto: ").lower()
    stockproduct = validatenumber("Ingrese la cantidad: ")
    cursor.execute("UPDATE `products` SET `stock_product` = `stock_product` + ? WHERE `name_product`= ?", [stockproduct, nameproduct])
    conn.commit()

def delstock():
    os.system("clear")
    print("Eliminar del stock")
    print("--------------")
    nameproduct = validatename("Nombre del producto: ").lower()
    stockproduct = validatenumber("Ingrese la cantidad: ")
    cursor.execute("UPDATE `products` SET `stock_product` = `stock_product` - ? WHERE `name_product`= ?", [stockproduct, nameproduct])
    conn.commit()

# BEGIN
SetupDatabase()
SetAdminPassword()
menu()






    







