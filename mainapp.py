"""
Welcome to Email Sender.

This is an application with a command line interface (console) designed to make sending
quick emails as easy, efficient, and fast as possible. The work is done in an interactive
shell so there is no GUI.

This application makes use of the Python Standard Library modules cmd, email and smtplib which
are the core of this application.

The cmd module wa used to build this as an interactive shell.

The email module was used in order to create an Email instance which makes it easier to specify
things such as receivers, attachments, subject and body.

The smtplib is the basic protocol we use to send the email, and we use SSL encryption.

This application is packed full of commands made to make the task of sending an email very easy.

You must specify your email username and password. Note: the email must be configured to be allowed
access from less secure applications.

Then you must specify a list of receivers for this email, the body, and the subject.
There you have it: a basic email.

You are able to attach as well images, documents, and HTML files to create HTML emails.

Your inputs are saved and they include:
-Username
-Password
-List of Receivers
-Port
-Server
-Body
-Subject
-Attachments
-HTML

You have the option to save these to a JSON file, and load them from a JSON file.
"""

import cmd
import email
import getpass
import imghdr
import os
import pprint
import smtplib
import json


# noinspection PyUnusedLocal
class App(cmd.Cmd):
    intro = "Welcome to Email Sender"
    prompt = ">>>"
    file = None
    email_info = {
        "username": "",
        "password": "",
        "body": "",
        "subject": "",
        "port": 465,
        "server": "smtp.gmail.com",
        "receiver": [],
        "attachments": [],
        "html": ""
    }

    # Setup
    def do_user(self, arg):
        """
        Specify your email username.

        Argument: email
        """
        try:
            self.email_info["username"] = arg
        except Exception as e:
            print(e)

    def do_pass(self, arg):
        """
        Set the password for your email account.

        Argument: no argument
        """
        try:
            password = getpass.getpass(prompt="Password: ", stream=None)
            self.email_info["password"] = password
        except Exception as e:
            print(e)

    def do_server(self, arg):
        """
        Specify the server you wish to use.

        Argument: smtp server
        """
        try:
            self.email_info["server"] = arg
        except Exception as e:
            print(e)

    def do_setup(self, arg):
        """
        Setup the server and the port you wish to use.

        Argument: no argument
        """
        try:
            if arg == "gmail":
                self.email_info["server"] = "smtp.gmail.com"
                self.email_info["port"] = 465
            elif arg == "outlook":
                self.email_info["server"] = "smtp-mail.outlook.com"
                self.email_info["port"] = 587
            elif arg == "yahoo":
                self.email_info["server"] = "smtp.mail.yahoo.com"
                self.email_info["port"] = 465
            else:
                print("Specify one of the acceptable inputs:\ngmail\noutlook\nyahoo")
        except Exception as e:
            print(e)

    def do_port(self, arg):
        """
        Set the port you want to use.

        Argument: port number
        """
        try:
            self.email_info["port"] = arg
        except Exception as e:
            print(e)

    def do_recv(self, arg):
        """
        Set the receiver of your email.

        Argument 1: receiver email
        Argument 2: pop <int>            Removes email inserted at position int starting 0.

        Note:
        Can add multiple receivers.
        """
        try:
            array = arg.split()
            if array[0] == "pop":
                self.email_info["receiver"].pop(int(array[1]))
            else:
                self.email_info["receiver"].append(arg)
        except Exception as e:
            print(e)

    def do_cred(self, arg):
        """
        Set the username and password of your email account.

        Argument: no argument
        """
        try:
            user = input("Username: ")
            password = input("Password: ")
            self.email_info["username"] = user
            self.email_info["password"] = password
        except Exception as e:
            print(e)

    # Email
    def do_subj(self, arg):
        """
        Specify the subject of your email.

        Argument: subject
        """
        try:
            self.email_info["subject"] = arg
        except Exception as e:
            print(e)

    def do_body(self, arg):
        """
        Set the plain text body of your email. "end" to end.

        Argument: no argument
        """
        try:
            msg = ""
            while True:
                line = input("> ")
                if line == "end":
                    break
                else:
                    msg = msg + "\n" + line
            self.email_info["body"] = msg
        except Exception as e:
            print(e)

    def do_info(self, arg):
        """
        View the information you have entered so far.

        Argument: no argument
        """
        try:
            pprint.pprint(self.email_info)
        except Exception as e:
            print(e)

    # Attachments
    def do_img(self, arg):
        """
        Attach images to message.
        All image types supported.
        Follow instructions.

        Argument: no argument
        """
        try:
            img_path = input("Path to Image: ")
            with open(img_path, "rb") as image:
                image_data = image.read()
                image_type = imghdr.what(img_path)
                image_name = image.name
            self.email_info["attachments"].append([image_data, "image", image_type, image_name])
            print("Image attached successfully.")
        except Exception as e:
            print(e)

    def do_doc(self, arg):
        """
        Attach documents to message.
        All image types supported.
        Follow instructions.

        Argument: no argument
        """
        try:
            doc_path = input("Path to Document: ")
            with open(doc_path, "rb") as doc:
                doc_data = doc.read()
                doc_name = doc.name
            self.email_info["attachments"].append([doc_data, "application", "octet-stream", doc_name])
            print("Document attached successfully.")
        except Exception as e:
            print(e)

    def do_html(self, arg):
        try:
            html_path = input("Path to HTML: ")
            with open(html_path, "r") as html:
                data = html.read()
                self.email_info["html"] = data
            print("HTML attached successfully.")
        except Exception as e:
            print(e)

    def do_reset(self, arg):
        """
        Reset all the values that you have inputted.
        Application information will return to default.

        Argument: no argument
        """
        self.email_info = self.email_info.fromkeys(self.email_info, "")
        self.email_info['server'] = "smtp.gmail.com"
        self.email_info['port'] = 465
        self.do_clear(self)

    # Login
    def do_login(self, arg):
        """
        Login into your account. Test whether your credentials are correct.

        Argument: no argument
        """
        try:
            print("Attempting to Login...")
            with smtplib.SMTP_SSL(self.email_info["server"], self.email_info["port"]) as server:
                server.login(self.email_info["username"], self.email_info["password"])
            print("Login Successful.\nCredentials are fine.")
        except Exception as e:
            print(e)

    def do_send(self, arg):
        """
        Send email.

        Argument: no argument
        """
        try:
            print("Logging in...")
            msg = email.message.EmailMessage()
            msg["Subject"] = self.email_info["subject"]
            msg["From"] = self.email_info["username"]
            msg["To"] = ", ".join(self.email_info["receiver"])
            msg.set_content(self.email_info["body"])
            for att in self.email_info["attachments"]:
                msg.add_attachment(att[0], maintype=att[1], subtype=att[2], filename=att[3])
            msg.add_alternative(self.email_info["html"], subtype="html")
            with smtplib.SMTP_SSL(self.email_info["server"], self.email_info["port"]) as server:
                server.login(self.email_info["username"], self.email_info["password"])
                print("Logged in.")
                server.send_message(msg)
                print("Message sent successfully.")
        except Exception as e:
            print(e)

    # JSON
    def do_save(self, arg):
        """
        Save settings to a JSON file.(Specify absolute path to file included)

        Argument: no argument
        """
        try:
            path = input("JSON file path: ")
            with open(path, 'w+') as file:
                json.dump(self.email_info, file, sort_keys=True, indent=4)
        except Exception as e:
            print(e)

    def do_load(self, arg):
        """
        Load settings from a JSON file.(Specify absolute path to file included)

        Argument: no argument
        """
        try:
            path = input("JSON file path: ")
            with open(path, 'r+') as file:
                self.email_info = json.load(file)
        except Exception as e:
            print(e)

    # Console
    @staticmethod
    def do_about(arg):
        print("""
                Welcome to Email Sender.
                
                This is an application with a command line interface (console) designed to make sending
                quick emails as easy, efficient, and fast as possible. The work is done in an interactive 
                shell so there is no GUI.
                
                This application makes use of the Python Standard Library modules cmd, email and smtplib which
                are the core of this application. 
                
                The cmd module wa used to build this as an interactive shell.
                
                The email module was used in order to create an Email instance which makes it easier to specify
                things such as receivers, attachments, subject and body.
                
                The smtplib is the basic protocol we use to send the email, and we use SSL encryption.
                
                This application is packed full of commands made to make the task of sending an email very easy.
                
                You must specify your email username and password. Note: the email must be configured to be allowed
                access from less secure applications.
                
                Then you must specify a list of receivers for this email, the body, and the subject. 
                There you have it: a basic email.
                
                You are able to attach as well images, documents, and HTML files to create HTML emails.
                
                Your inputs are saved and they include:
                -Username
                -Password
                -List of Receivers
                -Port
                -Server
                -Body
                -Subject
                -Attachments
                -HTML

                You have the option to save these to a JSON file, and load them from a JSON file.
            """)

    @staticmethod
    def do_clear(arg):
        """
        Clear the console window.

        Argument: no argument
        """
        try:
            os.system('cls')
        except OSError:
            os.system('clear')

    @staticmethod
    def do_exit(arg):
        """
        Exit application.

        Argument: no argument
        """
        try:
            quit()
        except Exception as e:
            print(e)


app = App()
app.cmdloop()
