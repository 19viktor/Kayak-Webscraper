import time
from time import strftime, sleep
from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Error
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import os
import re
from statistics import mean, median
#import smtplib

Airports = ("Aarhus", "Aberdeen Ltd", "Abu Dhabi", "Acapulco", "Adana-Sakirpasa", "Addis Ababa-Bole", "Adelaide", "Aden", "Aerodrom Portoroz doo", "Agadir – Al Massira", "Agen – La Ganne", "Agra", "Ahmedabad – Sardar Vallabh Bhai Patel Int´l", "Ajaccio – Campo Dell´Oro", "Akron-Canton Regional", "Alamosa-Bergman-San Luis Valley Regional Airfield", "Albany", "Albi – Le Sequestre", "Albuquerque", "Alderney", "Aleppo", "Alesund-Vigra", "Alexandria", "Alexandria – El Nhouza", "Alexandroupolis National", "Alghero-Fertilia", "Algiers-Houari Boumedienne", "Alicante", "Alice Springs", "Almaty Int´l", "Almeria", "Alor Setar – Sultan Abdul Halim", "Altenrhein", "Amarillo – Rick Husband", "Amilcar Cabral", "Amman-Queen Alia", "Amritsar – Raja Sansi", "Amsterdam Schiphol", "Anchorage – Ted Stevens", "Ancona", "Angoulême – Brie-Champniers", "Ankara – Esenboga", "Annaba-Rabah Bitat", "Annecy – Haute Savoie", "Antalya", "Antananarivo-Ivato Aerodrome", "Antigua-VC Bird", "Antofagasta-Cerro Moreno", "Antwerp", "Appleton/Outagamie County Regional", "Aqaba", "Arad", "Arica-Chacalluta", "Arkhangelsk – Talagi", "Aruba – Queen Beatrix", "Asheville Regional", "Ashkabad", "Asmara Int´l", "Asturias", "Asuncion – Silvio Pettirossi", "Aswan – Daraw", "Athens Ben Epps", "Athens – Eleftherios Venizelos", "Athens – Hellinikon", "Atlanta – Hartsfield Atlanta", "Atlantic City Int´l", "Auckland", "Augsburg", "Augusta Regional", "Austin-Bergstrom", "Avignon/Caumont", "Badajoz-Talavera la Real", "Baden-Airpark GmbH", "Baghdad", "Bahrain", "Baku – Bina Int´l", "Bali-Denpasar-Ngurah Rai", "Balikpapan-Sepinggan", "Baltimore/Washington Int´l", "Bamako-Senou Int´l", "Bandaranaike Int´l", "Bangalore", "Bangkok Int´l", "Bangor", "Bangui-M´Poko", "Banjul Int´l", "Bankstown", "Barcelona", "Bari-Palese", "Barnaul", "Barra", "Barranquilla-Aeropuerto Int´l Ernesto Cortissoz", "Basel/Mulhouse", "Basel/Mulhouse", "Baton Rouge Metroplitan", "Beauvais/Tille", "Beijing – Capital", "Beira", "Beirut", "Belfast", "Belfast", "Belfast City", "Belgrade", "Belize-Phillip SW Goldson", "Bellingham", "Belo Horizonte – Pampulha", "Belo Horizonte – Tancredo Neves Int´l",
"Benbecula", "Benghazi – Benina", "Bergen, Flesland", "Bergerac-Roumaniere", "Berlin – Schönefeld", "Berlin – Tegel", "Berlin – Tempelhof", "Bermuda", "Bern", "Beziers/Vias", "Biak-Frans Kaisiepo", "Biarritz/Bayone/Anglet", "Bilbao", "Billings Logan", "Billund", "Binghamton", "Bintulu", "Birmingham", "Birmingham", "Bishkek-Manas", "Bismark Municipal", "Bissau-Osvaldo Vieira", "Blackbushe", "Blackpool", "Blantyre-Chileka", "Bloemfontein", "Bluefield – Mercer County", "Boa Vista Int´l", "Bodø", "Boeing Field/King County Int´l", "Bogotá-El Dorado", "Boise", "Bologna-G Marconi", "Bonriki Int´l", "Bordeaux/Merignac", "Borlänge", "Bornholm-Roenne", "Boston-Logan", "Bourgas", "Bourges", "Bournemouth", "Bozeman", "Bradford Regional", "Brasilia Int´l – Presidente Juscelino Kubitschek", "Bratislava – M R Stefanik", "Brazzaville – Maya Maya", "Bremen – Flughafen Bremen", "Brest/Guipavas", "Brindisi", "Brisbane", "Brisbane – Archerfield", "Bristol", "Bristol – Filton", "Brive – La Roche", "Brno-Turany", "Brownsville/South Padre Island Int´l", "Brunei-Bandar Seri Begawan", "Brussels", "Brussels-South Charleroi", "Bucaramanga – Palo Negro", "Bucharest – Baneasa", "Bucharest – Otopeni", "Budapest – Ferihegy", "Buenos Aires – Aeropuerto Ministro Pistarini Int´l Ezeiza", "Buenos Aires – Don Torcuato", "Buffalo Niagara Int´l", "Bujumbura", "Bulawayo", "Burbank-Glendale-Pasedena", "Burlington", "Cairns", "Cairo", "Calgary", "Cali-Alfonso Bonilla Aragón", "Calicut", "Calvi – Sainte Catherine", "Camagüey-Ignacio Agramonte", "Cambridge", "Camden", "Campbeltown", "Campeche – Ingeniero Alberto Acuna Ongay Int´l", "Campo Grande",
"Canberra", "Cancun Int´l", "Canefield", "Cannes", "Cape Town", "Caracas-Maiquetia Simon Bolivar", "Carcassonne", "Cardiff", "Carlisle", "Cartagena-Rafael Nunez", "Casablanca – Mohammed V", "Casper/Natrona County Int´l", "Castres – Mazamet", "Catania-Fontanarossa", "Cayenne – Rochambeau", "Cayo Largo-Vilo Acuña Int´l", "Chambery/Aix les Bains", "Champaign – Willard", "Chania K Daskalogiannis", "Channel Islands – Alderney", "Channel Islands – Guernsey", "Channel Islands – Jersey", "Charleston-Yeager", "Charlotte/Douglas Int´l", "Chattanooga Metropolitan", "Chavenay", "Cheju – Jeju", "Chelyabinsk – Balandino", "Chengdu/Shuangliu", "Chennai/Madras – Meenambakam", "Cherbourg-Maupertus", "Chester", "Chetumal", "Cheyenne", "Chiang Mai Int´l", "Chiang Rai", "Chicago Midway", "Chicago-O´Hare", "Chisinau", "Chittagong – Shah Amanat Int´l", "Christchurch Ltd", "Châteauroux/Déols-Marcel Dassault", "Ciego de Avila-Maximo Gomez Int´l", "Cienfuegos – Jamie González Int´l", "Cincinnati/N Kentucky Int´l", "City of Derry – Londonderry", "Ciudad del Carmen", "Ciudad Obregón", "Ciudad Victoria", "Clermont Ferrand Auvergne", "Cleveland – Hopkins", "Cochin", "Cocos Islands", "Coimbatore", "Colima", "Colmar-Houssen", "Cologne/Bonn", "Colorado Springs", "Columbia Metropolitan", "Columbus – Port Columbus Int´l", "Columbus-Golden Triangle Regional", "Conakry-Gbessia", "Concepcion", "Constanta-Mihail Kogalniceanu", "Constantine", "Cook Is-Rarotonga", "Coolangatta – Gold Coast", "Copenhagen Roskilde", "Copenhagen – Kastrup", "Cordoba", "Cordoba – Ambrosio l y Taravella", "Corfu I Kapodistrias", "Cork", "Corpus Christi Int´l", "Cortez Municipal", "Corumba", "Cotonou", "Coventry – West Midlands", "Cozumel", "Crotone", "Crown Point", "Cruzeiro do Sul Int´l", "Cuernavaca", "Cumberland Regional", "Cuneo-Levaldigi", "Curacao – Hato", "Curitiba – Afonso Pena", "Dakar-Yoff – Leopol Sedar Senghor Int´l", "Dalaman", "Dalian – Zhoushuizi", "Dallas Love Field", "Dallas/Fort Worth", "Damascus", "Dammam – King Fahd", "Dane County Regional", "Dar-es-Salaam", "Darwin Int´l", "Davao Int´l", "Dayton", "Daytona Beach Int´l", "Deauville/Saint Gatien", "Decatur",
"Delhi – Indira Ghandi", "Denver", "Des Moines", "Detroit City", "Detroit Metropolitan Wayne County", "Dhahran", "Dhaka – Zia", "Dijon-Bourgogne Aéroport", "Dinard/Plertuit/St Malo", "Djerba-Zarzis", "Djibouti – Ambouli", "Dnepropetrovsk", "Doha", "Dole/Tavaux", "Donegal Int´l", "Dortmund – Wickede", "Dothan Regional", "Douala", "Dresden", "Dubai", "Dublin", "Dubois-Jefferson County", "Dubrovnik", "Dubuque Regional", "Dundee", "Dunedin Ltd", "Durango – La Plata County", "Durban", "Dushanbe", "Düsseldorf", "Düsseldorf Express- Mönchengladbach", "East London", "East Midlands", "Eastern Iowa", "Edinburgh", "Edmonton", "Egilsstadir", "Eilat-J Hozman", "Eindhoven", "Ekaterinburg – Koltcovo", "El Paso", "El Salvador Int´l", "Elmira/Coring Regional", "Enontekiö", "Enschede Twente", "Entebbe", "Epinal/Mirecourt", "Erfurt", "Erie", "Esbjerg", "Essen/Mulheim", "Essendon", "Evansville Regional", "Exeter", "Fairbanks Int´l", "Faleolo", "Fargo – Hector", "Farnborough", "Faro", "Fayetteville Municipal – Drake Field", "Fayetteville Regional", "Fayetteville – Lincoln County Regional", "Fes Saiss", "Fiji – Suva Nausori Int´l", "Fiji-Nadi", "Flagstaff Pulliam", "Flamingo", "Flint – Bishop", "Florence Regional", "Florence – Amerigo Vespucci", "Flores", "Forli", "Fort Collins-Loveland Municipal", "Fort Lauderdale-Hollywood Int´l", "Fort McMurray", "Fort Myers-SW Florida Int´l", "Fort Pierce – St Lucie County Int´l", "Fort Smith", "Fort Wayne", "Fortaleza", "Foz do Iguaçu-Cataratas Int´l", "Franceville – Mvengue", "Francistown", "Frankfurt", "Frankfurt-Hahn", "Freetown-Lunghi", "Fresno Yosemite", "Friedrichshafen/Lowental", "Fua´amotu Int´l", "Fuerteventura", "Fujairah", "Fukui", "Funchal -o da Madeira", "Gaborone-Seretse Khama", "Gainesville Regional", "Galway", "Garoua", "Gaya",
"Gdansk-Trojmiasto Ltd", "Geilo – Dagali", "Geneva", "Genoa", "George", "Georgetown – Cheddi Jagan Int´l", "Gerona-Costa Brava", "Gibraltar", "Glasgow Ltd", "Glasgow – Prestwick", "Gloucestershire", "Goa – Dabolim", "Gomel (Pokalubichi)", "Gorna Orjahovica", "Gran Canaria", "Granada", "Grand Bahama", "Grand Cayman-Owen Roberts Int´l", "Grand Forks Int´l", "Grand Junction – Walker Field", "Grand Rapids/Kent County Int´l", "Grand Turk", "Grande Case – L´Esperance", "Grant County", "Grantley Adams Int´l", "Graz", "Great Falls", "Greater Los Angeles/March GlobalPort", "Greater Rochester Int´l", "Greenville Spartanburg", "Grenada-Point Salines Int´l", "Grenoble/Saint-Geoirs", "Groningen Eelde", "Guadalajarra-Don Miguel Hidalgo", "Guam-Antonio BWon Pat Int´l", "Guangzhou Baiyun", "Guatemala City – La Aurora", "Guayaquil-Simon Bolivar", "Guaymas – General Jose Maria Yanez Intl", "Gulfport – Biloxi", "Göteborg City", "Göteborg-Landvetter", "Hagerstown Regional", "Haifa – U Michaeli", "Halifax Stanfield", "Hamburg", "Hamilton", "Hannover", "Hanoi – Noi Bai", "Harare", "Harbin – Taiping", "Harrisburg", "Harstad/Narvik – Evenes", "Hartford – Springfield – Bradley", "Hastings Municipal", "Hat Yai Int´l", "Haugesund", "Haverfordwest", "Helsinki – Malmi", "Helsinki – Vantaa", "Henderson", "Heraklion – Nikos Kazantzakis", "Hickory Regional", "Hierro", "Hilton Head Island", "Hiroshima", "Ho Chi Minh City – Tan Son Nhat Int´l", "Hobart", "Holguin-Frank Pais Int´l", "Hong Kong (HKG)", "Honolulu", "Horta", "Houston – George Bush Intercontinental", "Houston – William P Hobby", "Humberside Ltd", "Huntington Tri-State", "Huntsville", "Hurgadah", "Hyderabad", "Ibiza", "Ile d´Yeu – Grand Phare", "Indianapolis", "Innsbruck", "Inverness-Dalcross", "Inyokern – Kern County", "Ioannina National", "Ipoh – Sultan Azlan Shah", "Iquitos", "Irkutsk", "Islamabad", "Islay", "Isle of Man", "Isles of Scilly-St Mary´s", "Istanbul – Atatürk", "Ithaca – Tompkins County", "Ivalo Int´l", "Izmir – Adnan Menderes", "Jackson Hole", "Jackson Int´l", "Jacksonville", "Jaipur – Sanganeer", "Jakarta – Halim Perdanakusuma Int´l", "Jakarta – Soekarno Hatta", "Jeddah – King Abdulaziz",
"Joe Foss Field-Sioux Falls", "Joensuu", "Johannesburg", "Johnstown – Cambria County", "Johor Bahru – Sultan Ismail", "Jyvaskyla", "Jönköping", "Kabul-Khwaja Rawash", "Kajaani", "Kalamazoo/Battle Creek Int´l", "Kalmar", "Kano – Mallam Aminu Kano", "Kansas City", "Kansas City Downtown", "Kaohsiung Int´l", "Karachi", "Karaganda – Sary Arka", "Kariba", "Karlovy Vary", "Karonga", "Karup", "Kasane", "Kassel", "Kathmandu – Tribhuvan", "Katowice", "Kaunas", "Kavala-Megas Alexandros Int´l", "Kazan", "Kefallinia", "Keflavik", "Kelowna", "Kemi-Tornio", "Kerry", "Key West", "Khabarovsk – Novy", "Khartoum", "Kiev – Boryspil State", "Kiev – Zulhany", "Kigali", "Kilimanjaro", "Kimberley", "Kingston – Norman Manley", "Kinshasa-N´Djili", "Kinston – North Carolina Global Transpark", "Kirkenes", "Kirkwall", "Kiruna", "Kittilä", "Klagenfurt", "Klamath Falls Int´l", "Knock Int´l", "Knoxville – McGhee Tyson", "Kochi", "Kolkata – Netaji Subhas Chanra Bose Int´l", "Komatsu", "Kortrijk-Wevelgem/Flanders Int´l", "Kos – Ippokratis", "Kosice", "Kota Bharu – Sultan Ismail Petra", "Kota Kinabalu Int´l", "Kotoka", "Krakow-Balice", "Krasnoyarsk", "Kristianstad – Everod", "Krivij Rig", "Kruunupyy – Kokkola-Pietarsaari", "Kuala Lumpur – KLIA", "Kuala Lumpur – Sultan Abdul Aziz Shah", "Kuala Terengganu – Sultan Mahmud", "Kuantan – Sultan Haji Ahmad Shah", "Kuching Int´l", "Kumamoto", "Kumasi", "Kunming – Wujiaba", "Kuopio", "Kuressaare", "Kuusamo", "Kuwait", "Kärdla", "La Ceiba – Golson", "La Coruña", "La Crosse Municipal", "La Havana – Jose Marti", "La Palma", "La Paz-El Alto", "La Paz-Manuel de Leon", "La Rochelle – Ile de Ré", "Laayoune Hassan", "Labuan", "Lae", "Lafayette Regional", "Lagos – Murtala Muhammed", "Lahad Datu", "Lahore – Allama Iqbal", "Lahr – Black Forest", "Lake Tahoe",
"Lakselv – Banak", "Lambarene", "Lamezia", "Lancaster", "Langkawi", "Lannion", "Lanseria", "Lansing – Capital City", "Lanzarote", "Lappeenranta", "Laredo Int´l", "Larnaca", "Las Vegas – McCarran", "Launceston", "Le Bourget", "Le Havre/Octeville", "Le Touquet-Côte d´Opale", "Leeds Bradford", "Lehigh Valley", "Leipzig/Halle", "Lelystad", "Lexington/Blue Grass", "Libreville-Leon M´Ba Int´l", "Liepaja", "Lihue", "Lille", "Lilongwe", "Lima – Jorge Chavez", "Limnos", "Limoges/Bellegarde", "Limon", "Linz – Blue Danube", "Lisbon", "Little Rock National", "Liverpool – John Lennon", "Livingstone", "Liège", "Ljubljana D D", "Ljubljana D Dndoza-El Plumerillo", "Lome-Tokoin", "London – Biggin Hill", "London – City", "London – Gatwick", "London – Heathrow", "London – Luton", "London – Manston", "London – Southend", "London – Stansted", "Long Beach", "Long Island – MacArthur", "Lorain County Regional", "Lorient/Lann-Bihoué", "Los Angeles", "Louisville", "Luanda – 4 de Fevereiro", "Lubbock", "Lucknow – Amausi", "Luebeck – Blankensee", "Lugano", "Luleå-Kallax Cargo", "Lusaka", "Luxembourg-Findel", "Luxor", "Lydd", "Lynchburg Regional", "Lyon – Aéroport Lyon-Saint Exupéry", "Lyon/Bron Int´l", "Maastricht Aachen", "Macau", "Mackay", "Mactan – Cebu Int´l", "Madrid – Barajas", "Madrid – Cuatro Vientos", "Magadan Sokol", "Makedonia-Thessaloniki", "Malabo", "Malaga", "Male", "Malmö – Sturup", "Malta Int´l", "Manado – Sam Ratulangi", "Managua – Augusto Cesar Sandino", "Manaus-Eduardo Gomes Int´l", "Manchester", "Manchester", "Mandalay", "Manila – Ninoy Aquino Int´l", "Manzanillo-Sierra Maestra Int´l", "Maputo", "Marathon", "Maribor Aerodrom", "Mariehamn", "Marrakech – Menara", "Marseille/Provence", "Martinique-Lamentin", "Maseru-Moshoeshoe 1", "Mason City Municipal", "Matamoros – General Servando Canales", "Matsapha", "Matsumoto", "Maun", "Mazatlan – General Rafael Buelna", "Mbandaka", "McAllen – Miller", "Medan-Polonia", "Medellin – Jose Maria Cordova", "Melaka – Batu Berendam", "Melbourne Int´l", "Melbourne – Tullamarine", "Melilla", "Melo – Aeropuerto Int´l de Cerro Largo", "Melville Hall", "Memphis", "Menorca", "Mercedita", "Merida – Licenciado Manuel Crecencio Rejon Int´l",
"Meridian Regional-Key Field", "Metz/Nancy/Lorraine", "Mexico-Benito Juarez", "Miami", "Midland", "Mikkeli City", "Milan – Orio Al Serio", "Milan-Linate", "Milan-Malpensa", "Milwaukee – General Mitchell Int´l", "Minneapolis-St Paul Int´l", "Minot", "Minsk National", "Miri", "Misawa", "Missoula Int´l – Johnson-Bell Field", "Mitilini", "Mobile Downtown", "Mobile Regional", "Modesto City County", "Mogadishu", "Molde-Aaro", "Mombasa – Moi Int´l", "Monaco Heliport", "Moncton", "Monrovia-Roberts", "Montego Bay – Sangster", "Monterrey", "Montevideo – Carrasco", "Montpellier – Mediterranée Aéroport", "Montréal–Mirabel", "Montréal–Pierre Elliott Trudeau", "Montserrat", "Moorabbin", "Mora – Siljan", "Moscow – Domodedovo", "Moscow – Sheremetyevo", "Moscow – Vnukovo", "Mostar", "Mount Isa", "Mumbai/Bombay – Chhatarpati Shivaji", "Munich", "Murmansk", "Muscat-Seeb", "Münster-Osnabrück", "Nagoya", "Nairobi – Jomo Kenyatta", "Nampula", "Nancy/Essey Aéroport", "Nanjing Lukou Co Ltd", "Nantes-Atlantique", "Nantucket Memorial", "Naples Municipal", "Naples-Capodichino", "Narssarssuaq", "Nashville", "Nassau", "Natal – Augusto Severo", "Nauru", "Ndola and Kitwe", "Nevis – Newcastle", "New Caledonia", "New Haven", "New Orleans – Louis Armstrong", "New York – John F Kennedy", "New York-La Guardia", "Newark", "Newcastle", "Newcastle", "Newquay Cornwall", "Niamey Diori Hamani", "Nice/Cote D´Azur", "Niigata", "Nimes/Arles/Camargue", "Nogales", "Norfolk", "Norrköping", "North Platte Regional", "Northern Maine Regional", "Norwich", "Nouadhibou Aerodrome", "Nouakchott Aerodrome",
"Novosibirsk Tolmachevo", "Nuevo Laredo – Quetzalcoatl", "Nuremberg", "N´Djamena", "Oakland", "Oaxaca", "Odense", "Odessa", "Ohrid", "Okayama", "Okinawa/Naha", "Oklahoma City-Will Rogers World", "Olbia-Costa Smerelda", "Omaha-Eppley Airfield", "Ontario Int´l", "Oporto – Fr SA Carneiro", "Orkney Is – Eday Airstrip", "Orkney Is – N Ronaldsay Airstrip", "Orlando", "Orlando/Sanford Central Florida Regional", "Osaka – Itami", "Osaka – Kansai Co Ltd", "Oslo – Gardermoen", "Ostend", "Ostrava Int´l", "Ottawa ", "Ouagadougou", "Ouarzazate", "Oujda Angads", "Oulu", "Oxford", "Paderborn/Lippstadt", "Pago Pago", "Palanga", "Palembang – Sultan Mahmud Badaruddin II", "Palermo -o Falcone e Borsellino", "Palm Beach Int´l", "Palm Springs Regional", "Palma De Mallorca", "Pamplona", "Panama City-Tocumen", "Panama City/Bay County Int´l", "Paphos", "Paramaribo – Johan Adolf Pengel Int´l", "Pardubice", "Paris – Charles De Gaulle", "Paris – Orly", "Paris – Pontoise", "Parkersburg – Mid-Ohio Valley Regional", "Paro", "Patna", "Patras/Araxos National", "Pau – Pyrenees", "Penang", "Pendleton/Eastern Oregon Regional", "Pensacola", "Penzance Heliport", "Peoria – Greater Peoria Regional", "Pereira-Matecana", "Perpignan/Rivesaltes", "Perth Int´l – Westralia Corporation", "Peru/Grissom Aeroplex", "Peshawar", "Petropavlovsk-Kamchatsky – Yelizovo", "Philadelphia", "Phnom Penh", "Phoenix Sky Harbor Int´l", "Phuket Int´l", "Piarco", "Piedmont Triad Int´l", "Piestany", "Pilanesburg", "Pisa", "Pittsburgh", "Piura", "Plattsburgh Clinton County", "Plattsburgh Int´l AFB", "Plovdiv", "Plymouth City", "Point-a-Pitre Le Raizet", "Pointe – Noire Aerodrome", "Poitiers – Biard", "Ponta Pora Int´l", "Pontianak – Supadio", "Poprad-Tatry", "Pori", "Port Angeles-William R Fairchild Int´l", "Port Elizabeth", "Port Gentil", "Port Harcourt", "Port Moresby/Jacksons", "Port Vila – Bauerfield", "Port-au-Prince", "Portland", "Porto Alegre – Salgado Filho Int´l", "Porto Santo", "Poughkeepsie – Dutchess County", "Poza Rica – Tajin", "Poznan-Lawica", "Prague-Ruzyne", "Prince George", "Providence-Theodore Francis Green", "Providenciales", "Provincetown Municipal", "Puebla – Hermanos Serdan", "Puerto Montt-El Tepual",
"Puerto Plata", "Puerto Vallarta Int´l – Gustavo Diaz Ordaz", "Pula", "Punta Arenas", "P´yongyang-Sunan", "Quaid-e-Azam", "Querétaro – Ingeniero F Espinoza Gutierrez Int´l", "Quimper – Pluguffan", "Quito-Mariscal Sucre", "Québec", "Rabat-Sale", "Rabaul-Lakunai", "Rafha", "Raleigh – Durham Int´l", "Rapid City Regional", "Ras Al Khaimah", "Reading Regional", "Recife – Guararapes/Gilberto Freyre Int´l", "Redmond Municipal – Roberts Field", "Reims/Champagne", "Rennes/Saint-Jacques", "Reno/Tahoe", "Reus", "Reykjavik", "Rhinelander – Oneida County", "Rhodes-Diagoras", "Richmond", "Rickenbacker", "Riga", "Rijeka-Riviera Kvarner", "Rimini – Miramareo", "Rio Branco – Presidente Medici", "Rio De Janeiro – Santos Dumont", "Rio de Janeiro-Galeão – Antonio Carlos Jobim International A", "Riyadh – King Khaled", "Roanoke Regional", "Rochester", "Rock Sound", "Rocky Mount/Wilson Regional", "Rodez/Marcillac", "Roland Garros", "Rome – Ciampino", "Rome-Leonardo da Vinci Fiumicino", "Rosh Pina – Mahanaim Ben Yaakov", "Roswell Industrial Air Center", "Rotterdam", "Rovaniemi", "Rzeszow-Jasionka", "Saarbrucken", "Sabadell", "Sacramento County System", "Saint Brieuc-Armor", "Saint Croix – Henry E Rohlsen", "Saint Etienne/Boutheon", "Saint Kitts – Robert Bradshaw", "Saint Louis – Lambert Int´l", "Saint Lucia – Hewanorra", "Saint Lucia-Vigie", "Saint Maarten-Princess Juliana", "Saint Thomas-Cyril E King", "Saint Vincent-E T Joshua", "Saipan", "Salalah", "Salamanca", "Salina", "Salisbury/Ocean City Regional", "Salt Lake City", "Salta", "Salzburg – W A Mozart", "Samarkand", "Samos", "San Andres – Gustavo Rojas Pinilla", "San Angelo Regional/Mathis Field", "San Antonio", "San Diego", "San Francisco", "San Javier/Murcia", "San Jose", "San Jose – Juan Santamaria", "San José – Tobias Bolanos", "San Juan – Luiz Munoz Marin", "San Luis County Regional", "San Pedro Sula – La Mesa", "San Sebastian – Fuenterrabia", "Sana´a", "Sandakan", "Sandefjord – Torp", "Santa Ana – John Wayne", "Santa Barbara", "Santa Maria", "Santander – Parayas", "Santarém Int´l", "Santiago", "Santiago – Antonio Maceo", "Santiago – Arturo Merino Benitez", "Santo Domingo-Las Americas",
"Sao Tome", "Sarajevo", "Saranac Lake-Adirondack Regional", "Sarasota Bradenton Int´l", "Saratov – Tsentralny", "Saskatoon", "Satu Mare", "Savannah", "Savonlinna", "Seattle/Tacoma", "Sebha", "Seinäjoki", "Selebi Phikwe", "Sendai", "Seoul – Incheon", "Seoul – Kimpo", "Seville – San Pablo", "Seychelles Int´l", "Sfax-el-Maou", "Shanghai – Hong Qiao", "Shanghai – Pudong", "Shannon", "Sharjah", "Sheffield City", "Shenyang – Taoxian", "Shenzhen – Baoan", "Shetland Island – Sumburgh", "Shiraz – Shahid Dastghaib", "Shoreham", "Shreveport Regional", "Sibu", "Sidney Municipal", "Singapore – Changi", "Sion", "Sioux Falls Regional", "Sioux Gateway", "Sir Seewoosagur Ramgoolam", "Skive", "Skopje", "Sliac", "Sligo Regional", "Sofia EAD", "Sondre Stromfjord/Kangerlussuaq", "South Bend Regional", "South Caicos", "Southampton", "Split", "Spokane", "Springfield – Branson Regional", "St Moritz – Samedan", "St Nazaire/Montoir", "St Petersburg-Clearwater Int´l", "St Petersburg-Pulkovo", "St Tropez du Golfe", "St. John's", "State College", "Stauning Vestjyllands", "Stavanger", "Stewart", "Stockholm – Arlanda", "Stockholm – Bromma", "Stockholm – Skavsta", "Stord – Soerstokken", "Stornoway", "Strasbourg", "Stuttgart", "Sundsvall-Härnösand", "Surabaya-Juanda Int´l", "Surakarta – Adi Sumarmo Wiryokusumo", "Svalbard-Longyear", "Swansea", "Sydney", "Syracuse – Hancock", "Szczecin – Goleniow", "São Paulo – Congonhas Int´l", "São Paulo – Guarulhos Int´l", "São Paulo – Viracopos", "Sønderborg", "Tabarka-7 Novembre Int´l", "Tahiti – Faa´a", "Taipei-Chiang Kai Shek", "Tallinn", "Tamale", "Tampa Int´l", "Tampere-Pirkkala", "Tanga", "Tangier – Boukhalef", "Tarbes-Lourdes-Pyrennes", "Targu Mures", "Tartu Raadi Ltd", "Tashkent – Yuzhny", "Tawau", "Tbilisi", "Teesside", "Tegucigalpa-Toncontin", "Tehran – Mehrabad", "Tehuacán", "Tel Aviv-Ben Gurion", "Tel Aviv-Dov Hoz", "Tenerife North", "Tenerife South", "Tennant Creek", "Tepic", "Thiruvanthapuram Int´l", "Thisted", "Thunder Bay", "Tianjin – Binhai", "Tirana – Rinas Mother Teresa", "Tiree", "Tiruchirapalli", "Tokyo – Haneda Int´l", "Tokyo-Narita Int´l", "Toledo Express", "Toluca – Licenciado Adolfo Lopez Mateos Int´l", "Toronto", "Toulon/Hyeres",
"Toulouse-Blagnac", "Townsville Int´l", "Toyama", "Tozeur – Nefta", "Trenton – Mercer County", "Treviso-San Angelo", "Tri-Cities Regional", "Trieste – R Dei Legionari", "Tripoli", "Tromsø", "Trondheim/Vaernes", "Tucson", "Tulcea", "Tulsa", "Tunis – Carthage", "Tupelo Municipal", "Turin", "Turku", "Tuxtla Gutiérrez – Francisco Sarabia", "Tyler Pounds Regional", "Tyumen – Roshchino", "Uherské Hradiste – Kunovice", "Ulan Bator – Buyant Ukha", "Ulyanovsk-Vostochny", "Umeå", "Upington", "Uruapan – Licenciado Y Gen Ignacio Lopez Rayon", "Urumqi – Diwopu", "Utica – Oneida County", "Vaasa", "Vagar", "Valence/Chabeuil", "Valencia", "Valladolid", "Vancouver", "Varadero-Juan G Gomez Int´l", "Varanasi", "Varkaus", "Varna Ltd", "Venice-Aeroporto Marco Polo", "Vero Beach", "Verona-Valerio Catullo", "Vichy/Charmeil", "Victoria Falls", "Victoria, CA", "Vienna", "Vientiane – Wattay", "Vigo", "Vilnius Int´l", "Virgin Gorda", "Viseu", "Vitoria Int´l", "Vladivostok (JSC Vladivostok Air)", "Vojens – Skrydstrup", "Växjö – Urasa", "Wakkanai", "Wallis Hihifo", "Warsaw – Frederic Chopin", "Washington – Dulles", "Washington – Ronald Reagan National", "Waterford Regional", "Waterloo Municipal", "Watertown Int´l", "Wausau/Central Wisconsin Regional", "Wellington", "Wenatchee/Pangborn Memorial", "Westchester County", "Westerland-SFG Sylter Flughafen GmbH & Co", "Wichita Mid-Continent", "Wick Aerodrome", "Wilkes-Barre – Scranton Int´l", "Williams Gateway", "Williamsport Regional", "Wilmington Int´l", "Windhoek – Hosea Kutako", "Windsor, CA", "Winnipeg", "Winston-Salem", "Worcester Regional", "Wroclaw-Strachowice", "Yangon", "Yaounde-Nsimalen", "Yerevan-Zvartnots", "Yogyakarta-Adi Sucipto", "Yuzhno-Sakhalinsk", "Örnsköldsvik", "Östersund")

airportCodes = ("AAL", "AAR", "ABZ", "AUH", "ACA", "ADA", "ADD", "ADL", "ADE", "POW", "AGA", "AGF", "AGR", "AMD", "AJA", "CAK", "ALS", "ALB", "LBI", "ABQ", "ACI", "ALP", "AES", "ESF", "ALY", "AXD", "AHO", "ALG", "ALC", "ASP", "ALA", "LEI", "AOR", "ACH", "AMA", "SID", "AMM", "ATQ", "SPL", "ANC", "AOI", "ANG", "ESB", "AAE", "NCY", "AYT", "TNR", "SJF", "ANF", "ANR", "ATW", "AQJ", "ARW", "ARI", "ARH", "AUA", "AVL", "ASB", "ASM", "OVD", "ASU", "ASW", "AHN", "ATH", "ATH", "ATL", "ACY", "AKL", "AGB", "AGS", "AUS", "AVN", "BJZ", "FKB", "SDA", "BAH", "BAK", "DPS", "BPN", "BWI", "BKO", "CMB", "BLR", "BKK", "BGR", "BGF", "BJL", "BWU", "BCN", "BRI", "BAX", "BRR", "BAQ", "MLH", "BSL", "BTR", "BVA", "PEK", "BEW", "BEY", "BFS", "BFS", "BHD", "BEG", "BZE", "BLI", "PLU", "CNF", "BEB", "BEN", "BGO", "EGC", "SXF", "TXL", "THF", "BDA", "BRN", "BZR", "BIK", "BIQ", "BIO", "BIL", "BLL", "BGM", "BTU", "BHX", "BHM", "KGA", "BIS", "BXO", "BBS", "BLK", "BLZ", "BFN", "BLF", "BVB", "BOO", "BFI", "BOG", "BOI", "BLQ", "TRW", "BOD", "BLE", "RNN", "BOS", "BOJ", "BOU", "BOH", "BZN", "BFD", "BSB", "BTS", "BVZ", "BRE", "BES", "BDS", "BNE", "BNE", "BRS", "BRS", "BVE", "BRQ", "BRO", "BWN", "BRU", "CRL", "BGA", "BBU", "OTP", "BUD", "EZE", "DOT", "BUF", "BJM", "BUQ", "BUR", "BTV", "CNS", "CAI", "YYC", "CLO", "CCI", "CLY", "CMW", "CBG", "CDU", "CAL", "CPE", "CGR", "CBN", "CUN", "DCF", "CEQ", "CPT", "CCS", "CCF", "CWL", "CAX", "CTG", "CMN", "CPR", "DCM", "CTA", "CAY", "CYO", "CMF", "CMI", "CHQ", "ACI", "GCI", "JER", "CRW", "CLT", "CHA", "PAR", "CJU", "CEK", "CTU", "MAA", "CER", "CEG", "CTM", "CYS", "CNX", "CEI", "MDW", "ORD", "KIV", "CGP", "CHC", "CHR", "AVI", "CFG", "CVG", "LDY", "CME", "CEN", "CVM", "CFE", "CLE", "COK", "CCK", "CJB", "CLQ", "CMR", "CGN", "COS", "CAE", "CMH", "GTR", "CKY", "CCP", "CND", "CZL", "RAR", "OOL", "RKE", "CPH", "ODB", "COR", "CFU", "CRK", "CRP", "CEZ", "CMG", "COO", "CVT", "CZM", "CRV", "TAB", "CZS", "CVJ", "CBE", "CUF", "CUR", "CWB", "DKR", "DLM", "DLC", "DAL", "DFW", "DAM",
"OED", "MSN", "DAR", "DRW", "DVO", "DAY", "DAB", "DOL", "DEC", "DEL", "DEN", "DSM", "DET", "DTW", "DHA", "DAC", "DIJ", "DNR", "DJE", "JIB", "DNK", "DOH", "DLE", "CFN", "DTM", "DHN", "DLA", "DRS", "DXB", "DUB", "DUJ", "DBV", "DBQ", "DND", "DUD", "DRO", "DUR", "DYU", "DUS", "MGL", "ELS", "EMA", "CID", "EDI", "YEG", "EGS", "ETH", "EIN", "SVX", "ELP", "SAL", "ELM", "ENF", "ENS", "EBB", "EPL", "ERF", "ERI", "EBJ", "ESS", "MEB", "EVV", "EXT", "FAI", "APW", "FAR", "FAB", "FAO", "FYV", "FAY", "FYM", "FEZ", "SUV", "NAN", "FLG", "BON", "FNT", "FLO", "FLR", "FLW", "FRL", "FNL", "FLL", "YMM", "RSW", "FPR", "FSM", "FWA", "FOR", "IGU", "MVB", "FRW", "FRA", "HHN", "FNA", "FAT", "FDH", "TBU", "FUE", "FJR", "FKJ", "FNC", "GBE", "GLE", "GWY", "GOU", "GAY", "GDN", "DLD", "GVA", "GOA", "GRJ", "GEO", "GRO", "GIB", "GLA", "PIK", "GLO", "GOI", "GME", "GOZ", "LPA", "GRX", "FPO", "GCM", "GFK", "GJT", "GPZ", "GDT", "SFG", "MWH", "BGI", "GRZ", "GTF", "RIV", "ROC", "GSP", "GND", "GNB", "GRQ", "GDL", "GUM", "CAN", "GUA", "GYE", "GYM", "GPT", "GSE", "GOT", "HGR", "HFA", "YHZ", "HAM", "YHM", "HAJ", "HAN", "HRE", "HRB", "HAR", "EVE", "BDL", "HSI", "HDY", "HAU", "HAW", "HEM", "HEL", "HIR", "HER", "HKY", "VDE", "HXD", "HIJ", "SGN", "HBA", "HOG", "HKG", "HNL", "HOR", "IAH", "HOU", "HUY", "HTS", "HSV", "HRG", "HYD", "IBZ", "IDY", "IND", "INN", "INV", "IYK", "IOA", "IPH", "IQT", "IKT", "ISB", "ILY", "IOM", "ISC", "IST", "ITH", "IVL", "ADB", "JAC", "JAN", "JAX", "JAI", "HLP", "JKT", "JED", "FSD", "JOE", "JNB", "JST", "JHB", "JYV", "JKJ", "KBL", "KAJ", "AZO", "KLR", "KAN", "MCI", "MKC", "KHH", "KHI", "KGF", "KAB", "KLV", "KGJ", "KRP", "BBK", "KSF", "KTM", "KTW", "KUN", "KVA", "KZN", "EFL", "KEF", "YLW", "KEM", "KIR", "EYW", "KHV", "KRT", "KBP", "IEV", "KGL", "JRO", "KIM", "KIN", "FIH", "ISO", "KKN", "KOI", "KRN", "KTT", "KLU", "LMT", "NOC", "TYS", "KCZ", "CCU", "KMQ", "FIA", "KGS", "KSC", "KBR", "BKI", "ACC", "KRK", "KJA", "KID", "KWG", "KOK", "KUL", "SZB", "TGG", "KUA", "KCH", "KMJ", "KMS", "KMG", "KUO", "URE", "KAO", "KWI", "KDL", "LCE", "LCG", "LSE", "HAV", "SPC", "LPB",
"LAP", "LRH", "EUN", "LBU", "LAE", "LFT", "LOS", "LDU", "LHE", "LHA", "TVL", "LKL", "LBQ", "SUF", "LNS", "LGK", "LAI", "HLA", "LAN", "ACE", "LPP", "LRD", "LCA", "LAS", "LST", "LBG", "LEH", "LTQ", "LBA", "ABE", "LEJ", "LEY", "LEX", "LBV", "LPX", "LIH", "LIL", "LLW", "CLX", "LXS", "LIG", "LMH", "LNZ", "LIS", "LIT", "LPL", "LVI", "LGG", "LJU", "MDZ", "LFW", "BQH", "LCY", "LGW", "LHR", "LTN", "MSE", "SEN", "STN", "LGB", "ISP", "LPR", "LRT", "LAX", "SDF", "LAD", "LBB", "LKO", "LBC", "LUG", "LLA", "LUN", "LUX", "LXR", "LYX", "LYH", "LYS", "LYS", "MST", "MFM", "MKY", "NOP", "MAD", "MCV", "GDX", "SKG", "SSG", "AGP", "MLE", "MMX", "MLA", "MDC", "MGA", "MAO", "MHT", "MAN", "MDL", "MNL", "MZO", "MPM", "MTH", "MBX", "MHQ", "RAK", "MRS", "FDF", "MSU", "MCW", "MAM", "MTS", "MMJ", "MUB", "MZT", "MDK", "MFE", "MES", "MDE", "MKZ", "MLB", "MEL", "MLN", "MLZ", "DOM", "MEM", "MAH", "PSE", "MID", "MEI", "ETZ", "MEX", "MIA", "MAF", "MIK", "BGY", "LIN", "MXP", "MKE", "MSP", "MOT", "MSQ", "MYY", "MSJ", "MSO", "MJT", "BFM", "MOB", "MOD", "MGQ", "MOL", "MBA", "MCM", "YQM", "ROB", "MBJ", "MTY", "MUD", "MPL", "YMX", "YUL", "MNI", "MBW", "MXX", "DME", "SVO", "VKO", "OMO", "ISA", "BOM", "MUC", "MMK", "MCT", "MSR", "NGO", "NBO", "APL", "ENC", "NKG", "NTE", "ACK", "APF", "NAP", "UAK", "BNA", "NAS", "NAT", "INU", "NLA", "NEV", "NOU", "HVN", "MSY", "JFK", "LGA", "EWR", "NTL", "NCL", "NQY", "NIM", "NCE", "KIJ", "FNI", "NOG", "ORF", "NRK", "LBF", "PQI", "NWI", "NDB", "NKO", "OVB", "NLD", "NUE", "NDH", "OAK", "OAX", "ODE", "ODS", "OHD", "OKJ", "OKA", "OKC", "OLB", "OMA", "ONT", "OPO", "EOI", "NRL", "MCO", "SFB", "ITM", "KIX", "GEN", "OST", "OSR", "YOW", "OUA", "OZZ", "OUD", "OUL", "OXF", "PAD", "PPG", "PLQ", "PLM", "PMO", "PBI", "PSP", "PMI", "PNA", "PTY", "PFN", "PFO", "PBM", "PED", "CDG", "ORY", "POX", "PKB", "PBH", "PAT", "GPA", "PUF", "PEN", "PDT", "PNS", "PZE", "PIA", "PEI", "PGF", "PER", "IND", "PEW", "PKC", "PHL", "PNH", "PHX", "HKT", "POS", "GSO", "PZY", "NTY", "PSA", "DTP", "PIU", "PLB", "PBG", "PDV", "PLH", "PTP", "PNR", "PIS", "PMG", "PNK", "TAT", "POR", "CLM", "PLZ",
"POG", "PHC", "POM", "VLI", "PAP", "PDX", "POA", "PXO", "POU", "PAZ", "POZ", "PRG", "YXS", "PVD", "PLS", "PNN", "PBC", "PMC", "POP", "PVR", "PUY", "PUQ", "FNJ", "KHI", "QRO", "UIP", "UIO", "YQB", "RBA", "RAB", "RAH", "RDU", "RAP", "RKT", "RDG", "REC", "RDM", "RHE", "RNS", "RNO", "REU", "REK", "RHI", "RHQ", "RIC", "LCK", "RIX", "RJK", "RMI", "RBR", "GIG", "GIG", "RUH", "ROA", "RST", "RSD", "RWI", "RDZ", "RUN", "CIA", "FCO", "RPN", "ROW", "RTM", "RVN", "RZE", "SCN", "QSA", "SMF", "SBK", "STX", "EBU", "SKB", "STL", "UVW", "SLU", "SXM", "STT", "SVD", "SPN", "SLL", "SLM", "SLN", "SBY", "SLC", "SLA", "SZG", "SKD", "SMI", "ADZ", "SJT", "SAT", "SAN", "SFO", "MJV", "SJC", "SJO", "SYQ", "SJU", "SBP", "SAP", "EAS", "SAH", "SDK", "TRF", "SNA", "SNA", "SMA", "SDR", "STM", "SCQ", "SCU", "SCL", "SDQ", "TMS", "SJJ", "SLK", "SRQ", "RTW", "YXE", "SUJ", "SAV", "SVL", "SEA", "SEB", "SJY", "PKW", "SDJ", "ICN", "SEL", "SVQ", "SEZ", "SFA", "SHA", "PVG", "SHN", "SHJ", "SZD", "SHE", "SZX", "LSI", "SYZ", "ESH", "SHV", "SBW", "SDY", "SIN", "SIR", "FSD", "SUX", "MRU", "SQW", "SKP", "SLD", "SXL", "SOF", "SFJ", "SBN", "SLX", "SOU", "SPU", "GEG", "SGF", "SMV", "SNR", "PIE", "LED", "LTT", "YYT", "SCE", "STA", "SVG", "SWF", "ARN", "BMA", "NYO", "SRP", "STY", "- S", "STR", "SDL", "SUB", "SOC", "LYR", "SWS", "SYD", "SYR", "SZZ", "CGH", "SAO", "VCP", "SGD", "TBJ", "PPT", "TPE", "TLL", "ACC", "TPA", "TMP", "TGT", "TNG", "LDE", "TGM", "TAY", "TAS", "TWU", "TBS", "MME", "TGU", "THR", "TCN", "TLV", "SDV", "TFN", "TFS", "TCA", "TPQ", "TRV", "TED", "YQT", "TSN", "TIA", "TRE", "TRZ", "HNT", "NRT", "TOL", "TLC", "YYZ", "TLN", "TLS", "TSV", "TOY", "TOE", "TTN", "TSF", "TRI", "TRS", "TIP", "TOS", "TRD", "TUS", "TCE", "TUL", "TUN", "TUP", "TRN", "TRK", "TGZ", "TYR", "TJM", "UHE", "ULN", "ULY", "UME", "UTN", "UPN", "URC", "UCA", "VAA", "FAE", "VAF", "VLC", "VLL", "YVR", "VRA", "VNS", "VRK", "VAR", "VCE", "VRB", "VRN", "VHY", "VFA", "YYJ", "VIE", "VTE", "VGO", "VNO", "VIJ", "VSE", "VIT", "VVO", "SKS", "VXO", "WKJ", "WLS", "WAW", "IAD", "DCA", "WAT", "ALO", "ART", "CWA", "WLG", "EAT", "HPN", "GWT", "ICT", "WIC", "WBW", "IWA", "IPT", "ILM", "WDH", "YQG", "YWG", "INT", "ORH", "WRO", "RGN", "NSI", "EVN", "JOG", "UUS", "OER", "OS")

class Trip:
	def __init__(self, idx, date, price, outbound_duration, return_duration):
		self.idx = idx
		self.date = date
		self.price = price
		self.outbound_duration = outbound_duration
		self.return_duration = return_duration

def input_date_to_datetime(input_date):
	output_date = datetime.strptime(input_date,"%Y-%m-%d")
	return output_date.date()

def datetime_to_string(datetime_date):
	kayak_date = datetime_date.strftime("%Y-%m-%d")
	return kayak_date

# Functions relating to the sqlite database
#_______________________________________________________________________________
def connect_to_database(database_file):
	conn = None
	try:
		conn = sqlite3.connect(database_file)
		return conn
	except Error as error:
		print(error)
		return conn

def create_sql_table(conn, sql_table):
    try:
        cur = conn.cursor()
        cur.execute(sql_table)
    except Error as error:
        print("error creating table: " + str(error))

def create_trip(conn, trip_row_format):
	sql_command = ''' INSERT INTO
					all_trips(id, departure_date, price, outbound_duration, return_duration)
					VALUES(?, ?, ?, ?, ?) '''
	cur = conn.cursor()
	cur.execute(sql_command, trip_row_format)
	#print(cur.lastrowid)
	return cur.lastrowid

def create_date_summary(conn, date_summary):
	sql_command = ''' INSERT INTO
					date_summary(id, departure_date,cheapest_price, median_price, average_price)
					VALUES(?, ?, ?, ?, ?) '''
	cur = conn.cursor()
	cur.execute(sql_command, date_summary)
	return cur.lastrowid

#Functions used for scraping the webpage:
#_______________________________________________________________________________
def find_element_using_xpath(web_driver,element_xpath):
	web_element = WebDriverWait(web_driver, 60).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
	return web_element

def close_popup(web_driver):
	close_button_xpath = '//div[contains(@class, "Common-Widgets-Dialog-Dialog R9-Overlay flightsDriveBy fromBottom visible animate")]//button[contains(@id,"dialog-close")]'
	try:
		close_button = find_element_using_xpath(web_driver, close_button_xpath)
		close_button.click()
	except TimeoutException as ex:
		print("Exception has been thrown. " + str(ex))
		return

def get_prices(web_driver):
	# There was a StaleElementReferenceException that kept being thrown as a result of the page reloading
	# while the scraping was occurring. The try/except structures ensures that the data is obtained and
	# the script keeps going
	sleep(randint(5,7))
	price_xpath = '//span[contains(@id, "price-text")]'
	try:
		price_list = [price.text.replace('$','') for price in web_driver.find_elements_by_xpath(price_xpath) if price.text != '']
	except StaleElementReferenceException as ex:
		print("stale element reference exception while getting prices. Attempting again.")
		sleep(7)
		price_list = [price.text.replace('$','') for price in web_driver.find_elements_by_xpath(price_xpath) if price.text != '']
		#Goes through the prices and gets rid of the $ sign for all the elements
	price_list = list(map(int, price_list))
	return price_list

def get_flight_durations(web_driver):
	# There was a StaleElementReferenceException that kept being thrown as a result of the page reloading
	# while the scraping was occurring. The try/except structures ensures that the data is obtained and
	# the script keeps going
	sleep(randint(1,3))
	outbound_duration_xpath = '//div[contains(@id, "info-leg-0") ]//div[contains(@class, "duration")]/div[@class="top"]'
	return_duration_xpath = '//div[contains(@id, "info-leg-1") ]//div[contains(@class, "duration")]/div[@class="top"]'
	try:
		outbound_durations_list =[duration.text for duration in web_driver.find_elements_by_xpath(outbound_duration_xpath)]
	except StaleElementReferenceException as ex:
		print("stale element reference exception while getting outbound durations. Attempting again.")
		sleep(7)
		outbound_durations_list =[duration.text for duration in web_driver.find_elements_by_xpath(outbound_duration_xpath)]
	try:
		return_durations_list = [duration.text for duration in web_driver.find_elements_by_xpath(return_duration_xpath)]
	except StaleElementReferenceException as ex:
		print("stale element reference exception while getting return durations. Attempting again.")
		sleep(7)
		return_durations_list = [duration.text for duration in web_driver.find_elements_by_xpath(return_duration_xpath)]
	return outbound_durations_list, return_durations_list

def increment_date(web_driver, kayak_link,current_outbound_date, duration):
	#Randomly switching between two different methods of incrementing to try and stop Recptchas from appearing
	current_return_date = current_outbound_date + timedelta(days = duration)
	n = randint(1,7)

	if n>=3:
		kayak_link = "https://www.kayak.com/flights/" + airport_codes + "/" + datetime_to_string(current_outbound_date) + "/" + datetime_to_string(current_return_date)
		web_driver.get(kayak_link)
		print("new link")
		sleep(5)
	else:
		departure_date_inc_xpath = '//button[contains(@id, "dateRangeInput-start-inc")]'
		return_date_inc_xpath = '//button[contains(@id, "dateRangeInput-end-inc")]'
		submit_xpath = '//div[contains(@id, "submit")]'

		departure_date_inc_button = find_element_using_xpath(web_driver,departure_date_inc_xpath)
		departure_date_inc_button.click()
		return_date_inc_button = find_element_using_xpath(web_driver,return_date_inc_xpath)
		return_date_inc_button.click()
		date_submit_button = find_element_using_xpath(web_driver,submit_xpath)
		date_submit_button.click()

def scrape_page(web_driver, conn, current_outbound_date):
#Obtains prices and flight durations of flights and stores them in the database tables
	sleep(randint(8,10))
	prices = get_prices(web_driver)
	flight_durations = get_flight_durations(web_driver)
	print(prices)
	id_null = None
	if prices:
		create_date_summary(conn, (id_null, current_outbound_date, min(prices), median(prices), mean(prices)))
		for idx, price in enumerate(prices):
			create_trip(conn, (id_null, current_outbound_date, price,flight_durations[0][idx],flight_durations[1][idx]))
			conn.commit()

#main code:
#_______________________________________________________________________________
driver = webdriver.Chrome()
# Only works because I added Chrome to path. Maybe move it and figure the
# other way out to make it work better on the Raspberry Pi
conn = connect_to_database('FlightBotDB.sqlite')
cur = conn.cursor()

all_trips_table_sql = """ CREATE TABLE IF NOT EXISTS all_trips(
						 	id integer PRIMARY KEY,
							departure_date text,
							price integer,
							outbound_duration text,
							return_duration text
							); """
date_summary_table_sql = """ CREATE TABLE IF NOT EXISTS date_summary(
							id integer PRIMARY KEY,
							departure_date text,
							cheapest_price int,
							median_price int,
							average_price int
							); """

create_sql_table(conn, all_trips_table_sql)
create_sql_table(conn, date_summary_table_sql)


input_outbound_date = input("Enter a start date in YYYY-MM-DD format")
duration = 7;
#while True:
#	try:
#    	inputOrigin = int(input("Please enter the duration of your trip in days"))
#    except ValueError:
#        print("Sorry that location wasn't recognized")
#        continue
#    else:
#        break
airport_codes = "STO-TYO"
start_time = time.time()
current_outbound_date = input_date_to_datetime(input_outbound_date)
current_return_date = current_outbound_date + timedelta(days=duration)

kayak_link = "https://www.kayak.com/flights/" + airport_codes + "/" + datetime_to_string(current_outbound_date) + "/" + datetime_to_string(current_return_date)
print("https://www.kayak.com/flights/" + airport_codes + "/" + datetime_to_string(current_outbound_date) + "/" + datetime_to_string(current_return_date))
driver.get(kayak_link)

days_to_scrape = 90
for idx in range(days_to_scrape):
	if idx %7 == 0:
	#There is a popup every 7 times the page loads. This closes it
		print("--- %s seconds ---" % (time.time()-start_time))
		close_popup(driver)
	current_outbound_date = current_outbound_date + timedelta(days=1)
	print(current_outbound_date)
	scrape_page(driver,conn, current_outbound_date)
	increment_date(driver, airport_codes, current_outbound_date, duration)
	sleep(randint(2,4))
driver.quit()
print("--- %s seconds ---" % (time.time()-start_time))

#captcha = https://www.kayak.com/security/check?out=%2Fflights%2FSTO-TYO%2F2020-10-31%2F2020-11-07
#          https://www.kayak.com/security/check?out=%2Fflights%2FSTO-TYO%2F2020-11-01%2F2020-11-08
#//div[@class= "recaptcha-checkbox-border"]
