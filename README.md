# gold


sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/www.goldfisher.de.key -out /etc/nginx/ssl/www.goldfisher.de.crt

sudo apt install wkhtmltopdf


Neongelb    #FFFF00
Neonrot     #FF073A
Neongrü     #39FF14
Neonblau    #00E5FF
Neonping    #FF6EC7
Neonorange	#FF5F1F
Neonlila    #B026FF
Neocyan     #00FFD5
Neonlime	#CCFF00

UST = U.S. Treasury
Treasuries = Sammelbegriff für US-Staatsanleihen
T-Bills (Treasury Bills)
Laufzeit: bis 1 Jahr
Keine Zinsen, sondern Abschlag (Zero Coupon)

T-Notes (Treasury Notes)
Laufzeit: 2–10 Jahre
Feste halbjährliche Zinszahlung

T-Bonds (Treasury Bonds)
Laufzeit: 20–30 Jahre
Feste halbjährliche Zinszahlung

US10Y = 10-jährige US-Staatsanleihe
US2Y = 2-jährige
US30Y = 30-jährige


## MYSQL fuer Goldpreis

mysql -u debian-sys-maint -pOO82WE7zXPdvvqp8

CREATE DATABASE gold

CREATE USER 'gold'@'localhost' IDENTIFIED BY 'rodengold';
Select * from mysql.user;
GRANT ALL PRIVILEGES ON gold . * TO 'gold'@'localhost';
FLUSH PRIVILEGES;

### Neue Tabelle Umtauschkurs
create table exchangerate( id integer unsigned not null auto_increment, day date not null, usd decimal(8,4) not null, primary key(id), index exchangerate_day (day) ) engine=innodb;
insert into exchangerate set day='2026-01-07', usd='1234.1234';

### Neue Tabelle goldpreis
create table goldapicom ( id integer unsigned not null auto_increment, day date not null, clock time not null, price decimal(6,2) not null, primary key(id), index goldapicom_day_clock (day, clock) ) engine=innodb;

CREATE TABLE variety (`id` int unsigned NOT NULL AUTO_INCREMENT, `day` date NOT NULL, `clock` time NOT NULL, gold decimal(6,2) NOT NULL, silver decimal(6,2) NOT NULL, copper decimal(6,2) NOT NULL, platinum decimal(6,2) NOT NULL, palladium decimal(6,2) NOT NULL, PRIMARY KEY (`id`), KEY variety_day_clock (`day`,`clock`) ) ENGINE=InnoDB

### Change
select date(timepoint) as day, time(timepoint) as clock, price from timepoint, gold_api_com  where timepoint.id=gold_api_com.timepoint_id order by day, clock Limit 10;


# Dolarkurs
curl -XGET https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_Q6iwqY0PHnM0d0HePBaxpkdDzYiVGCsiSJNcTppf

use gold;

CREATE TYBLE goldprice (id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, timepoint TIMESTAMP NOT NULL, price DECIMAL(8,2),PRIMARY KEY( id ),UNIQUE KEY timepoint (timepoint)) ENGINE=InnoDB;

insert into goldprice set timepoint='2025-01-13T12:30:00', pricepergram=22112652.12;

create table timepoint ( id integer unsigned not null, auto_increment timepoint timestamp NOT NULL, primary key(id)) ENGINE=InnoDB;
create table gold_api_com ( timepoint_id integer unsigned not null, price decimal(6,2) NOT NULL, primary key(timepoint_id)) ENGINE=InnoDB;

CREATE INDEX idx_timepoint_timepoint ON timepoint(timepoint);

# Dolarkurs
curl -XGET https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_Q6iwqY0PHnM0d0HePBaxpkdDzYiVGCsiSJNcTppf

CREATE table exchange_rate (id integer unsigned auto_increment not null primary key, timepoint_id integer unsigned not null, usd decimal(8,6) not null) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
select distinct(date(timepoint)) from timepoint;

## Zeitzone setzen
Anschauen: timedatectl
Setzen: timedatectl set-timezone Europe/Berlin 
https://wiki.ubuntuusers.de/Systemzeit/

## Goldpreise zum Vergleich
https://www.wallstreet-online.de/rohstoffe/goldpreis
https://www.gold.de/kurse/goldpreis/


@app.route('/fig/<cropzonekey>')
def fig(cropzonekey):
    fig = draw_polygons(cropzonekey)
    img = StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


Was diese Zeiten üblicherweise bedeuten
🕘 9:00 Uhr Start des europäischen Handelstages, Orientierung am frühen London-/Frankfurt-Handel, Wird oft als „Tagesanfangskurs“ in Deutschland verwendet
Geeignet für: Preisvergleiche, Buchhaltung, Tagesstatistiken

🕘 21:00 Uhr Entspricht grob dem Ende des US-Handelstages, Nähe zum COMEX-/New-York-Schluss
Wird häufig als „Tagesschlusskurs“ genutzt, Relevant für: Tagesabschluss, Charts Abrechnungspreise bei Händlern

Die offiziellen Referenzpreise sind die LBMA Gold Prices:
AM Fix: 10:30 Uhr London (≈ 11:30 MEZ)
PM Fix: 15:00 Uhr London (≈ 16:00 MEZ)
