import re
from datetime import datetime

<<<<<<< HEAD

def extract_mpesa_details(message, action):
    if action == "add":
        transaction_id_match = re.search(r"([A-Z0-9]+) Confirmed", message)
        amount_match = re.search(r"Ksh([\d,]+\.\d{2})", message)
        date_match = re.search(
            r"on (\d{1,2}/\d{1,2}/\d{2}) at (\d{1,2}:\d{2} [APM]{2})", message
        )
        phone_match = re.search(r"from .+?\b(\d{10})\b", message)
    elif action == "verify":
        transaction_id_match = re.search(r"([A-Z0-9]+) Confirmed", message)
        amount_match = re.search(r"Ksh([\d,]+\.\d{2})", message)
        date_match = re.search(
            r"on (\d{1,2}/\d{1,2}/\d{2}) at (\d{1,2}:\d{2} [APM]{2})", message
        )
        phone_match = re.search(r"to .+?\b(\d{10})\b", message)

    if transaction_id_match and amount_match and date_match and phone_match:
        transaction_id = transaction_id_match.group(1)
        amount = float(amount_match.group(1).replace(",", ""))
        date_str = f"{date_match.group(1)} {date_match.group(2)}"
        transaction_date = datetime.strptime(date_str, "%d/%m/%y %I:%M %p")
        phone_number = phone_match.group(1)

        return transaction_id, amount, transaction_date, phone_number

    return None, None, None, None
=======
def extract_mpesa_details(message, action):
    if action == 'add':
        transaction_id_match = re.search(r'([A-Z0-9]+) Confirmed', message)
        amount_match = re.search(r'Ksh([\d,]+\.\d{2})', message)
        date_match = re.search(r'on (\d{1,2}/\d{1,2}/\d{2}) at (\d{1,2}:\d{2} [APM]{2})', message)
        phone_match = re.search(r'from .+?\b(\d{10})\b', message)
    elif action == 'verify':
        transaction_id_match = re.search(r'([A-Z0-9]+) Confirmed', message)
        amount_match = re.search(r'Ksh([\d,]+\.\d{2})', message)
        date_match = re.search(r'on (\d{1,2}/\d{1,2}/\d{2}) at (\d{1,2}:\d{2} [APM]{2})', message)
        phone_match = re.search(r'to .+?\b(\d{10})\b', message)

    if transaction_id_match and amount_match and date_match and phone_match:
        transaction_id = transaction_id_match.group(1)
        amount = float(amount_match.group(1).replace(',', ''))
        date_str = f"{date_match.group(1)} {date_match.group(2)}"
        transaction_date = datetime.strptime(date_str, "%d/%m/%y %I:%M %p")
        phone_number = phone_match.group(1)
        
        return transaction_id, amount, transaction_date, phone_number
    
    return None, None, None, None
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
