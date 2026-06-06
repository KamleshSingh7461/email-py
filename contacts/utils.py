import pandas as pd
from .models import Contact, ContactList

def parse_and_save_contacts(file_obj, contact_list_id, mapping):
    """
    Parses an uploaded CSV or Excel file and creates Contact instances.
    `mapping` is a dict that maps expected fields to column names in the file.
    """
    filename = file_obj.name.lower()
    if filename.endswith('.csv'):
        df = pd.read_csv(file_obj)
    elif filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_obj)
    else:
        raise ValueError("Unsupported file format. Please upload a .csv or .xlsx file.")

    df = df.fillna('')
    contact_list = ContactList.objects.get(id=contact_list_id)
    contacts_to_create = []

    for index, row in df.iterrows():
        email_col = mapping.get('email')
        if not email_col or email_col not in df.columns:
            continue
            
        email = str(row[email_col]).strip()
        if not email:
            continue

        first_name_col = mapping.get('first_name')
        last_name_col = mapping.get('last_name')
        phone_col = mapping.get('phone')

        first_name = str(row[first_name_col]).strip() if first_name_col and first_name_col in df.columns else ''
        last_name = str(row[last_name_col]).strip() if last_name_col and last_name_col in df.columns else ''
        phone = str(row[phone_col]).strip() if phone_col and phone_col in df.columns else ''

        extra_data = {}
        for col in df.columns:
            val = row[col]
            if val != '':
                extra_data[col] = str(val)

        contacts_to_create.append(Contact(
            contact_list=contact_list,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone,
            extra_data=extra_data
        ))

    if contacts_to_create:
        Contact.objects.bulk_create(contacts_to_create)
    
    return len(contacts_to_create)
