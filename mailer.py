import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from usermanagement import encode_user

sender_email = "heretaungacollegeforum@sebj.nz"
sender_name = "Heretaunga College Forum"
password = str("mcvG8EhPwHz9") 

def verify_email(receiver_email, name, uid, authentication_type, verification, domain):
    smtp = smtplib.SMTP('smtp.zoho.com.au', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender_email, password)

    email = MIMEMultipart("alternative")
    email["From"] = formataddr((sender_name, sender_email))
    email["reply-to"] = "sebastian.johnstone@heretaunga.school.nz"

    email["Subject"] = f"HC Forum {authentication_type}"
    email["To"] = receiver_email    
    if authentication_type == "New Account":
        context = "Your account has been created, but you need to verify it."
        verification_encoded = encode_user(uid, verification, "New Account")
    else:
        context = "Your account needs to be verified for security reasons."
        verification_encoded = encode_user(uid, verification, "Reverify Account")
    
    text = f"Welcome {name}, to Heretaunga College's Forum!\n\nYour account has been created, but you need to verify it.\n\nEither visit http://{domain}/{verification_encoded}, or on your next login, use this code: {verification}\n\nIf you didn't sign up for an account, then you can safely delete this email."

    html = f"""
    <html>
        <head>
            <style>
                body {{
                    display: flex;
                }}
                * {{
                    font-family: Calibri, Geneva, Tahoma, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                .header {{
                    margin: auto;
                    width: 100%;
                    display: flex;
                    background-color: #8D0B41;
                    padding-bottom: 1vh;
                    color: white;
                }}
                .title {{
                    margin-left: auto;
                    margin-right: auto;
                    margin-top: 1vh;
                }}
                .content {{
                    font-size: 1.1em;
                    text-align: center;
                    padding-top: 1vh;
                    padding-bottom: 1vh;
                    background-color: #E9DCD3;
                }}
                .code {{
                    font-size: 2em;
                    background-color: #E1D0C4;
                    width: 40%;
                    margin-left: auto;
                    margin-right: auto;
                }}
                .footer {{
                    color: white;
                    width: 100%;
                    background-color: #8D0B41;
                    padding-top: 1vh;
                    padding-bottom: 1vh;
                    text-align: center;
                }}
                a {{
                    color: black;
                }}
                .main {{
                    font-size: 2em;
                }}
                .content_text {{
                    font-size: 1.5em;
                }}
                .content2_text {{
                    font-size: 1.25em;
                }}
                .container {{
                    width: 100%;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 class="title">Heretaunga College Forum</h1>
                </div>
                <div class="content">
                    <h2 class="main">Welcome {name}, to Heretaunga College's Forum!</h2>
                    <br>
                    <h2 class="content_text">{context}</h2>
                    <br>
                    <h2 class="content_text">Either <a href="{domain}verify?code={verification_encoded}">click here</a>, or on your next login, use this code:</h2>
                    <br>
                    <p class="code">{verification}</p>
                    <br>
                    <h2 class="content2_text">If you didn't sign up for an account, then you can safely delete this email.</h2>
                </div>
                <div class="footer">
                    <h2>© 2025 Sebastian Johnstone</h2>
                </div>
            </div>
        </body>
    </html>
    """

    text_body = MIMEText(text, 'plain')
    html_body = MIMEText(html, 'html')

    email.attach(text_body)
    email.attach(html_body)

    smtp.sendmail(email["From"], email["To"], email.as_string())
    smtp.quit()

def post_update(receiver_email, name, domain, post_name, pid, commenterusername):
    smtp = smtplib.SMTP('smtp.zoho.com.au', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender_email, password)

    email = MIMEMultipart("alternative")
    email["From"] = formataddr((sender_name, sender_email))
    email["reply-to"] = "sebastian.johnstone@heretaunga.school.nz"

    email["Subject"] = f"HC Forum | {post_name} has a new comment"
    email["To"] = receiver_email    
    
    text = f"Hi, {name}, a post you follow has a new comment!\n\n{commenterusername} has replied with a comment on the post {post_name}\n\nHere's a quick link to the post: http://{domain}/forum/{pid}\n\nIf you don't have an account on Heretaunga College Forum, then reply to this email 'Stop', we won't email you again."

    html = f"""
    <html>
        <head>
            <style>
                body {{
                    display: flex;
                }}
                * {{
                    font-family: Calibri, Geneva, Tahoma, sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                .header {{
                    margin: auto;
                    width: 100%;
                    display: flex;
                    background-color: #8D0B41;
                    padding-bottom: 1vh;
                    color: white;
                }}
                .title {{
                    margin-left: auto;
                    margin-right: auto;
                    margin-top: 1vh;
                }}
                .content {{
                    font-size: 1.1em;
                    text-align: center;
                    padding-top: 1vh;
                    padding-bottom: 1vh;
                    background-color: #E9DCD3;
                }}
                .code {{
                    font-size: 2em;
                    background-color: #E1D0C4;
                    width: 40%;
                    margin-left: auto;
                    margin-right: auto;
                }}
                .footer {{
                    color: white;
                    width: 100%;
                    background-color: #8D0B41;
                    padding-top: 1vh;
                    padding-bottom: 1vh;
                    text-align: center;
                }}
                a {{
                    color: black;
                }}
                .main {{
                    font-size: 2em;
                }}
                .content_text {{
                    font-size: 1.5em;
                }}
                .content2_text {{
                    font-size: 1.25em;
                }}
                .container {{
                    width: 100%;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 class="title">Heretaunga College Forum</h1>
                </div>
                <div class="content">
                    <h2 class="main">Hi, {name}, a post you follow has a new comment!</h2>
                    <br>
                    <h2 class="content_text">{commenterusername} has replied with a comment on the post <a href="{domain}forum/{pid}">{post_name}</a></h2>
                    <br>
                    <h2 class="content_text">Here's a quick link to the post: <a href="{domain}forum/{pid}">CLICK</a></h2>
                    <br>
                    <h2 class="content2_text">If you don't have an account on Heretaunga College Forum, then reply to this email 'Stop', we won't email you again.</h2>
                </div>
                <div class="footer">
                    <h2>© 2025 Sebastian Johnstone</h2>
                </div>
            </div>
        </body>
    </html>
    """

    text_body = MIMEText(text, 'plain')
    html_body = MIMEText(html, 'html')

    email.attach(text_body)
    email.attach(html_body)

    smtp.sendmail(email["From"], email["To"], email.as_string())
    smtp.quit()
