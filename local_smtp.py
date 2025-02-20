import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import AsyncMessage
import email
from email.policy import default

class CustomSMTPHandler(AsyncMessage):
    async def handle_message(self, message):
        print('Incoming message:')
        print(f'From: {message["From"]}')
        print(f'To: {message["To"]}')
        print(f'Subject: {message["Subject"]}')

        # Decode and print the content of the email
        msg = email.message_from_string(message.as_string(), policy=default)
        if msg.is_multipart():
            for part in msg.iter_parts():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    print(f'Content: {body}')
        else:
            body = msg.get_payload(decode=True).decode()
            print(f'Content: {body}')

async def main():
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='127.0.0.1', port=1025)
    controller.start()
    print("SMTP server is running on localhost:1025")
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("SMTP server stopped.")

