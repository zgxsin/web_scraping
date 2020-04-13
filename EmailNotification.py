import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailNotification:
    def __init__(self, contact_file, template_message_file):
        self.contact_file = contact_file
        self.template_message_file = template_message_file

    def get_contacts(self):
        """
        Return two lists names, emails containing names and email addresses
        read from a file specified by self.contact_file .
        """
        names = []
        emails = []
        with open(self.contact_file, mode='r') as contacts_file:
            for single_line_contact in contacts_file:
                names.append(single_line_contact.split()[0])
                emails.append(single_line_contact.split()[1])
        return names, emails

    def read_template(self):
        """
        Returns a Template object comprising the contents of the
        file specified by self.template_message_file.
        """

        with open(self.template_message_file, 'r') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    def notify_by_email(self, email_address, email_password, email_subject="Data at your request is available!",
                        message_to_send="sample text"):
        # Reference: https://www.freecodecamp.org/news/send-emails-using-code-4fcea9df63f/.
        names, emails = self.get_contacts()
        message_template = self.read_template()

        # Set up the SMTP server.
        # todo: add instruction.
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(email_address, email_password)

        # For each contact, send the email:
        for name, email in zip(names, emails):
            # Create a message.
            msg = MIMEMultipart()

            # Add in the actual person name to the message template.
            message = message_template.substitute(PERSON_NAME=name.title(), CONTENTS=message_to_send)

            # Setup the parameters of the message.
            msg['From'] = email_address
            msg['To'] = email
            msg['Subject'] = email_subject

            # Add in the message body.
            msg.attach(MIMEText(message, 'plain'))

            # Send the message via the server set up earlier.
            server.send_message(msg)
            del msg

        # Terminate the SMTP session and close the connection.
        server.quit()


if __name__ == "__main()__":
    email_notification_obj = EmailNotification(contact_file="files/contacts.txt",
                                               template_message_file="files/message_template.txt")
    # You need to configure your email setting inside this function.
    email_notification_obj.notify_by_email(email_address="example@gmail.com", email_password="xxx")
