# Nya Rotary Pub Websida

Använder sig av Flask, UWSGI, och en extern reverse-proxy SWAG för produktion.

## Development

Starta dev-containern med `docker-compose -f docker-compose.dev.yml up -d`och accessa localhost:5000 för att se sidan. Allt under `website/rotary` förutom `website/rotary/static` går att redigera för att se på devhemsidan. Ingen autorefresh på hemsidan tyvärr ;((

## Kort info om vad NPM gör.
"You either die a hero or live long enough to see yourself become the villain." beskriver detta projekt ganska bra. Det blev lite mer komplext men grunden är att via npm så hämtas och packeteras de js filerna som använder dataTables (shifts och beers i nuläget). Utöver detså körs också purgecss för att ta bort onödig CSS* och skriver över den redan skapade style.css filen skapat.


*Det är ganska mycket onödig css, då mycket i Bulma inte används. Då Bulma är modulärt bör en del av detta kunna åtgärdas genom att bara importerar de modulerna vi använder oss av men detta blr kollas närmare på, i dagsläget är purgecss dock ett bra mellansteg.
