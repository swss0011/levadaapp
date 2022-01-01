import aiohttp
import json

url = 'https://api.mailjet.com/v3.1/send'
verify_url = 'https://bonsai/login/verifyemail/'
change_password_url = 'https://bonsai/user/changepasword/'
api_key = '27ea4da336a9e2a7bb24acf2b7635636'
api_secret = 'e1ae5bb1e0e66f7dc900d2f0813e5fb1'

headers = {
    'Content-Type': 'application/json',
}

payload = {
  "Messages": [
    {
      "From": {
        "Email": "promptdev911@gmail.com",
        "Name": "Edy"
      },
      "To": [
        {
          "Email": "ewalbach@gmail.com",
          "Name": "Edy"
        }
      ],
      "Subject": "Verification Email.",
      
      "HTMLPart": "<h3>Dear Customer, Please open the link: <a href='https://www.mailjet.com/'>In Order To Verify Your Email Address</a>!</h3>"
    }
  ]
}

async def send_email(email: str, linkTo: str, is_verification: bool = True):
    payload["Messages"][0]["To"][0]["Email"] = email
    if(is_verification):
        payload["Messages"][0]["HTMLPart"] = f"<h3>Dear Customer, Please open the link: <a href='{verify_url}{linkTo}'>In Order To Verify Your Email Address</a>!</h3>"
    else:
        payload["Messages"][0]["HTMLPart"] = f"<h3>Dear Customer, Please open the link: <a href='{change_password_url}{linkTo}'>In Order To Change Your Password</a>!</h3>"

    async with aiohttp.ClientSession() as session:
        async with await session.post(url,
                   json=payload,
                   headers=headers,
                   auth=aiohttp.BasicAuth(api_key, api_secret)) as response:

            print("Status:", response.status)
            html = await response.text()
            return response.status
            #print("Content-type:", response.headers['content-type'])

            #html = await response.text()
            #print("Body:", html[:300], "...")

