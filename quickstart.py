import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1NIKEZs0EH8RdcP6Au7Y0m65p9yotwho2M9TRpUsyesk"
SAMPLE_RANGE_NAME = "A2:P100"

today_day = datetime.now().day
this_month = datetime.now().month

months_spanish = {
    1: 'enero',
    2: 'febrero',
    3: 'marzo',
    4: 'abril',
    5: 'mayo',
    6: 'junio',
    7: 'julio',
    8: 'agosto',
    9: 'septiembre',
    10: 'octubre',
    11: 'noviembre',
    12: 'diciembre'
        }

this_month_spanish = months_spanish[this_month]


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    # get keys
    keys = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A1:P1").execute().get("values", {})

    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueRenderOption="UNFORMATTED_VALUE")
        .execute()
    ).get("values", {})

    # combine keys and values

    final_result = []
    for row in result:
      final_result.append(dict(zip(keys[0], row)))

    messages_quantity = 0

    messages_to_send = []

    for row in final_result:
        dates_difference = int(today_day) - int(row['payment_date'])
        if(dates_difference >= 0 and dates_difference < 3 and row['status'] == 'Activo' and row[this_month_spanish] == 'no'):
            #print(f"El cliente {row['name']} no ha pagado los servicios de {row['servicios']} su suscripción vencía el día {row['payment_date']} de este mes.")
            client_message = f"Hola {row['name']}. Este mensaje es para recordarte que tu suscripción a {row['servicios']} venció el día {row['payment_date']} de este mes. Por favor realiza el pago correspondiente para evitar la suspensión de tus servicios. Gracias por tu preferencia."
            formated_whatsapp_client_message = client_message.replace(" ", "%20")
            current_message = f"El cliente {row['name']} no ha pagado los servicios de {row['servicios']} su suscripción vencía el día {row['payment_date']} de este mes. \n Enviar mensaje: https://wa.me/{row['phone']}?text={formated_whatsapp_client_message}"
            messages_to_send.append(current_message)


        if(dates_difference > 3 and row['status'] == 'Activo' and row[this_month_spanish] == 'no'):
            #print(f"El cliente {row['name']} no ha pagado los servicios de {row['servicios']} su suscripción vencía el día {row['payment_date']} de este mes, por favor retirar.") 
            client_message = f"Hola {row['name']}. Este mensaje es para recordarte que tu suscripción a {row['servicios']} venció el día {row['payment_date']} de este mes. Por favor realiza el pago correspondiente para evitar la suspensión de tus servicios. Gracias por tu preferencia."
            formated_whatsapp_client_message = client_message.replace(" ", "%20")
            current_message = f"\n\nEl cliente {row['name']} no ha pagado los servicios de {row['servicios']} su suscripción vencía el día {row['payment_date']} de este mes, por favor retirar. \n Enviar mensaje: https://wa.me/{row['phone']}?text={formated_whatsapp_client_message}"
            messages_to_send.append(current_message)

    if len(messages_to_send) > 0:
        return messages_to_send


    if len(messages_to_send) == 0:
        return messages_to_send

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()
