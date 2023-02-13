import aiohttp
import json
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from typing import List



#
verify_url = 'https://levada-server.onrender.com/login/verifyemail/'
change_password_url = 'https://levada-server.onrender.com/user/changepasword/'

config_credentials = dotenv_values(".env")
#"smtp-relay.sendinblue.com",
conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials["USERNAME"],
    MAIL_PASSWORD = config_credentials["PASS"],
    MAIL_FROM = config_credentials["EMAIL"],
    MAIL_PORT = 587,
    MAIL_SERVER = "in-v3.mailjet.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)


async def send_email(email: str, linkTo: str, is_verification: bool = True):
    temp_url = ""
    link_to = linkTo
    msg_text = ""
    template = ""

    print("1---------------------------")

    if is_verification:
        temp_url = verify_url
        msg_text = "In Order To Verify Your Email Address"

        template = f"""
                        <html>
                            <head>
                            </head>
                            <body>
                                <div style = "display: flex; align-items: center; justify-content: center; flex-direction: column">
                                    <h3>Account Verification</h3>
                                    <br>
                                    <p>Dear Customer, Please open the link:</p>
                                    <a stle="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #275d8; color: white;" href="{temp_url}{link_to}">{msg_text}</a>
                                    <p>Please kindly ignore this email if you did not register for our service. Thanks</p>
                                </div>
                            </body>
                        </html>
                    """
    else:
        temp_url = verify_url
        msg_text = "In Order To Change Your Password"

        template = f"""
                                <!DOCTYPE html>
                                <html>
                                    <head>
                                    </head>
                                    <body>
                                        <div style = "display: flex; align-items: center; justify-content: center; flex-direction: column">
                                            <h3>Account Verification</h3>
                                            <br>
                                            <p>Dear Customer, Please open the link:</p>
                                            <a stle="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #275d8; color: white;" href="{temp_url}{link_to}">{msg_text}</a>
                                            <p>Please kindly ignore this email if you did not register for our service. Thanks</p>
                                        </div>
                                    </body>
                                </html>
                            """

    subject_text = ""

    if is_verification:
        subject_text = "Postaty; Verify Your Email"
    else:
        subject_text = "Postaty; Change Your Password"

    print("2---------------------------")
    message = MessageSchema(
        subject=subject_text,
        recipients=[email],  # LIST OF recipients
        html=template,
        subtype="html"
    )

    fm = FastMail(conf)
    print("3---------------------------")
    try:
        await fm.send_message(message=message)
    except:
        return 404

    return 200

