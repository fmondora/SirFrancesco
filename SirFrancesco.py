import telebot
from telebot import types
import config
import database


# Inserisci il token del tuo bot qui
# Leggi il token da una variabile d'ambiente
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


# Funzione per ottenere il menu principale
def get_main_menu(user_id):
    categories = database.get_unique_categories(user_id)  # Ottieni le categorie uniche per l'utente
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    
    # Aggiungi un bottone per ogni categoria unica
    for category in categories:
        markup.add(types.InlineKeyboardButton(category, callback_data=category))
    
    return markup

# Funzione per ottenere i voucher di una specifica categoria
def get_voucher_menu(category, user_id):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    for voucher in database.get_voucher_data(user_id).get(category, []):
        markup.add(types.InlineKeyboardButton(voucher['title'], callback_data=f"voucher_{category}_{voucher['id']}"))
    markup.add(types.InlineKeyboardButton("👈 Back", callback_data=f'back_to_main'))
    return markup


def escape_markdown(text):
    # Lista dei caratteri da fare l'escape in Markdown
    escape_chars = '_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)



# Invia i dettagli del voucher
def send_voucher_details(chat_id, category, voucher):
    # Prepara il titolo e la descrizione facendo l'escape dei caratteri di Markdown
    title = escape_markdown(voucher['title'])
    descr = escape_markdown(voucher['description'])
    
    # Verifica se il voucher è privato e aggiungi lo spoiler se necessario
    if voucher.get('private'):
        # Aggiungi lo spoiler alla descrizione
        descr = f"||{descr}||"
    
    # Formatta il testo dei dettagli del voucher
    details_text = f"*{title}*\n" \
                   f"_{descr}_\n" \
                   f"\\# *{voucher['quantity']}*"

    # Crea la tastiera inline
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🍑 Use", callback_data=f'use_{category}_{voucher["id"]}'))
    markup.add(types.InlineKeyboardButton("👈 Back", callback_data=f'back_to_category_{category}'))

    # Controlla se il voucher è privato e invia l'immagine con lo spoiler
    if voucher.get('private'):
        bot.send_photo(chat_id=chat_id, photo=voucher['image_url'], caption=details_text, reply_markup=markup, parse_mode='MarkdownV2', has_spoiler=True)
    else:
        bot.send_photo(chat_id=chat_id, photo=voucher['image_url'], caption=details_text, reply_markup=markup, parse_mode='MarkdownV2')


def back_from_voucher_category(chat_id, category):
    # Testo che spiega all'utente di scegliere un voucher dalla categoria specificata
    text = f"🌟 Nell'area *{category}* sono ancora disponibili questi buoni"
    # Invia un nuovo messaggio con il menu dei voucher per quella specifica categoria
    bot.send_message(chat_id=chat_id, text=text, reply_markup=get_voucher_menu(category, chat_id), parse_mode='MarkdownV2')
   
# Escape del markdown
def escape_markdown_v2(text):
    escape_chars = '_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

# Utilizza un voucher
def use_voucher(chat_id, voucher, user_handle, category):

   
    # Decrementa la quantità del voucher
    if voucher['quantity'] > 0:
        voucher['quantity'] -= 1

        database.decrement( voucher['id'] )
        # Invia un messaggio all'utente che ha usato il voucher
        title = escape_markdown(voucher['title'])
        descr = escape_markdown(voucher['description'])
    
        # Verifica se il voucher è privato e aggiungi lo spoiler se necessario
        if voucher.get('private'):
        # Aggiungi lo spoiler alla descrizione
            descr = f"||{descr}||"
    
        # Formatta il testo dei dettagli del voucher
        details_text = f"L'utente *@{user_handle}* *{title}*\n" \
                   f"_{descr}_\n" \
                   f"ne ha ancora: *{voucher['quantity']}*"

        bot.send_message(chat_id, f"Hai usato il voucher: {voucher['title']}. Voucher rimanenti: {voucher['quantity']}", reply_markup=get_voucher_menu(category, chat_id))
        

        
        # Invia un messaggio all'emittente del voucher
        issuer_id = voucher['emettitore']  # Assicurati che questo campo sia presente nel tuo JSON
        bot.send_message(issuer_id, details_text)
    else:
        # Notifica l'utente che il voucher non è più disponibile
        bot.send_message(chat_id, "Questo voucher non è più disponibile.")



# Gestore del comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Ciao! \n\n👋 Sono qui per consegnarti buoni speciali pieni d'affetto da Francesco. \nOgni buono è un gesto per rendere la tua giornata un po' più luminosa. 🌈\n", reply_markup=get_main_menu( message.chat.id ))




@bot.message_handler(commands=['info'])
def send_info(message):
    info_text = (
    "🤖 Info su *Sir Francesco:*\n\n"
    "Questo bot ti permette di riscattare doni speciali pieni d'affetto. Ogni dono è una offerta da parte di Francesco, creato per rendere la tua giornata un po' più luminosa.\n\n"
    "Puoi navigare tra diverse categorie di doni e riscattare quelli che desideri quando vuoi. Ricorda, ogni dono è unico e può essere riscattato per un numero di volte specificato.\n\n"
    "Al riscatto, Francesco riceverà un messaggio e ti contatterà!\n\n"
    "🔹 Usa /start per vedere i doni disponibili.\n\n"
    "🔹 Usa /info se hai bisogno di assistenza.\n\n"
    "Spero che questi piccoli gesti possano portare gioia nella tua vita!"
)
    bot.send_message(message.chat.id, escape_markdown(info_text), parse_mode='MarkdownV2')


# Gestore delle callback query
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(call.id)
    data = call.data
    user_id = call.from_user.id  # ID Telegram dell'utente
    user_handle = call.from_user.username  # Handle Telegram dell'utente

    print("User Id: "+ str(call.from_user.id))
    print("ChatId: "+ str(call.message.chat.id))

     # Gestione del ritorno al menu principale
    if data == 'back_to_main':
        messaggio = "Ogni buono è un gesto per rendere la tua giornata un po' più luminosa. 🌈\n"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=messaggio, reply_markup=get_main_menu( user_id ))
        return

    # Ritorna alla categoria da un post
    if data.startswith('back_to_'):
        category = data.split('_')[3]  # Estrai la categoria dal callback_data
        back_from_voucher_category(call.message.chat.id, category)
        return


    # Gestione del ritorno al menu della categoria
    if data.startswith('back_to_category_'):
        category = data.split('_')[-1]
        try:
            messaggio = f"Questi sono i buoni che hai disponibili in {category}"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=messaggio, reply_markup=get_voucher_menu(category, user_id))
        except Exception as e:
            print(f"Errore nell'aggiornare la didascalia: {e}")
        return
        
    # Gestione della selezione della categoria
    if data in database.get_voucher_data( user_id ):
        messaggio = f"🌟 Nell'area *{data}* sono ancora disponibili questi buoni"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=messaggio, reply_markup=get_voucher_menu(data, user_id), parse_mode='MarkdownV2')
        return

    # Gestione della selezione del voucher

    if data.startswith('voucher_'):
        _, category, voucher_id = data.split('_')
        voucher = next((v for v in database.get_voucher_data( user_id )[category] if v['id'] == voucher_id), None)
        if voucher:
            send_voucher_details(call.message.chat.id, category, voucher)
            #details_text, markup = get_voucher_details(category, voucher)
            #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=details_text, reply_markup=markup, parse_mode='Markdown')
            return

    if data.startswith('use_'):
        _, category, voucher_id = data.split('_')
        voucher = None
        for v in database.get_voucher_data( user_id ).get(category, []):
            if v['id'] == voucher_id :
                voucher = v
                break

        if voucher:
            use_voucher(call.message.chat.id, voucher, user_handle, category)
            return
   
# Avvia il polling

print("Starting bot in "+config.ENV)
bot.polling(none_stop=True)
