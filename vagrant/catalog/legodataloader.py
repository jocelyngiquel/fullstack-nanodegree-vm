
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Catalog, Base, Item, User

engine = create_engine('sqlite:///legocatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(Uname="John Doe", email="Johndoe@somewhere.com",
             picture='https://lc-imageresizer-live-s.legocdn.com/resize?width=744&imageUrl=https%3a%2f%2fwww.lego.com%2fr%2fwww%2fr%2fportals%2f-%2fmedia%2fthemes%2fworlds%2ffrontpage%2fcta%2fcta-minifig-05.png%3fl.r%3d-1845865519')
session.add(User1)
session.commit()

#Catalog entry for Lego City
catalog1 = Catalog(user_id=1, Cname="City", catalog_image="https://sh-s7-live-s.legocdn.com/is/image/LEGOMKTG/city%2D%2D201606%2D%2Dgl%2D%2Dlogo?$CatListLogo$")

session.add(catalog1)
session.commit()

#Catalog entry for Lego Star Wars
catalog2 = Catalog(user_id=1, Cname="Star Wars", catalog_image="https://sh-s7-live-s.legocdn.com/is/image/LEGOMKTG/star-wars-black--201606--gl--logo?$CatListLogo$")

session.add(catalog2)
session.commit()

#Catalog entry for Lego Technic
catalog3 = Catalog(user_id=1, Cname="Technic", catalog_image="https://sh-s7-live-s.legocdn.com/is/image/LEGOMKTG/technic%2D%2D201606%2D%2Dgl%2D%2Dlogo?$CatListLogo$")

session.add(catalog3)
session.commit()

#Items for Lego City
item1 = Item(user_id=1, Iname="Police Station", description="Be part of the action with the LEGO City police as they try to keep the crooks in jail, featuring a three-level Police Station loaded with accessory elements, a jail cell with exploding wall function, watchtower, garage and offices, helicopter, police pursuit car and police motorbike, plus the crooks truck with rotating, extendable cherry picker. Includes seven minifigures plus a police dog figure.",
                    pieces=894, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/60141_alt1?$main$",
                    catalog_id=1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, Iname="City Hospital", description="Grab your stethoscope and head to the 60204 LEGO City Hospital, where heroes are needed every day! This amazing set features a hospital building with reception area, kiosk and ambulance drop-off, vision testing room with eye chart, x-ray room with a light brick function, plus an operating/delivery room. It's also modular, so you can configure it in different ways. This cool set also includes an ambulance with opening back door and space for a stretcher, a helicopter with spinning rotors and storage box, and a separate buildable helipad. Includes 11 LEGO minifigures, plus skeleton and baby figures.",
                    pieces=861, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/60204_alt1?$main$",
                    catalog_id=1)

session.add(item2)
session.commit()

#Items for Lego Star Wars
item3 = Item(user_id=1, Iname="Millenium Falcon", description="Welcome to the largest, most detailed LEGO Star Wars Millennium Falcon model we've ever created in fact, with 7,500 pieces it's one of our biggest LEGO models, period! This amazing LEGO interpretation of Han Solo's unforgettable Corellian freighter has all the details that Star Wars fans of any age could wish for.",
                    pieces=7541, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/75192_alt1?$main$",
                    catalog_id=2)

session.add(item3)
session.commit()

item4 = Item(user_id=1, Iname="Snowspeeder", description="Collect a true Star Wars classic: the T-47 Snowspeeder. This LEGO interpretation of the iconic airspeeder that fans will remember from Star Wars: Episode V The Empire Strikes Back has all the details you'd expect.",
                    pieces=1703, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/75144_alt1?$main$",
                    catalog_id=2)

session.add(item4)
session.commit()

item5 = Item(user_id=1, Iname="Imperial TIE Fighter", description="Engage the enemy with the LEGO Star Wars Imperial TIE Fighter! This brick-built version of the Empire's iconic attack craft has a highly detailed design.",
                    pieces=519, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/75211_alt1?$main$",
                    catalog_id=2)

session.add(item5)
session.commit()

#Items for Lego Technic
item6 = Item(user_id=1, Iname="BMW R 1200 GS Adventure", description="Explore the high-tech innovation of the BMW R 1200 GS Adventure with this authentic LEGO Technic replica, featuring a blue and black color scheme, black spoke wheels with all-terrain tires, windshield and a detailed dashboard and exhaust.",
                    pieces=603, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/42063_alt1?$main$",
                    catalog_id=3)

session.add(item6)
session.commit()

item7 = Item(user_id=1, Iname="First Responder", description="Enjoy a rewarding build and play experience with this awesome replica of a fire department SUV, featuring a red and black color scheme with sticker detailing, wide black rims with chunky tires, blue warning beacons, and roof-mounted spot lamps.",
                    pieces=513, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/42075_alt1?$main$",
                    catalog_id=3)

session.add(item7)
session.commit()

item8 = Item(user_id=1, Iname="Airport Rescue Vehicle", description="Head for the runway with this authentic 2-in-1 LEGO Technic Airport Rescue Vehicle, featuring a red, black and gray color scheme, working boom mechanism, 4-cylinder engine with moving pistons, large driver's cab with detailed dashboard, wing mirrors, equipment storage compartment, twin-axle steering, double rear axle and chunky tires.",
                    pieces=1098, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/42068_alt1?$main$",
                    catalog_id=3)

session.add(item8)
session.commit()

item9 = Item(user_id=1, Iname="Ocean Explorer", description="Enjoy seafaring adventures with this LEGO Technic Ocean Explorer set, featuring a ship with a dark-blue, red and white color scheme, plus a buildable submarine with movable arms and spinning propeller, and a buildable helicopter with spinning rotors.",
                    pieces=1327, created_at=datetime.now(), item_image="https://sh-s7-live-s.legocdn.com/is/image//LEGO/42064_alt1?$main$",
                    catalog_id=3)

session.add(item9)
session.commit()

print "added menu items!"
