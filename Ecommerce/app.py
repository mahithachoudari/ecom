from flask import Flask,render_template,url_for,request
app = Flask(__name__)
import smtplib
import pymysql
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "root",
    "database" : "ECOM"
}

@app.route("/")
def landing():
    return render_template("home.html") 

@app.route("/register1")
def register1():
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/register2",methods=["POST","GET"])
def register2():
    username=request.form["username"]
    fullname=request.form["fullname"]
    email=request.form["email"]
    mobile=request.form["mobile"]
    password=request.form["password"]
    cpassword=request.form["cpassword"]
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USERNAME = %s"
    cursor.execute(query,(username,))
    data =  cursor.fetchone()
    conn.close()
    print(data)
    if data is not None:
        return render_template("register.html",msg="usernameexist")
    elif password != cpassword:
        return render_template("register.html",msg="wrongpassword")
    else:
        otp = random.randint(1111,9999)

        body = f"OTP For Validation is {otp}"

        #miza zifw ppse nojz

        msg=MIMEMultipart()
        msg["From"] = "nuthakkimahitha16@gmail.com"
        msg["To"] = email
        msg['Subject'] = "OTP For Validation"
        msg.attach(MIMEText(body, 'plain'))

        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("nuthakkimahitha16@gmail.com","miza zifw ppse nojz")
        server.send_message(msg)
        server.quit()
        return render_template("otpverification.html",username=username,fullname=fullname,email=email,mobile=mobile,password=password,otp=otp)


@app.route("/register3",methods=["POST","GET"])
def register3():
    username=request.form["username"]
    fullname=request.form["fullname"]
    email=request.form["email"]
    mobile=request.form["mobile"]
    password=request.form["password"]
    otp=request.form["otp"]
    cotp=request.form["cotp"]

    if str(otp) != str(cotp):
        newotp = random.randint(1111,9999)
        body = f"OTP For Validation is {newotp}"
        msg=MIMEMultipart()
        msg["From"] = "nuthakkimahitha16@gmail.com"
        msg["To"] = email
        msg['Subject'] = "OTP For Validation"
        msg.attach(MIMEText(body, 'plain'))

        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("nuthakkimahitha16@gmail.com","miza zifw ppse nojz")
        server.send_message(msg)
        server.quit()
        return  render_template("otpverification.html",msg="Invalid",username=username,fullname=fullname,email=email,mobile=mobile,password=password,otp=newotp)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query ="INSERT INTO USERS VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query,(username,fullname,email,mobile,password))
        conn.commit()
        conn.close()
        return render_template("login1.html",msg="account created")
    
@app.route("/login1")
def login1():
    return render_template("login1.html")

@app.route("/login2",methods=["POST","GET"])
def login2():
    username=request.form["username"]
    password=request.form["password"]
    print(username)
    print(password)
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchone()

    if data is None:
        return render_template("login1.html",msg="nouser")
    if data[-1] != password:
        return render_template("login1.html",msg="wrongpassword")
    else:
        return render_template("userhome.html",username=username)
    
@app.route("/forgetpassword")
def forgetpassword():
    return render_template("forgetpassword1.html")

@app.route("/forgetpassword1",methods=["POST","GET"])
def forgetpassword1():
    username = request.form["username"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return render_template("forgetpassword1.html",msg="nouser")
    else:
        newotp = random.randint(1111,9999)

        #weej tuer oawt ipwp

        body = f"OTP For Validation is {newotp}"
    
        msg = MIMEMultipart()
        msg["From"] = "nuthakkimahitha16@gmail.com"
        msg["To"] = data[2]
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("nuthakkimahitha16@gmail.com","miza zifw ppse nojz")
        server.send_message(msg)
        server.quit()

        return render_template("forgetpassword2.html",username=data[0],email=data[2],otp=newotp)
    
@app.route("/forgetpassword2",methods=["POST","GET"])
def forgetpassword2():
    username = request.form["username"]
    email = request.form["email"]
    otp = request.form["otp"]
    cotp = request.form["cotp"]
    password = request.form["password"]
    cpassword = request.form["cpassword"]
    print(username)
    print(email)
    print(otp)
    print(cotp)
    print(password)
    print(cpassword)
    
    if str(otp) != str(cotp):
        newotp = random.randint(1111,9999)

        #weej tuer oawt ipwp

        body = f"OTP For Validation is {newotp}"
    
        msg = MIMEMultipart()
        msg["From"] = "nuthakkimahitha16@gmail.com"
        msg["To"] = email
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("nuthakkimahitha16@gmail.com","miza zifw ppse nojz")
        server.send_message(msg)
        server.quit()

        return render_template("forgetpassword2.html",msg="wrongotp",username=username,email=email,otp=newotp)
    elif password != cpassword:
        return render_template("forgetpassword3.html",msg="wrongpassword",username=username,email=email)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE USERS SET PASSWORD = %s WHERE USERNAME = %s"
        cursor.execute(query,(password,username))
        conn.commit()
        conn.close()
        return render_template("login1.html",msg="passwordreset")
    
@app.route("/forgetpassword3",methods=["POST","GET"])
def forgetpassword3():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    cpassword = request.form["cpassword"]
    print(username)
    print(email)
    print(password)
    print(cpassword)

    if password != cpassword:
        return render_template("forgetpassword3.html",msg="wrongpassword",username=username,email=email)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE USERS SET PASSWORD = %s WHERE USERNAME = %s"
        cursor.execute(query,(password,username))
        conn.commit()
        conn.close()
        return render_template("login1.html",msg="passwordreset")
    

@app.route("/addtocart1", methods=["POST","GET"])
def addtocart1():
    username =  request.form["username"]
    product_id = request.form["productid"]
    product_name = request.form["productname"]
    product_price = request.form["productprice"]
    print(username)
    print(product_id)
    print(product_name)
    print(product_price)

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USERNAME = %s AND PRODUCT_ID = %s"
    cursor.execute(query,(username,product_id))
    data = cursor.fetchone()
    if data is None:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO CART (USERNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(username,product_id,product_name,product_price))
        conn.commit()
        conn.close()
        return render_template("userhome.html",username=username,msg="product added")
    else:
        qty = int(data[-1]) + 1
        price = int(data[-2]) * qty
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE CART SET QUANTITY = %s WHERE PRODUCT_ID = %s AND USERNAME = %s"
        cursor.execute(query,(qty,product_id,username))
        conn.commit()
        conn.close()
        
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE CART SET PRODUCT_PRICE = %s WHERE PRODUCT_ID = %s AND USERNAME = %s"
        cursor.execute(query,(price,product_id,username))
        conn.commit()
        conn.close()
        return render_template("userhome.html",username=username,msg="product updated")
    
@app.route("/shopping_cart/<username>")
def shopping_cart(username):
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchall()
    conn.close()
   
    if len(data) == 0:
        return render_template("userhome.html",username=username,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total += int(i[-2])
        return render_template("shopping_cart.html",data=data,username=username,grandtotal=total)

@app.route('/update_quantity', methods=["POST","GET"])
def update_quantity():
    product_id = request.form['product_id']
    action = request.form['action']
    username = request.form['username']

    conn = mysql.connector.connect(host="localhost", user="root", password="", database="your_db_name")
    cursor = conn.cursor()

    # Get user_id from username
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()[0]

    # Get current quantity
    cursor.execute("SELECT quantity FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    result = cursor.fetchone()

    if result:
        quantity = result[0]
        if action == 'increase':
            quantity += 1
        elif action == 'decrease' and quantity > 1:
            quantity -= 1

        cursor.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s",
                       (quantity, user_id, product_id))
        conn.commit()

    cursor.close()
    conn.close()

    return redirect(f"/cart/{username}")

    
@app.route("/userhome2/<username>")
def userhome2(username):
    return render_template("userhome.html",username=username)

@app.route("/deleteproduct/<pid>/<username>")
def deleteproduct(pid,username):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM CART WHERE PRODUCT_ID = %s"
    cursor.execute(query,(pid))
    conn.commit()
    conn.close()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchall()
    conn.close()
   
    if len(data) == 0:
        return render_template("userhome.html",username=username,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total += int(i[-2])
        return render_template("shopping_cart.html",data=data,username=username,grandtotal=total)

@app.route("/success",methods=["POST","GET"])
def success():
    username = request.form["username"]


    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO ORDERS (USERNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE,QUANTITY) SELECT USERNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE,QUANTITY FROM CART"
    cursor.execute(query,)
    conn.commit()
    conn.close()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM CART WHERE USERNAME = %s"
    cursor.execute(query,(username))
    conn.commit()
    conn.close()
    return render_template("userhome.html",username=username)

@app.route("/failure",methods=["POST","GET"])
def failure():
    username = request.form["username"]
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchall()
    conn.close()
   
    if len(data) == 0:
        return render_template("userhome.html",username=username,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total += int(i[-2])
        return render_template("shopping_cart.html",data=data,username=username,grandtotal=total)

@app.route("/orders/<username>")
def orders(username):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM ORDERS WHERE USERNAME = %s"
    cursor.execute(query,(username))
    data = cursor.fetchall()
    conn.close()
    return render_template("userorders.html",data=data,username=username)
@app.route("/success1",methods=["POST","GET"])
def success1():
    username = request.form["username"]
    productid = request.form["productid"]
    productname = request.form["productname"]
    productprice = request.form["productprice"]
    quantity = request.form["quantity"]

    print(username)
    print(productid)
    print(productname)
    print(productprice)
    print(quantity)

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO ORDERS (USERNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE,QUANTITY) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query,(username,productid,productname,productprice,quantity))
    conn.commit()
    conn.close()

    return render_template("user_home.html",username=username)
        
app.run()