from fastapi_mail import ConnectionConfig




conf = ConnectionConfig(
    MAIL_SERVER = "smtp.mail.ru",
    MAIL_PORT = 465,
    MAIL_USERNAME ='beautyroom37@mail.ru',
    MAIL_PASSWORD = "Kit241281",
    MAIL_FROM = "glebhleb89@icloud.com",
    MAIL_TLS = True,
    MAIL_SSL = False
)
#glebhleb89@icloud.com