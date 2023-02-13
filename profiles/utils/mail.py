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
            <!doctype html>
            <html>
              <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <title>Simple Transactional Email</title>
                <style>
                  /* -------------------------------------
                      GLOBAL RESETS
                  ------------------------------------- */
                  
                  /*All the styling goes here*/
                  
                  img {{
                    border: none;
                    -ms-interpolation-mode: bicubic;
                    max-width: 100%; 
                  }}
            
                  body {{
                    background-color: #f6f6f6;
                    font-family: sans-serif;
                    -webkit-font-smoothing: antialiased;
                    font-size: 14px;
                    line-height: 1.4;
                    margin: 0;
                    padding: 0;
                    -ms-text-size-adjust: 100%;
                    -webkit-text-size-adjust: 100%; 
                  }}
            
                  table {{
                    border-collapse: separate;
                    mso-table-lspace: 0pt;
                    mso-table-rspace: 0pt;
                    width: 100%; }}
                    table td {{
                      font-family: sans-serif;
                      font-size: 14px;
                      vertical-align: top; 
                  }}
            
                  /* -------------------------------------
                      BODY & CONTAINER
                  ------------------------------------- */
            
                  .body {{
                    background-color: #f6f6f6;
                    width: 100%; 
                  }}
            
                  /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
                  .container {{
                    display: block;
                    margin: 0 auto !important;
                    /* makes it centered */
                    max-width: 580px;
                    padding: 10px;
                    width: 580px; 
                  }}
            
                  /* This should also be a block element, so that it will fill 100% of the .container */
                  .content {{
                    box-sizing: border-box;
                    display: block;
                    margin: 0 auto;
                    max-width: 580px;
                    padding: 10px; 
                  }}
            
                  /* -------------------------------------
                      HEADER, FOOTER, MAIN
                  ------------------------------------- */
                  .main {{
                    background: #ffffff;
                    border-radius: 3px;
                    width: 100%; 
                  }}
            
                  .wrapper {{
                    box-sizing: border-box;
                    padding: 20px; 
                  }}
            
                  .content-block {{
                    padding-bottom: 10px;
                    padding-top: 10px;
                  }}
            
                  .footer {{
                    clear: both;
                    margin-top: 10px;
                    text-align: center;
                    width: 100%; 
                  }}
                    .footer td,
                    .footer p,
                    .footer span,
                    .footer a {{
                      color: #999999;
                      font-size: 12px;
                      text-align: center; 
                  }}
            
                  /* -------------------------------------
                      TYPOGRAPHY
                  ------------------------------------- */
                  h1,
                  h2,
                  h3,
                  h4 {{
                    color: #000000;
                    font-family: sans-serif;
                    font-weight: 400;
                    line-height: 1.4;
                    margin: 0;
                    margin-bottom: 30px; 
                  }}
            
                  h1 {{
                    font-size: 35px;
                    font-weight: 300;
                    text-align: center;
                    text-transform: capitalize; 
                  }}
            
                  p,
                  ul,
                  ol {{
                    font-family: sans-serif;
                    font-size: 14px;
                    font-weight: normal;
                    margin: 0;
                    margin-bottom: 15px; 
                  }}
                    p li,
                    ul li,
                    ol li {{
                      list-style-position: inside;
                      margin-left: 5px; 
                  }}
            
                  a {{
                    color: #3498db;
                    text-decoration: underline; 
                  }}
            
                  /* -------------------------------------
                      BUTTONS
                  ------------------------------------- */
                  .btn {{
                    box-sizing: border-box;
                    width: 100%; }}
                    .btn > tbody > tr > td {{
                      padding-bottom: 15px; }}
                    .btn table {{
                      width: auto; 
                  }}
                    .btn table td {{
                      background-color: #ffffff;
                      border-radius: 5px;
                      text-align: center; 
                  }}
                    .btn a {{
                      background-color: #ffffff;
                      border: solid 1px #3498db;
                      border-radius: 5px;
                      box-sizing: border-box;
                      color: #3498db;
                      cursor: pointer;
                      display: inline-block;
                      font-size: 14px;
                      font-weight: bold;
                      margin: 0;
                      padding: 12px 25px;
                      text-decoration: none;
                      text-transform: capitalize; 
                  }}
            
                  .btn-primary table td {{
                    background-color: #3498db; 
                  }}
            
                  .btn-primary a {{
                    background-color: #3498db;
                    border-color: #3498db;
                    color: #ffffff; 
                  }}
            
                  /* -------------------------------------
                      OTHER STYLES THAT MIGHT BE USEFUL
                  ------------------------------------- */
                  .last {{
                    margin-bottom: 0; 
                  }}
            
                  .first {{
                    margin-top: 0; 
                  }}
            
                  .align-center {{
                    text-align: center; 
                  }}
            
                  .align-right {{
                    text-align: right; 
                  }}
            
                  .align-left {{
                    text-align: left; 
                  }}
            
                  .clear {{
                    clear: both; 
                  }}
            
                  .mt0 {{
                    margin-top: 0; 
                  }}
            
                  .mb0 {{
                    margin-bottom: 0; 
                  }}
            
                  .preheader {{
                    color: transparent;
                    display: none;
                    height: 0;
                    max-height: 0;
                    max-width: 0;
                    opacity: 0;
                    overflow: hidden;
                    mso-hide: all;
                    visibility: hidden;
                    width: 0; 
                  }}
            
                  .powered-by a {{
                    text-decoration: none; 
                  }}
            
                  hr {{
                    border: 0;
                    border-bottom: 1px solid #f6f6f6;
                    margin: 20px 0; 
                  }}
            
                  /* -------------------------------------
                      RESPONSIVE AND MOBILE FRIENDLY STYLES
                  ------------------------------------- */
                  @media only screen and (max-width: 620px) {{
                    table.body h1 {{
                      font-size: 28px !important;
                      margin-bottom: 10px !important; 
                    }}
                    table.body p,
                    table.body ul,
                    table.body ol,
                    table.body td,
                    table.body span,
                    table.body a {{
                      font-size: 16px !important; 
                    }}
                    table.body .wrapper,
                    table.body .article {{
                      padding: 10px !important; 
                    }}
                    table.body .content {{
                      padding: 0 !important; 
                    }}
                    table.body .container {{
                      padding: 0 !important;
                      width: 100% !important; 
                    }}
                    table.body .main {{
                      border-left-width: 0 !important;
                      border-radius: 0 !important;
                      border-right-width: 0 !important; 
                    }}
                    table.body .btn table {{
                      width: 100% !important; 
                    }}
                    table.body .btn a {{
                      width: 100% !important; 
                    }}
                    table.body .img-responsive {{
                      height: auto !important;
                      max-width: 100% !important;
                      width: auto !important; 
                    }}
                  }}
            
                  /* -------------------------------------
                      PRESERVE THESE STYLES IN THE HEAD
                  ------------------------------------- */
                  @media all {{
                    .ExternalClass {{
                      width: 100%; 
                    }}
                    .ExternalClass,
                    .ExternalClass p,
                    .ExternalClass span,
                    .ExternalClass font,
                    .ExternalClass td,
                    .ExternalClass div {{
                      line-height: 100%; 
                    }}
                    .apple-link a {{
                      color: inherit !important;
                      font-family: inherit !important;
                      font-size: inherit !important;
                      font-weight: inherit !important;
                      line-height: inherit !important;
                      text-decoration: none !important; 
                    }}
                    #MessageViewBody a {{
                      color: inherit;
                      text-decoration: none;
                      font-size: inherit;
                      font-family: inherit;
                      font-weight: inherit;
                      line-height: inherit;
                    }}
                    .btn-primary table td:hover {{
                      background-color: #34495e !important; 
                    }}
                    .btn-primary a:hover {{
                      background-color: #34495e !important;
                      border-color: #34495e !important; 
                    }} 
                  }}
            
                </style>
              </head>
              <body>
                <span class="preheader">This is preheader text. Some clients will show this text as a preview.</span>
                <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
                  <tr>
                    <td>&nbsp;</td>
                    <td class="container">
                      <div class="content">
            
                        <!-- START CENTERED WHITE CONTAINER -->
                        <table role="presentation" class="main">
            
                          <!-- START MAIN CONTENT AREA -->
                          <tr>
                            <td class="wrapper">
                              <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                <tr>
                                  <td>
                                    <h3>Account Verification</h3>
                                    <p>Hi there,</p>
                                     <p>Dear Customer, Please verify you account by clicking on button bellow</p>
                                     <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
                                      <tbody>
                                        <tr>
                                          <td align="left">
                                            <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                              <tbody>
                                                <tr>
                                                  <td> <a href="{temp_url}{link_to}" target="_blank">{msg_text}</a> </td>
                                                </tr>
                                              </tbody>
                                            </table>
                                          </td>
                                        </tr>
                                      </tbody>
                                    </table>
                                    <p>Please kindly ignore this email if you did not register for our service. Thanks</p>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
            
                        <!-- END MAIN CONTENT AREA -->
                        </table>
                        <!-- END CENTERED WHITE CONTAINER -->
            
                      </div>
                    </td>
                    <td>&nbsp;</td>
                  </tr>
                </table>
              </body>
            </html>
        """

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

