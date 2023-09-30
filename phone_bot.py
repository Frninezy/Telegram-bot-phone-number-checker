import telebot
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

# Initialize the Telegram bot with your API token
bot = telebot.TeleBot('6423277021:AAFgy3FZWORzSRIii3sSZxRy6-3SFUSMehg')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "Welcome to the Phone Number Info Bot!\n\n"
        "To get information about a phone number, simply send the phone number as a message, "
        "and I will provide you with details such as country, network, and time zone.\n\n"
        "Example: +1234567890"
    )
    bot.send_message(message.chat.id, welcome_message)

@bot.message_handler(func=lambda message: True)
def get_phone_info(message):
    try:
        # Check if the message contains a valid phone number
        phone_number = message.text
        parsed_number = phonenumbers.parse(phone_number, None)

        if phonenumbers.is_valid_number(parsed_number):
            country = geocoder.description_for_number(parsed_number, 'en')
            network = carrier.name_for_number(parsed_number, 'en')
            tz = timezone.time_zones_for_number(parsed_number)

            response = f"Phone number info:\nNumber: {phone_number}\nCountry: {country}\nNetwork: {network}\nTime Zone: {tz[0] if tz else 'Unknown'}"
        else:
            response = "Invalid phone number."

        # Send the response back to the user
        bot.send_message(message.chat.id, response)
    except Exception as e:
        # Handle any exceptions that may occur
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

# Start the bot
bot.polling()
