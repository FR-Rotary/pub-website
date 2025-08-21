# Nya Rotary Pub Websida

Använder sig av Flask, UWSGI, och en extern reverse-proxy SWAG för produktion.

## Development

Starta dev-containern med `docker-compose -f docker-compose.dev.yml up -d`och accessa localhost:5000 för att se sidan. Allt under `website/rotary` förutom `website/rotary/static` går att redigera för att se på devhemsidan. Ingen autorefresh på hemsidan tyvärr ;((

### Steg 1: Skapa en .env fil innehållandes det variabler som behövs i composefilen. ***
SECRET_KEY behöver genereras [enligt](https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY), om man inte orkar klicka på länkar kan helt enkelt bara köra detta: `python -c 'import secrets; print(secrets.token_hex())' '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'`

USERNAME och PASSWORD är helt enkelt vilka inloggningsuppgifterna för kontot som har access till internsidan. 

GOOGLE_USERNAME & GOOGLE_PASSWORD är lite mer komplicerat. Användarnamnet är helt enkelt mejladressen för kontot. Lösenordet måste däremot vara ett applikationslösenord, instruktioner för hur man gör det finns i [denna](https://support.google.com/accounts/answer/185833?hl=en) artikel.


### Steg 2: Migrera databasen
Detta bör vara så lätt som att bara köra skriptet migrate.py, tyvärr är det sällan så lätt.

## Kort info om vad NPM gör.
"You either die a hero or live long enough to see yourself become the villain." beskriver detta projekt ganska bra. Det blev lite mer komplext men grunden är att via npm så hämtas och packeteras de js filerna som använder dataTables (shifts och beers i nuläget). Utöver detså körs också purgecss för att ta bort onödig CSS* och skriver över den redan skapade style.css filen skapat.


*Det är ganska mycket onödig css, då mycket i Bulma inte används. Då Bulma är modulärt bör en del av detta kunna åtgärdas genom att bara importerar de modulerna vi använder oss av men detta blr kollas närmare på, i dagsläget är purgecss dock ett bra mellansteg.

## Google bös
https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
https://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.html
