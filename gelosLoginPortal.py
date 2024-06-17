# Gelos login portal project
# By Alexander Graham

from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
import time
import ctypes                                           # imports
import winsound
import random
import string
import re

# Variable setup
window = tk.Tk()
user_var=tk.StringVar()
passw_var=tk.StringVar()                                # variables
passVerification = False
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#------------------------------------- MAIN WINDOW SETTINGS -------------------------------------#

# get the screen dimension
window_width = 500
window_height = 400
verificationWindow_width = 250
verificationWindow_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
textboxSizeWidth = 50

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
window.resizable(FALSE, FALSE)


# background, title, logo, systray logo
window.configure(bg="grey")
window.title("Gellos Login Portal")
myappid = 'mycompany.myproduct.subproduct.version'                                  # I aint gonna lie I stole this code
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)              # But basicaly it makes it so the logo can be displayed in systrey adn taskbar
small_icon = tk.PhotoImage(file="content\gelosENT16BIT.png")                        # Turning it into a image tk can understand
large_icon = tk.PhotoImage(file="content\gelosENT32BIT.png")
window.iconphoto(True, large_icon, small_icon)                                      # Use the small icon for the window and big icon for the taskbar

#------------------------------------- MAIN WINDOW SETTINGS -------------------------------------#

# Resizing the image so it can display properly
img = Image.open("content\gelosENT.png")
resized_image = img.resize((150, 100))
new_image = ImageTk.PhotoImage(resized_image)

def windowKillSwitch():     # Kill switch for the entire window
    time.sleep(0.3)
    window.destroy()  

def toggle():    
    if showPasswordButton.var.get():                                                # when the user checks the checkbox it shows them the password and not ***
        entryPassword.config(show = "*")
    else:
        entryPassword.config(show= "")
        
def goBack():
    adminPanel.destroy()
    window.deiconify()

# When the Login button is pressed
def submit(*arg):
    passVerification = False
    
    user_var = entryUser.get()
    passw_var = entryPassword.get()
    login_info = entryUser.get() + ' ' + entryPassword.get()
    
    #checking if the username and password is in the accounts.txt
    
    for line in open(r"content\accounts.txt", 'r').readlines():
        login_info = line.split() # Split on the space, and store the results in a list of two strings
        if user_var == login_info[0] and passw_var == login_info[1]:
            passVerification = True

    
    if passVerification == True:       # If both verification checks are met
        time.sleep(0.5)                                     # Artificial waiting (for effect)
        
        global verificationWindow
        verificationWindow = Toplevel()                     # creating a new window
        verificationWindow.title("")
        verificationWindow.geometry(f'{verificationWindow_width}x{verificationWindow_height}+{center_x}+{center_y}')
        verificationWindow.resizable(FALSE, FALSE)
        verificationWindow.configure(bg="grey")
        verificationWindow.title("Complete")
        verificationWindow.focus_force()                    # Forces the focus 
        
        verificationLabel = tk.Label(                       # Making a text box to say Sign in complete
            verificationWindow,
            text = "Sign in complete",
            fg = "dark green",
            bg = "grey"
        )
        verificationLabel.pack()                            # Placing the window
        verificationLabel.place(x=75, y=75)
        
                                                             # Creating the OK button so it can exit the window
        okButton = tk.Button(verificationWindow, text = "OK", command = windowKillSwitch)
        okButton.pack()
        okButton.place(x=107, y=100)

    if passVerification == False:                           # If the username and password is wrong
        global incorrectText
        incorrectText = tk.Label(                           # Display a text box saying it is inccorect
            window,
            text = "Incorrect try again",
            fg = "red",
            background = "grey",
        )
        incorrectText.after(2500, incorrectText.destroy)    # After 2.5 seconds destroy the text box
        incorrectText.pack()
        incorrectText.place(x=window_width/2.5,y=350)

def signUp():                                               # When the user presses the sign up button
    
    def toggle():
        if signUpButtonShowButton.var.get():                # same fuction as the earlier toggle but for the signup window
            entryNewPassword.config(show = "*")
        else:
            entryNewPassword.config(show= "")
            
    def generate(*args):                                        # to generate a new secure password
        
        warningWindowWidth = 250
        warningWindowHeight = 200
        center_x_warning = center_x - 75
        center_y_warning = center_y - 90                    
        
        global warningWindow
        warningWindow = Toplevel()                              # making a warning window to let the user know to save the password
        warningWindow.title("Warning")
        warningWindow.geometry(f'{warningWindowWidth}x{warningWindowHeight}+{center_x_warning}+{center_y_warning}')
        warningWindow.resizable(FALSE, FALSE)
        warningWindow.focus_force()
        warningWindow.configure(bg="grey")
        
        winsound.PlaySound("IDoNotExist", winsound.SND_ASYNC)   # a sound to attract the users attention
        
        warningMessage = tk.Label(warningWindow, text="Please save the auto generated password\nIf you loose the password\n you will have to contact support\n to reinstate your account", bg="grey")
        warningMessage.pack(pady=20)
        warningMessage.after(3000, warningWindow.destroy)       # destroy the window after it has been deleted
        
        characters = string.ascii_letters + string.digits                       # making the random password have random numbers and letters
        randomPassword = ''.join(random.choice(characters) for i in range(12))  # generating those random numbers and letters
        entryNewPassword.delete(0, END)                                         # deleting whatever is in the box originaly
        entryNewPassword.insert(0, randomPassword)                              # inserting the new auto generated password into the entry box
        
    def signUpCheckAndComplete():                                               # once the user has pressed the sign up button
        canDisplayPass_var = True
        canProceedEmail = False
        canProceedPass = False
        
        if(re.fullmatch(regex, entryEmail.get())):                              # check if it is a valid email adress
            canProceedEmail = True                      # can continue with the setup
        else:
            incorrectEmail = tk.Label(signUpWindow, text = "Please enter a valid email", fg= "red", bg= "grey")
            incorrectEmail.pack()
            incorrectEmail.place(x=33, y=322)
            incorrectEmail.after(6000, incorrectEmail.destroy)                      # error saying it wasnt a valid email
            canDisplayPass_var = False                                              # for formattingm I dont want the incorrect email message mixing with 
                                                                                    # the incorrect password label, it looks ugly and weird ewwwwwww
        newPass_var = entryNewPassword.get()
        newPass_var_count = len(newPass_var)                                    # count how many characters are in the password
        
        if canDisplayPass_var == True:                                          # if there isnt another error sign
            if newPass_var_count >= 6:
                canProceedPass = True                                           # can continue with setup of account
            else:
                incorrectPassword = tk.Label(signUpWindow, text="Password needs to be longer\nthan 6 characters", fg = "red", bg="grey")
                incorrectPassword.pack()
                incorrectPassword.place(x=33, y=322)
                incorrectPassword.after(3500, incorrectPassword.destroy)
                
        if canProceedEmail and canProceedPass == True:                          # once the two entrys are verifyed
            with open(r"content\accounts.txt", 'a') as entry:                   # open the accounts folder
                email_var = entryEmail.get()
                pass_var = entryNewPassword.get()
                total = '\n' + email_var + " " + pass_var                       # format the account and username
                entry.write(total)                                              # write the username into the file and create a new line so passwords dont get muddled up
            
            time.sleep(1.5)                                             # artifical waiting
            
            signUpWindow.destroy()                                  # kill the signup window
            signUpDone = tk.Label(window, text="Account created, please log in", bg="grey", fg="light green")
            signUpDone.pack(side=BOTTOM)
            signUpDone.after(4000, signUpDone.destroy)                  # yippe! your account is created :)
            
    signUpCenter_x = center_x + 45                          # Create a artificial offset to cause less confusion
    signUpCenter_y = center_y + 5
    
    global signUpWindow                                     # Creating the window and applying settings
    signUpWindow = Toplevel()
    signUpWindow.title("Sign up to Gelos Portal")
    signUpWindow.geometry(f'{window_width}x{window_height}+{signUpCenter_x}+{signUpCenter_y}')
    signUpWindow.resizable(FALSE, FALSE)
    signUpWindow.focus_force()
    signUpWindow.configure(bg="grey")
    
    signUpHeading = Frame(signUpWindow, bg = "grey")        # Frame for the title
    signUpHeading.pack()
    
                                                            # title
    Label(signUpHeading, text = "Sign up to Gelos Online Portal", font = ("Helvatical bold",15), fg="black", bg="grey").pack(side=TOP, pady=10)
    
                                                            # image
    labelImageSignUp = tk.Label(signUpWindow, image = new_image)
    labelImageSignUp.pack(side=tk.TOP)
    
                                                            # Email input
    frameEmail = tk.Frame(signUpWindow, bg= 'grey', padx=10, pady=15)
    frameEmail.pack()
    
    Label(frameEmail, text="Enter your Company Email :", fg="black", bg="grey", font = ('Helvatical bold',10)).pack(side=LEFT,padx=10, pady=20)
    
    entryEmail = tk.Entry(frameEmail, width=textboxSizeWidth)
    entryEmail.pack(side=RIGHT, padx=7)
    
                                                            # New password input
    frameNewPassword = tk.Frame(signUpWindow, bg='grey', padx=10)
    frameNewPassword.pack()
    
    Label(frameNewPassword, text='New Secure Password :      ', bg="grey", fg='black', font = ('Helvatical bold',10)).pack(side=LEFT, padx=10)
    
    entryNewPassword = tk.Entry(frameNewPassword, width=textboxSizeWidth, show="*")
    entryNewPassword.pack(side=RIGHT, padx=7)
    
                                                            # sign up button
    labelSubmit = tk.Button(signUpWindow, bg="white", fg="black", text= "Sign Up", command=signUpCheckAndComplete)
    labelSubmit.pack(side=BOTTOM, pady=30)
    
    signUpShowPassword = tk.Frame(signUpWindow, bg="grey", pady=10)
    signUpShowPassword.pack()
                                                            # generate password button
    generatePassword = tk.Button(signUpShowPassword, bg="white", fg="black", text="Generate Secure Password", command= generate)
    generatePassword.pack(side=RIGHT, padx= 45)
    
    Label(signUpShowPassword, text="Show Password", bg="grey").pack(side=LEFT)
    
                                                            # show password checkbox
    signUpButtonShowButton = tk.Checkbutton(signUpShowPassword, bg="grey", command = toggle, onvalue=False, offvalue=True)
    signUpButtonShowButton.var = tk.BooleanVar(value=True)
    signUpButtonShowButton['variable'] = signUpButtonShowButton.var
    signUpButtonShowButton.pack(side=LEFT)
    
def accountInformation():
    global adminPanel
    adminPanel = Toplevel()
    adminPanel.title("Sign up to Gelos Portal")
    adminPanel.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    adminPanel.resizable(FALSE, FALSE)
    adminPanel.focus_force()
    adminPanel.configure(bg="grey")
    
    title = tk.Label(adminPanel, text= "Account info", font = ('Helvatical bold',15), fg = "black", bg = "grey")
    title.pack(side=TOP)
    
    back = tk.Button(adminPanel, text="Back", command=goBack)
    back.pack(side=BOTTOM, pady=30)
    
    with open(r"content\accounts.txt") as file:
        textFile = file.read()
        labelList = tk.Label(adminPanel, text = textFile)
        labelList.pack(pady= 20)
    
    
#------------------------------------- WINDOW LABEL & ENTRY SETUP -------------------------------------#

labelHead = tk.Label(                                               # Making the heading
    text = "Please login to the Gelos Enterprises Portal", font = ('Helvatical bold',15), fg = "black", bg = "grey")
labelHead.pack(side=tk.TOP, pady=10)


labelImage = tk.Label(image = new_image)                            # Add the gelos image
Label(window, image=new_image).pack(side = TOP)


labelUser = Frame(window, bg="grey")                                # Adding the username frame
labelUser.pack()

Label(labelUser, text="Username :", fg="black", bg="grey", font = ("Helvatical bold",12)).pack(side=LEFT, pady=30)

entryUser = tk.Entry(labelUser, width = textboxSizeWidth)           # Adding a frame makes it so the text and entry box can be
entryUser.pack(side=RIGHT,padx=30, pady=20)                         # displayed side by side properly without using messy x & y cords


labelPassword = Frame(window, bg="grey")                            # Adding the password frame
labelPassword.pack()

Label(labelPassword, text="Password :", fg="black", bg="grey", font = ("Helvatical bold",12)).pack(side=LEFT, pady=30)

entryPassword = tk.Entry(labelPassword, width = textboxSizeWidth, show="*")            
entryPassword.pack(side=RIGHT,padx=30, pady=20)                     # Same with the username

labelCommands = Frame(window, bg="grey")                            # Yeah this part doesnt work but im not going to fix it
labelCommands.pack()

labelLogin = tk.Button(labelCommands, text = "Login", command = submit, bd = 1) # login buttom
labelLogin.pack(side=LEFT)

labelSignUp = tk.Button(window, text = "Sign Up", command = signUp, bd=1)       # signup buttom
labelSignUp.pack()
labelSignUp.place(x=50, y=322)                                      # <-- It looks so bad but I hate the pack function so suck it

tk.Button(window, text="Accounts", command = accountInformation, bd = 1).pack(side=BOTTOM)

showPassword = tk.Label(window, text="Show Password", bg= "grey")               # show password button
showPassword.pack()
showPassword.place(x=335, y=322)

showPasswordButton = tk.Checkbutton(window,bg="grey", onvalue=False, offvalue=True, command=toggle)
showPasswordButton.var = tk.BooleanVar(value=True)
showPasswordButton['variable'] = showPasswordButton.var
showPasswordButton.pack()
showPasswordButton.place(x=430, y=321)

window.bind('<Return>', submit)                             # make it so when someone presses enter it clicks the sign in button
window.mainloop()