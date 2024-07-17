import mysql.connector
import streamlit as st
import re

# Setting SQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="login"
)

mycursor = mydb.cursor(buffered=True)

# Setting the page config
st.set_page_config(page_title='Login', page_icon=':zap:', layout='wide', initial_sidebar_state='auto')


# setting the streamlit tabs
tab1, tab2 = st.tabs(['REGISTER', 'LOGIN'])

with tab1:
    # register page
    st.header('Register here')
    st.write("New User? Register here")

    # Name input field
    fName = st.text_input('First Name')
    if fName is None:
        st.error('First Name cannot be empty')
    
    lastName = st.text_input('Last Name')
    if lastName is None:
        st.error('Last Name cannot be empty')

    # Email input field
    email = st.text_input('Email', value=None)
    if email is not None:
        if not re.match(r"^[a-z0-9\.\+_-]+@gmail.com$", email):
            st.error('Invalid Email')
            
    # Phonenumber input field
    phoneNumber = st.text_input('Phone Number', value= None)
    if phoneNumber is not None:
        if not re.match(r"^[0-9]{10}$", phoneNumber):
            st.error('Invalid Phone Number')
    
    # Password input field
    password = st.text_input('Password', type='password', value = None)
    if password is not None:
        if len(password) < 8:
            st.error('Password should be atleast 8 characters long')
    
    # Checking the password
    confirmPassword = st.text_input('Confirm Password', type='password')
    if st.button('Register'):
        if password == confirmPassword:
            try:
                # Storing the data in MySQL database
                sql = "INSERT INTO users (firstName, lastName, email, phonenumber, password) VALUES (%s, %s, %s, %s, %s)"
                val = (fName, lastName, email, phoneNumber, password)
                mycursor.execute(sql, val)
                mydb.commit()
                st.spinner('Registering...')
                st.success('Registered successfully')   
            except:
                st.error('User already exists, please login')
        else:
            st.error('Passwords do not match')

with tab2:
    # login page
    st.header('Login here')
    st.write("Already Registered? Login here")
    flag = False
    
    emailTab, phoneTab = st.tabs(['Log in with Email', 'Log in with Phone Number'])
    with emailTab:
        loginEmail = st.text_input('Email id', value=None)
        if loginEmail is not None:
            if not re.match(r"^[a-z0-9\.\+_-]+@gmail.com$", loginEmail):
                st.error('Invalid Email')
        loginPassword = st.text_input('Pass Word', type='password', value = None)
        if loginPassword is not None:
            if len(loginPassword) < 8:
                st.error('Password should be atleast 8 characters long')
        
        if st.button('Login'):
            # Retriving the stored data from MySQL by mail id
            sql = "SELECT * FROM users WHERE email = %s AND password = %s"
            val = (loginEmail, loginPassword)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                flag = True
                st.spinner('Logging in...')
                st.success('Login Successful')

                st.header('Welcome {}'.format(myresult[0][0]))
                st.write("Nice to meet you!")
                st.code('email', myresult[0][2])
                st.code('phonenumber', myresult[0][3])
            else:
                st.error('Invalid Credentials or try to register')
    

    with phoneTab:
    # Phonenumber input field
        loginPhoneNumber = st.text_input('PhoneNumber', value= None)
        if loginPhoneNumber is not None:
            if not re.match(r"^[0-9]{10}$", loginPhoneNumber):
                st.error('Invalid Phone Number')

        # Password input field
        loginPassword = st.text_input('Pass word', type='password', value = None)
        if loginPassword is not None:
            if len(loginPassword) < 8:
                st.error('Password should be atleast 8 characters long')

        if st.button('Log in'):
            # Retriving the stored data from MySQL by phonenumber
            sql = "SELECT * FROM users WHERE phonenumber = %s AND password = %s"
            val = (loginPhoneNumber, loginPassword)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                flag = True
                st.spinner('Logging in...')
                st.success('Login Successful')

                st.header('Welcome {}'.format(myresult[0][0]))
                st.write("Nice to meet you!")
                st.code('email', myresult[0][2])
                st.code('phonenumber', myresult[0][3])
            
            else:
                st.error('Invalid Credentials or try to register') 
    if flag:
        if st.button('Logout'):
            st.write('Thank you')
            st.write('You are logged out')   