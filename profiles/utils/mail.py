import aiohttp
import json

url = 'https://api.mailjet.com/v3.1/send'
verify_url = 'https://bonsai/login/verifyemail/'
change_password_url = 'https://bonsai/user/changepasword/'
api_key = '540c3d704cbaeb778a70e106f9933375'
api_secret = 'b14c008fb259d5927607030d51858539'

headers = {
    'Content-Type': 'application/json',
}

payload = {
  "Messages": [
    {
      "From": {
        "Email": "swss0011@gmail.com",
        "Name": "RRR"
      },
      "To": [
        {
          "Email": "swss0011@gmail.com",
          "Name": "RRR"
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

            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:300], "...")
            return response.status

