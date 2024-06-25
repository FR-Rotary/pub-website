# Nya Rotary Pub Websida

Använder sig av Flask, UWSGI, och en extern reverse-proxy SWAG för produktion.

## Development

Starta dev-containern med `docker-compose -f docker-compose.dev.yml up -d`och accessa localhost:5000 för att se sidan. Allt under `website/rotary` förutom `website/rotary/static` går att redigera för att se på devhemsidan. Ingen autorefresh på hemsidan tyvärr ;((
