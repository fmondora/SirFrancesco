# SirFrancesco


Per configurare il progetto, è necessario creare un file `config.py` nella root del progetto. Questo file dovrebbe contenere tutte le impostazioni specifiche, come ad esempio:

```python
# config.py
TELEGRAM_TOKEN="" # il token che arriva da @botfather
DATABASE_ID = " " #il database che contiene i buoni 
DATABASE_USERS = ""  #il database users
NOTION_AUTH = "secret_"

ENV="test"
if ENV=="test":
    TELEGRAM_TOKEN="override" #override
    DATABASE_ID = "override" #production
    DATABASE_USERS = "override" #production
    NOTION_AUTH = "override" #production
    #USER_TEST="override" #Override user
