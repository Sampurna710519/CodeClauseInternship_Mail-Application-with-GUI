import tkinter as tk
from tkinter import filedialog, messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Application")
        self.setup_ui()

    def setup_ui(self):
        self.label_email = tk.Label(self.root, text="Your Gmail:")
        self.label_email.pack()

        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()

        self.label_password = tk.Label(self.root, text="Password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        self.label_recipient = tk.Label(self.root, text="Recipient Gmail:")
        self.label_recipient.pack()

        self.entry_recipient = tk.Entry(self.root)
        self.entry_recipient.pack()

        self.label_subject = tk.Label(self.root, text="Subject:")
        self.label_subject.pack()

        self.entry_subject = tk.Entry(self.root)
        self.entry_subject.pack()

        self.label_body = tk.Label(self.root, text="Body:")
        self.label_body.pack()

        self.text_body = tk.Text(self.root, height=10, width=50)
        self.text_body.pack()

        self.btn_attach = tk.Button(self.root, text="Attach File", command=self.attach_file)
        self.btn_attach.pack()

        self.btn_send = tk.Button(self.root, text="Send Email", command=self.send_email)
        self.btn_send.pack()

    def attach_file(self):
        attachment_path = filedialog.askopenfilename()
        self.attachment_path = attachment_path

    def send_email(self):
        sender_email = self.entry_email.get()
        sender_password = self.entry_password.get()
        recipient_email = self.entry_recipient.get()
        subject = self.entry_subject.get()
        body = self.text_body.get("1.0", "end-1c")

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            if hasattr(self, 'attachment_path') and self.attachment_path:
                with open(self.attachment_path, "rb") as attachment:
                    part = MIMEApplication(attachment.read())
                    part.add_header("Content-Disposition", f"attachment; filename= {self.attachment_path}")
                    msg.attach(part)

            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailApp(root)
    root.mainloop()
