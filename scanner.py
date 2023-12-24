import telebot
import config

TOKEN = config.PROFUMIERE  
ADMIN_USER_ID = config.MAKKINA  


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['new_chat_members'])
def greet_new_members(message):
    new_members = message.new_chat_members  # Lista di nuovi membri aggiunti al gruppo
    for member in new_members:
        # Controlla se il bot è tra i nuovi membri aggiunti
        if member.username == bot.get_me().username:
            print("chat id: ", message.chat.id )
            bot.send_message(message.chat.id, "Ciao! Sono stato aggiunto a questo gruppo e sono pronto ad aiutarti.")
            # Potresti voler inviare un messaggio privato all'amministratore qui


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_handle = message.from_user.username
    # Costruisci il messaggio da inviare all'amministratore
    admin_msg = f"Nuovo utente: @{user_handle} con ID: {user_id}"

    # Invia un messaggio di benvenuto all'utente
    bot.send_message(user_id, "Benvenuto! Grazie per aver aiutato Francesco a fare un mondo migliore.")

    # Invia l'ID e l'handle dell'utente all'amministratore
    bot.send_message(ADMIN_USER_ID, admin_msg)

bot.polling(none_stop=True)
