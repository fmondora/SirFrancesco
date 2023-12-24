from notion_client import Client

import config


# Configura il client Notion
# Sostituisci con il tuo token dell'API di Notion
notion = Client(auth=config.NOTION_AUTH)
# Sostituisci con l'ID del tuo database Notion

voucher_data = {
    "divertimento": [
        {"id": "v1f", "title": "Parco Avventura", "description": "Esplora il parco...", "image_url": "http://example.com/parco.jpg", "quantity": 10},
        {"id": "vff2", "title": "Parco Avventura1", "description": "Esplora il parco...", "image_url": "http://example.com/parco.jpg", "quantity": 10},
        {"id": "v3ff", "title": "Parco Avventura2", "description": "Esplora il parco...", "image_url": "http://example.com/parco.jpg", "quantity": 10},
        # Altri voucher...
    ],
    "xxx": [
        { "id": "v2", "private": "true", 
        "title": "🌬️👔💋 Stiratura naked", 
        "description": "Mi offro di trasformare una semplice stiratura in un'esperienza unica e piccante. Immagina: io, completamente nudo, che mi dedico con attenzione e cura a stirare ogni tuo capo di abbigliamento. Una combinazione perfetta di utilità e seduzione, che aggiunge un pizzico di eccitazione e sorrisi a un'ordinaria faccenda domestica. Sarà un modo per spezzare la routine, aggiungendo un tocco di audacia e divertimento alla nostra giornata. 🎉🔥👚", 
        "image_url": 
        "https://cdn08.bdsmlr.com/uploads/photos/2019/08/89146/bdsmlr-89146-2KxaR7irOd.jpg", 
        "quantity": 5, 
        "emettitore": "5941599694"},
        # Altri voucher...
    ],
    # Aggiungi altre categorie...
    # @fmondora - 28576633
    # @miciamicio - 5941599694
}

# Ottieni tutti i voucher data per un utente e ritornali nella forma del json 
# { categoria : [{ id, private, title, description, image_url, quantity, emettitore }, ]}
def get_voucher_data(user_id):
    user_vouchers = get_voucher_for(user_id)  # Ottieni i voucher per l'utente
    updated_voucher_data = {}  # Una nuova struttura per mantenere i dati aggiornati

    if user_vouchers and user_vouchers['results']:
        for item in user_vouchers['results']:
            # Estrai le proprietà necessarie da ogni record
            category = item.get("properties", {}).get("Categoria", {}).get("select", {}).get("name", "Altri")  # Assicurati che la categoria esista in Notion
            title = item.get("properties", {}).get("Name", {}).get("title", [{}])[0].get("plain_text", "")
            image_url = item.get("properties", {}).get("immagine", {}).get("url", "")
            description = item.get("properties", {}).get("descrizione", {}).get("rich_text", [{}])[0].get("plain_text", "")
            is_private = item.get("properties", {}).get("private", {}).get("checkbox", False)
            voucher_count = item.get("properties", {}).get("Voucher", {}).get("number", 0)

            # Estrai la proprietà rollup "Emettitore"
            emettitore_data = item.get("properties", {}).get("emettitore", {}).get("rollup", {}).get("array", [])
            emettitore = emettitore_data[0].get("number") if emettitore_data else None

            
            # Crea un nuovo voucher
            new_voucher = {
                "id": item["id"],  # Usa l'ID di Notion o un altro identificativo unico
                "title": title,
                "description": description,
                "image_url": image_url,
                "quantity": voucher_count,
                "private": is_private,
                "emettitore": emettitore  # Assumi che l'utente corrente sia l'emettitore
            }

            # Aggiungi il nuovo voucher alla categoria corrispondente
            if category not in updated_voucher_data:
                updated_voucher_data[category] = []
            updated_voucher_data[category].append(new_voucher)

    return updated_voucher_data


# Ottiene le categorie uniche per un utente
def get_unique_categories(user_id):
    voucher_data = get_voucher_data(user_id)  # Ottieni i dati del voucher per l'utente
    categories = set()  # Usa un set per evitare duplicati

    # Itera attraverso tutti i voucher e raccoglie le categorie
    for category, vouchers in voucher_data.items():
        categories.add(category)  # Aggiunge la categoria al set

    return list(categories)  # Converte il set in una lista e la restituisce


    
# Ottieni da notion la lista dei voucher per lo user_id (telegram id)
def get_voucher_for(user_id):
    try:

       
        filter = {
            "filter": {
                "and": [
                    {
                         "property": "t",  # Nome della proprietà rollup
                        "rollup": {
                            "any": {
                                 "number": {
                                 "equals": int(user_id)
                                }
                             }
                        }
                    },
                    {
                        "property": "Voucher",
                        "number": {
                            "greater_than": 0
                        }
                    }
                ]
            }
        }
        items = notion.databases.query(database_id=config.DATABASE_ID, **filter)
        return items
    except Exception as e:
        print(f"Error: {e}")
        return []


# Decrementa un voucher dato il suo Id
def decrement(voucher_id):
    try:
        # Ottieni prima il voucher corrente per sapere il conteggio attuale
        current_voucher = notion.pages.retrieve(voucher_id)

        # Estrai il conteggio attuale dal voucher
        current_count = current_voucher.get("properties", {}).get("Voucher", {}).get("number", 0)

        # Calcola il nuovo conteggio
        new_count = max(0, current_count - 1)  # Evita numeri negativi

        # Costruisci l'aggiornamento da inviare a Notion
        update_payload = {
            "properties": {
                "Voucher": {
                    "number": new_count
                }
            }
        }

        # Invia l'aggiornamento a Notion
        notion.pages.update(voucher_id, **update_payload)
        print(f"Voucher {voucher_id} aggiornato con successo. Nuovo conteggio: {new_count}")
    except Exception as e:
        print(f"Errore durante l'aggiornamento del voucher {voucher_id}: {e}")
