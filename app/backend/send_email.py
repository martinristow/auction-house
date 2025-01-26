import smtplib
from app.backend.config import settings


async def email_send(title, user_email):
    email_message = (f"Subject:Честитки! Победивте на аукцијата: {title}\n\nПочитуван/а,\n\n"
                     f"Честитки! Вие сте победник на аукцијата {title}.\n\n"
                     f"За да ја реализирате уплатата на средствата, ве молиме посетете ја нашата веб-страница: www.platiaukcija.com.\n\n"
                     f"⚠️ Важно:\n"
                     f"Доколку не ја реализирате уплатата во рок од 3 дена, аукцијата ќе биде изгубена, а предметот повторно ќе биде достапен за продажба.\n\n"
                     f"Доколку имате прашања или ви е потребна помош, слободно контактирајте нè.\n\n"
                     f"Со почит,\n"
                     f"Тимот на Плати Аукција")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(settings.my_email, settings.password)
        message = email_message
        connection.sendmail(from_addr=settings.my_email,
                            to_addrs=user_email,
                            msg=message.encode("utf-8"))



async def contact_email_send(user_email, message_from_user):
    email_message = (f"Здраво,\n\n"
                     f"{message_from_user}\n\n"
                     f"Со почит,\n"
                     f"{user_email}")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(settings.my_email, settings.password)
        message = email_message
        connection.sendmail(from_addr=user_email,
                            to_addrs=settings.my_email,
                            msg=message.encode("utf-8"))
