#!/usr/bin/env python3
"""Build data/lead_enrichment.json — verified copy + bespoke visual assignments."""
import csv
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "lead_enrichment.json")

PALETTE_COUNT = 12
LAYOUTS = ["split", "editorial", "cardhero"]
FONT_PAIRS = [
    ("Oswald", "Roboto"),
    ("Playfair Display", "Lato"),
    ("Bebas Neue", "Source Sans 3"),
    ("Cormorant Garamond", "Nunito Sans"),
    ("Archivo Black", "Work Sans"),
    ("Libre Baskerville", "Inter"),
    ("Abril Fatface", "Poppins"),
    ("Merriweather", "Open Sans"),
    ("Raleway", "Montserrat"),
    ("PT Serif", "DM Sans"),
    ("Space Grotesk", "IBM Plex Sans"),
    ("Fraunces", "Karla"),
    ("Anton", "Rubik"),
    ("Yeseva One", "Josefin Sans"),
    ("Bitter", "Mulish"),
    ("Roboto Slab", "Roboto"),
    ("Unbounded", "Manrope"),
    ("Lora", "Source Sans 3"),
    ("Spectral", "Noto Sans"),
    ("Syne", "Outfit"),
]

IMAGES = {
    "barber": ("https://images.unsplash.com/photo-1585747860715-2b67a7a7f336?w=1600&q=80", "Unsplash — barber shop interior"),
    "nails": ("https://images.unsplash.com/photo-1604654890710-f6390f18ddb0?w=1600&q=80", "Unsplash — nail salon"),
    "donut": ("https://images.unsplash.com/photo-1551024601-bec78ae704b3?w=1600&q=80", "Unsplash — donuts"),
    "bakery": ("https://images.unsplash.com/photo-1509440159596-0249088772ff?w=1600&q=80", "Unsplash — bakery"),
    "mex": ("https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=1600&q=80", "Unsplash — Mexican food"),
    "tire": ("https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=1600&q=80", "Unsplash — auto service"),
    "fabric": ("https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1600&q=80", "Unsplash — textiles"),
    "smog": ("https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=1600&q=80", "Unsplash — road / driving"),
    "auto": ("https://images.unsplash.com/photo-1487754180451-c456f581a583?w=1600&q=80", "Unsplash — auto repair"),
    "shoe": ("https://images.unsplash.com/photo-1549298916-b41d501d3772?w=1600&q=80", "Unsplash — footwear"),
    "mower": ("https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=1600&q=80", "Unsplash — small engines"),
    "appliance": ("https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1600&q=80", "Unsplash — appliances"),
    "rad": ("https://images.unsplash.com/photo-1625047509248-ec889cbff107?w=1600&q=80", "Unsplash — radiator / engine"),
    "weld": ("https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=1600&q=80", "Unsplash — welding"),
    "martial": ("https://images.unsplash.com/photo-1555597673-b21d5c935865?w=1600&q=80", "Unsplash — martial arts"),
    "trophy": ("https://images.unsplash.com/photo-1517649763962-0c62306601b7?w=1600&q=80", "Unsplash — trophies"),
    "tv": ("https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=1600&q=80", "Unsplash — television"),
    "euro": ("https://images.unsplash.com/photo-1619642751034-765df279d565?w=1600&q=80", "Unsplash — European car"),
    "plumb": ("https://images.unsplash.com/photo-1585704032915-ebc035e00588?w=1600&q=80", "Unsplash — plumbing"),
    "pet": ("https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=1600&q=80", "Unsplash — dog grooming"),
    "industrial": ("https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=1600&q=80", "Unsplash — industrial"),
    "rug": ("https://images.unsplash.com/photo-1600166896085-959adc3512d1?w=1600&q=80", "Unsplash — rugs"),
    "thai": ("https://images.unsplash.com/photo-1559314809-0d155014e29e?w=1600&q=80", "Unsplash — Thai food"),
    "tow": ("https://images.unsplash.com/photo-1544622351-20a7f5172b20?w=1600&q=80", "Unsplash — towing"),
    "fence": ("https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=1600&q=80", "Unsplash — construction"),
    "alter": ("https://images.unsplash.com/photo-1558171813-4c088753af8f?w=1600&q=80", "Unsplash — tailoring"),
}

CAT_IMAGE = {
    "Barbershop": "barber",
    "Nail salon": "nails",
    "Donut shop": "donut",
    "Bakery": "bakery",
    "Mexican restaurant": "mex",
    "Tire shop": "tire",
    "Auto/marine/furniture upholstery": "fabric",
    "Furniture upholstery": "fabric",
    "Smog check": "smog",
    "Smog check (STAR)": "smog",
    "Auto repair": "auto",
    "Auto repair / diagnostics": "auto",
    "Auto repair & smog": "auto",
    "Shoe repair": "shoe",
    "Shoe & leather repair": "shoe",
    "Shoe shine": "shoe",
    "Alterations / tailor": "alter",
    "Lawn mower / small engine repair": "mower",
    "Appliance repair": "appliance",
    "Radiator repair": "rad",
    "Welding / fabrication": "weld",
    "Martial arts (kung fu)": "martial",
    "Martial arts": "martial",
    "Trophies / engraving": "trophy",
    "TV repair (in-home)": "tv",
    "European auto repair": "euro",
    "Import auto repair": "auto",
    "Mobile welding": "weld",
    "Plumbing": "plumb",
    "Upholstery & embroidery": "fabric",
    "Dog grooming": "pet",
    "Industrial contractor / millwright": "industrial",
    "Rug cleaning": "rug",
    "Thai restaurant": "thai",
    "Towing": "tow",
    "Fence & concrete contractor": "fence",
}

# Verified copy overrides per slug (no invented reviews/prices/names)
FACTS = {
    "knock-out-barber-shop": {
        "headline": "Sharp cuts on Del Paso Boulevard",
        "subhead": "Neighborhood barbershop at 2829 Del Paso Blvd — booking also listed on Fresha and Booksy.",
        "paragraphs": [
            "Knock Out Barber Shop serves Sacramento with classic barber services from a Del Paso Boulevard location.",
            "Public listings note online booking through Fresha and Booksy for customers who prefer to schedule ahead.",
        ],
        "highlights": ["Del Paso Blvd location", "Walk-ins when available", "Online booking via Fresha/Booksy"],
        "services": ["Men's haircuts", "Beard trims", "Line-ups", "Kids' cuts"],
    },
    "el-novillero": {
        "headline": "Family-run Mexican dining since 1970",
        "subhead": "Fresh sauces and corn chips made daily — a Franklin Boulevard landmark at 18th Avenue.",
        "paragraphs": [
            "El Novillero Restaurant has been run by the Davalos family since 1970, growing from a 28-seat dining room to seating for about 180 guests.",
            "The restaurant states that sauces and corn chips are made fresh daily using quality ingredients. Gift cards are accepted only as El Novillero gift cards.",
            "The dining room does not take reservations, and private rooms are no longer available per the restaurant's public information.",
        ],
        "highlights": ["Since 1970", "127-space lighted parking lot", "Cards: Visa, MC, Amex, Discover"],
        "hours": ["Monday: Closed", "Tuesday–Sunday: 11:30 AM – 7:00 PM"],
        "hours_note": "<p>Holiday closures are posted on the restaurant's current site — call ahead on holiday weekends.</p>",
        "menu_categories": [
            {"title": "House standards (public menu categories)", "items": ["Combination plates", "Burritos", "Enchiladas", "Tostadas", "Daily specials"]},
            {"title": "Dining notes", "items": ["No reservations", "Face masks optional in waiting area until seated"]},
        ],
        "menu_heading": "From the kitchen",
        "aside_html": "<p><strong>Payments:</strong> Visa, Mastercard, American Express, Discover. El Novillero gift cards only.</p><p><strong>Parking:</strong> On-site lot with exterior lighting and cameras — valuables should not be left in vehicles.</p>",
        "layout": "editorial",
        "image_key": "mex",
    },
    "capitol-city-european": {
        "headline": "European automotive service with a warranty you can count on",
        "subhead": "4150 Power Inn Rd, Unit 2 — diagnostics, maintenance, and repairs for European makes.",
        "paragraphs": [
            "Capitol City European positions itself as a customer-first European car service center with computer diagnostics, factory recommended maintenance, electrical work, HVAC, brakes, and suspension repairs.",
            "Repairs are backed by a 2-year or 24,000-mile warranty stated on the shop's public website.",
        ],
        "highlights": ["2-year / 24,000-mile warranty", "European specialization", "Appointment-friendly"],
        "hours": ["Monday–Friday: 8:00 AM – 5:00 PM", "Saturday–Sunday: Closed"],
        "services": ["Computer diagnostics", "Factory scheduled maintenance", "Electrical repairs", "A/C service", "Brake & suspension work", "Complex drivability repairs"],
        "aside_html": "<p>Online appointments: the shop asks for about 48 hours notice when scheduling by email.</p>",
        "layout": "split",
        "image_key": "euro",
    },
    "sk-auto-repair": {
        "headline": "Auto repair & smog in Natomas",
        "subhead": "4381 Gateway Park Blvd — quality work with care, Mon–Fri 8:30 AM – 5:30 PM.",
        "paragraphs": [
            "SK Auto Repair & Smog serves Sacramento from Gateway Park Boulevard with maintenance, diagnostics, and smog inspections.",
            "The shop advertises a limited smog special of $10 off for 2000 and newer vehicles (per its public website).",
        ],
        "highlights": ["Smog & repair under one roof", "Quality guarantee stated online", "Natomas Gateway Park location"],
        "hours": ["Monday–Friday: 8:30 AM – 5:30 PM"],
        "services": ["Engine diagnostics", "Lube, oil & filter service", "Belts & hoses", "Air conditioning", "Brake repair", "Smog inspections"],
        "layout": "cardhero",
        "image_key": "auto",
    },
    "changs-thai-cuisine": {
        "headline": "Consistent Thai plates — Halal chicken & beef",
        "subhead": "3620 N Freeway Blvd #310 — lunch and dinner service through the week.",
        "paragraphs": [
            "Chang's Thai Cuisine invites guests to try genuine dishes with an emphasis on consistent quality every visit.",
            "The restaurant states Halal certification for chicken and beef dishes on its public website.",
        ],
        "hours": [
            "Tuesday–Friday: 11:00 AM – 3:30 PM & 4:30 PM – 9:00 PM",
            "Saturday–Sunday: 12:00 PM – 9:00 PM",
        ],
        "hours_note": "<p>Monday hours not listed on the current site — call to confirm.</p>",
        "menu_heading": "Menu focus",
        "menu_categories": [{"title": "Thai favorites (general)", "items": ["Curries", "Noodles", "Stir-fry plates", "Rice dishes"]}],
        "layout": "editorial",
        "image_key": "thai",
    },
    "trophy-center-port-engraving": {
        "headline": "Awards, engraving & trophies for 65+ years",
        "subhead": "3609 Bradshaw Rd Suite G — laser, rotary, and diamond-drag engraving on site.",
        "paragraphs": [
            "Trophy Center & Port Engraving describes more than 65 years of local service with a large in-stock showroom.",
            "Engraving is performed on site with laser, rotary, and diamond-drag capabilities for fast, accurate turnaround.",
        ],
        "highlights": ["Bradshaw Road showroom", "On-site engraving", "Express service at no extra cost (per site)"],
        "services": ["Custom trophies & awards", "Laser engraving", "Rotary engraving", "Diamond-drag engraving", "Corporate & team awards"],
        "aside_html": "<p><strong>Also listed:</strong> Fax 916-739-0549 · Mobile/after-hours 916-710-1908</p>",
        "layout": "split",
        "image_key": "trophy",
    },
    "chitas-taqueria": {
        "headline": "Midtown taquería since 2006",
        "subhead": "2019 Q Street — Mexican grill favorites in Sacramento.",
        "paragraphs": [
            "Chita's Taquería has served Sacramento since 2006 from its Q Street address.",
            "The business has built a large local following — a modern site helps guests find hours, directions, and contact info quickly.",
        ],
        "highlights": ["Since 2006", "Q Street / Midtown", "Dine-in & takeout"],
        "services": ["Tacos & burritos", "Mexican grill plates", "Lunch & dinner", "Takeout"],
        "layout": "cardhero",
        "image_key": "mex",
    },
    "broadway-donuts": {
        "headline": "Broadway Boulevard donuts — back under longtime baker leadership",
        "subhead": "2731 Broadway — reopened December 2025 with a baker who knows the neighborhood.",
        "paragraphs": [
            "Broadway Donuts reopened in December 2025 under new ownership that includes a longtime baker, according to local press coverage noted in TMBC lead research.",
            "A dedicated website makes it easy for regulars to find hours, directions, and how to reach the shop.",
        ],
        "highlights": ["Broadway in Sacramento", "Reopened Dec 2025", "Neighborhood donut counter"],
        "services": ["Fresh donuts daily", "Coffee & morning staples", "Counter service"],
        "layout": "cardhero",
        "image_key": "donut",
    },
    "maries-donuts": {
        "headline": "Freeport Boulevard donut institution",
        "subhead": "2950 Freeport Blvd — known for late-night and early-morning hours (confirm today's times by phone).",
        "paragraphs": [
            "Marie's Donuts is a long-running Sacramento counter on Freeport Boulevard with a strong local reputation.",
            "Lead research notes late-night hours and Facebook as a primary web presence today; delivery platforms list morning pickup windows — call for the current schedule.",
        ],
        "highlights": ["Freeport Blvd landmark", "Late-night reputation", "Counter service"],
        "hours_note": "<p>Hours vary by day and have been reported differently across platforms — please call before you drive.</p>",
        "services": ["Raised & cake donuts", "Fritters & classics", "Coffee", "Grab-and-go counter"],
        "layout": "editorial",
        "image_key": "donut",
    },
    "smog-xperts": {
        "headline": "Veteran-owned smog checks",
        "subhead": "121 Otto Cir — STAR-quality testing with a straightforward visit.",
        "paragraphs": [
            "Smog Xperts is described in public listings as a veteran-owned smog check station serving Sacramento.",
            "A clear website helps drivers find hours, pricing policies, and directions before their DMV deadline.",
        ],
        "highlights": ["Veteran-owned (per listings)", "Otto Circle location", "Smog inspections"],
        "services": ["Smog inspections", "DMV-required tests", "Quick turnaround focus"],
        "layout": "split",
        "image_key": "smog",
    },
    "par-tv-services": {
        "headline": "In-home TV repair across Sacramento",
        "subhead": "Mobile service based in Davis — serving Sacramento-area homes.",
        "paragraphs": [
            "Par TV Services offers in-home television repair with a mobile service model.",
            "The shop's public contact page lists 1802 Alicante St, Davis, CA as its base while serving the greater Sacramento region.",
        ],
        "highlights": ["Mobile in-home service", "Sacramento-area coverage", "TV repair focus"],
        "services": ["Television repair", "In-home service calls", "Remote & connectivity troubleshooting"],
        "layout": "split",
        "image_key": "tv",
    },
    "pinos-auto-repair": {
        "headline": "Madison Avenue auto repair since 1990",
        "subhead": "3805 Madison Ave, North Highlands — over three decades serving neighbors.",
        "paragraphs": [
            "Pino's Auto Repair states on its public site that it has served the community since 1990.",
            "A refreshed, mobile-friendly site helps customers call, find hours, and understand services before they visit.",
        ],
        "services": ["General auto repair", "Diagnostics", "Maintenance", "North Highlands shop"],
        "layout": "cardhero",
        "image_key": "auto",
    },
    "aarins-barbershop": {
        "headline": "Stockton Boulevard barber studio",
        "subhead": "7837 Stockton Blvd Ste 600 — appointments via Booksy listed publicly.",
        "paragraphs": ["Aarin's Barbershop serves south Sacramento from Stockton Boulevard.", "Public listings highlight Booksy for scheduling ahead."],
        "highlights": ["Ste 600 location", "Booksy booking", "Barber services"],
        "services": ["Haircuts", "Beard work", "Kids' cuts", "Line-ups"],
        "layout": "split",
    },
    "norms-barber-shop": {
        "headline": "Fourth Avenue neighborhood barber",
        "subhead": "2890 4th Ave — classic Sacramento barbershop energy.",
        "paragraphs": ["Norm's Barber Shop keeps a traditional barber presence near Land Park.", "A simple site helps neighbors find hours and phone before they walk in."],
        "services": ["Men's cuts", "Beard trims", "Walk-in friendly"],
        "layout": "editorial",
    },
    "antonios-barber-shop": {
        "headline": "Folsom Boulevard barbershop",
        "subhead": "5134 Folsom Blvd — classic neighborhood cuts.",
        "paragraphs": ["Antonio's Barber Shop is described in lead research as a classic neighborhood barbershop on Folsom Boulevard.", "Clear directions and click-to-call matter for walk-in barber traffic."],
        "services": ["Haircuts", "Beard shaping", "Walk-ins"],
        "layout": "cardhero",
    },
    "royal-nails": {
        "headline": "Greenback Lane nail care",
        "subhead": "7333 Greenback Ln, Citrus Heights — salon services with Fresha booking listed online.",
        "paragraphs": ["Royal Nails offers nail services from Citrus Heights on Greenback Lane.", "Listings note Fresha for online booking."],
        "services": ["Manicures", "Pedicures", "Nail shaping", "Polish services"],
        "layout": "editorial",
        "image_key": "nails",
    },
    "jacks-donuts-wheel": {
        "headline": "Northgate donut wheel",
        "subhead": "2261 Northgate Blvd — morning stop for fresh rings and coffee.",
        "paragraphs": ["Jack's Donuts Wheel serves Sacramento from Northgate Boulevard.", "A bright, mobile-friendly page helps commuters find the shop quickly."],
        "services": ["Donuts", "Coffee", "Counter service"],
        "layout": "cardhero",
    },
    "cks-donuts": {
        "headline": "Folsom Boulevard donuts",
        "subhead": "8333 Folsom Blvd — neighborhood donut counter.",
        "paragraphs": ["CK's Donuts operates on Folsom Boulevard in Sacramento.", "Showcase hours, phone, and directions for regular customers."],
        "layout": "split",
    },
    "16th-street-donuts": {
        "headline": "Downtown-adjacent donut stop",
        "subhead": "1601 F Street — quick counter service near downtown.",
        "paragraphs": ["16th Street Donuts serves customers from F Street with grab-and-go donuts.", "Make phone and map easy on mobile."],
        "layout": "editorial",
    },
    "le-croissant-factory": {
        "headline": "Riverside Boulevard bakery",
        "subhead": "6413 Riverside Blvd — pastries and baked goods.",
        "paragraphs": ["Le Croissant Factory offers baked goods from Riverside Boulevard.", "Highlight counter hours and directions for pickup orders."],
        "services": ["Croissants & pastries", "Baked goods", "Counter orders"],
        "layout": "split",
        "image_key": "bakery",
    },
    "taqueria-sanchez": {
        "headline": "Norwood Avenue taquería",
        "subhead": "2885 Norwood Ave — Mexican plates to stay or go.",
        "paragraphs": ["Taqueria Sanchez serves Mexican food on Norwood Avenue.", "Delivery apps list the restaurant — a owned website keeps contact info consistent."],
        "services": ["Tacos", "Burritos", "Combination plates", "Takeout"],
        "layout": "cardhero",
    },
    "e-z-tires": {
        "headline": "Winters Street tire shop",
        "subhead": "4011 Winters St — tires and service for local drivers.",
        "paragraphs": ["E Z Tires serves a high-traffic Winters Street location.", "Drivers need fast access to phone, directions, and services."],
        "services": ["Tire sales", "Installation", "Balancing", "Flat repair"],
        "layout": "split",
        "image_key": "tire",
    },
    "golden-state-upholstery": {
        "headline": "Auto, marine & furniture upholstery",
        "subhead": "5401 Warehouse Way — custom upholstery work.",
        "paragraphs": ["Golden State Upholstery handles auto, marine, and furniture upholstery from Warehouse Way.", "Facebook has been the primary web presence — a dedicated site explains services clearly."],
        "services": ["Auto upholstery", "Marine upholstery", "Furniture reupholstery"],
        "layout": "editorial",
    },
    "upholstery-unlimited": {
        "headline": "Fourteenth Avenue upholstery",
        "subhead": "7930 14th Ave — furniture upholstery & repair.",
        "paragraphs": ["Upholstery Unlimited serves Sacramento with furniture upholstery services.", "Project-based work needs clear contact paths and service lists."],
        "services": ["Reupholstery", "Cushion rebuilds", "Fabric replacement"],
        "layout": "split",
    },
    "pass-and-go-smog": {
        "headline": "Marysville Boulevard smog checks",
        "subhead": "3927 Marysville Blvd — quick DMV testing.",
        "paragraphs": ["Pass and Go Smog offers smog inspections on Marysville Boulevard.", "Confirm contact email in person if reaching out digitally — listings vary."],
        "services": ["Smog inspections", "DMV-required tests"],
        "layout": "cardhero",
        "image_key": "smog",
    },
    "5-star-smog": {
        "headline": "STAR smog station on Fruitridge",
        "subhead": "2790 Fruitridge Rd — STAR-certified testing.",
        "paragraphs": ["5 STAR SMOG (Star Station) provides STAR smog tests on Fruitridge Road.", "Listings also mention an alternate phone (530) 821-9363 — confirm which to use."],
        "services": ["STAR smog tests", "DMV inspections"],
        "aside_html": "<p>Alternate number (530) 821-9363 appears on some listings.</p>",
        "layout": "split",
    },
    "j-t-auto-repair": {
        "headline": "Watt Avenue auto repair",
        "subhead": "6315 Watt Ave #124, North Highlands.",
        "paragraphs": ["J & T Auto Repair serves North Highlands from Watt Avenue.", "Local repair shops win with trust-focused design and easy calls."],
        "services": ["Auto repair", "Diagnostics", "Maintenance"],
        "layout": "cardhero",
    },
    "fix-cars-auto-repair": {
        "headline": "Diagnostics & repair on Fruitridge",
        "subhead": "8500 Fruitridge Rd Unit 11 — automotive diagnostics specialty.",
        "paragraphs": ["Fix Car's focuses on automotive diagnostics and repair from Fruitridge Road.", "Complex repairs require clear service descriptions and contact info."],
        "services": ["Computer diagnostics", "Engine repair", "Maintenance"],
        "layout": "editorial",
    },
    "schroeders-shoe-repair": {
        "headline": "Tenth Street shoe repair",
        "subhead": "2022 10th St — long-running repair bench.",
        "paragraphs": ["Schroeder's Shoe Repair maintains a Tenth Street shop with decades of neighborhood use.", "Cobbler services need simple hours, phone, and map visibility."],
        "services": ["Heel & sole repair", "Stitching", "Leather patching"],
        "layout": "split",
    },
    "ks-complete-shoe-repair": {
        "headline": "J Street shoe & leather repair",
        "subhead": "912 J St — downtown near Cesar Chavez Park.",
        "paragraphs": ["K.S Complete Shoe Repair sits on J Street across from Cesar Chavez Park.", "Downtown foot traffic relies on clear directions and phone contact."],
        "services": ["Shoe repair", "Leather goods", "Quick turnaround"],
        "layout": "editorial",
    },
    "linda-lee-alterations": {
        "headline": "Freeport Boulevard alterations",
        "subhead": "3000 Freeport Blvd #2 — tailoring & hem work.",
        "paragraphs": ["Linda Lee Alterations provides tailoring services on Freeport Boulevard.", "Appointment-based work benefits from easy call and email contact."],
        "services": ["Hemming", "Resizing", "Repairs", "Formal wear adjustments"],
        "layout": "split",
        "image_key": "alter",
    },
    "mikes-mower-shop": {
        "headline": "Silica Avenue mower repair",
        "subhead": "1815 Silica Ave Ste A — lawn equipment specialists.",
        "paragraphs": ["Mike's Mower Shop repairs lawn mowers and small engines from Silica Avenue.", "Seasonal rushes require obvious phone and hours information."],
        "services": ["Lawn mower repair", "Blade sharpening", "Small engine tune-ups"],
        "layout": "cardhero",
    },
    "all-green-power-equipment": {
        "headline": "La Castana Way power equipment",
        "subhead": "5885 La Castana Way — outdoor power repair.",
        "paragraphs": ["All Green Power Equipment services outdoor power equipment in Sacramento.", "Help customers find the shop on mobile maps quickly."],
        "services": ["Mower repair", "Small engine service", "Seasonal maintenance"],
        "layout": "split",
    },
    "prime-service-appliance-repair": {
        "headline": "Norwood appliance repair",
        "subhead": "4408 Norwood Ave #8 — in-home appliance service.",
        "paragraphs": ["Prime Service Co. Appliance Repair is an active California LLC offering appliance repair.", "Home visits need prominent scheduling phone and service area clarity."],
        "services": ["In-home appliance repair", "Washer & dryer", "Refrigerators", "Ovens & ranges"],
        "layout": "editorial",
        "image_key": "appliance",
    },
    "sacramento-radiator": {
        "headline": "Franklin Boulevard radiator specialists",
        "subhead": "6430 Franklin Blvd #4 — cooling system sales & service.",
        "paragraphs": ["Sacramento Radiator Sales and Service works on radiators and cooling systems.", "Replacing an unfinished Wix template with clear services builds trust."],
        "services": ["Radiator repair", "Cooling system service", "Parts sales"],
        "layout": "cardhero",
        "image_key": "rad",
    },
    "weldmasters": {
        "headline": "Aluminum & stainless fabrication",
        "subhead": "1621 Juliesse Ave Suite B — welding masters on Juliesse.",
        "paragraphs": ["Aluminum and Stainless Weldmasters provides welding and fabrication.", "Industrial clients still expect HTTPS, mobile contact, and clear capability lists."],
        "services": ["Aluminum welding", "Stainless fabrication", "Custom metal work"],
        "layout": "editorial",
    },
    "eagle-claw-kung-fu-of-sacramento": {
        "headline": "Eagle Claw kung fu on 24th Street",
        "subhead": "2791 24th St — traditional martial arts training.",
        "paragraphs": ["Eagle Claw Kung Fu of Sacramento teaches kung fu from 24th Street.", "Lead research noted the old domain no longer represents the school — a new site restores trustworthy info."],
        "services": ["Kung fu classes", "Traditional training", "All ages"],
        "layout": "split",
    },
    "i-love-my-shoe-shine": {
        "headline": "L Street shoe shine stand",
        "subhead": "824 L St — professional shoe shine in downtown Sacramento.",
        "paragraphs": ["I love my shoe shine offers shoe shine services on L Street.", "A polished preview matches the craft — phone and map first."],
        "services": ["Shoe shines", "Leather conditioning", "Walk-in service"],
        "layout": "cardhero",
    },
    "star-motors": {
        "headline": "Florin Road import repair",
        "subhead": "2680 Florin Rd #103a — import automotive service.",
        "paragraphs": ["Star Motors services import vehicles from Florin Road.", "An updated site replaces outdated WordPress with fast, secure static pages."],
        "services": ["Import auto repair", "Maintenance", "Diagnostics"],
        "layout": "split",
    },
    "jays-mobile-welding": {
        "headline": "Mobile welding & fabrication",
        "subhead": "8581 Younger Creek Dr Ste 200 — on-site welding.",
        "paragraphs": ["Jay's Mobile Welding & Fabricating brings welding services to job sites.", "Previous hosting showed 'Site Not Found' — this concept restores credibility."],
        "services": ["Mobile welding", "Fabrication", "On-site repair"],
        "layout": "editorial",
    },
    "sac-city-plumbing": {
        "headline": "Sacramento plumbing that answers the phone",
        "subhead": "3031 E St — residential plumbing service.",
        "paragraphs": ["Sac City Plumbing provides plumbing services from E Street.", "When the old homepage 404s, customers can't book — a clear CTA fixes that."],
        "services": ["Leak repair", "Installations", "Drain service", "Residential plumbing"],
        "layout": "cardhero",
        "image_key": "plumb",
    },
    "friends-of-bailee": {
        "headline": "Freeport Boulevard dog grooming",
        "subhead": "6622 Freeport Blvd #4 — grooming with care.",
        "paragraphs": ["Friends Of Bailee grooms dogs from Freeport Boulevard.", "Replace an untouched 2013 Wix page with fresh layout and booking phone."],
        "services": ["Baths", "Haircuts", "Nail trims", "Breed-friendly grooms"],
        "layout": "editorial",
        "image_key": "pet",
    },
    "larson-industrial-services": {
        "headline": "Industrial contracting & millwright work",
        "subhead": "6000 Midway St Ste 400 — B2B industrial services.",
        "paragraphs": ["Larson Industrial Services, Inc. provides industrial contracting and millwright services.", "B2B buyers still need mobile-readable capabilities and contact info."],
        "services": ["Industrial installation", "Millwright services", "Plant maintenance support"],
        "layout": "split",
        "image_key": "industrial",
    },
    "moores-martial-arts": {
        "headline": "Broadway martial arts family",
        "subhead": "5708 Broadway — programs for kids and adults.",
        "paragraphs": ["Moore's Martial Arts of Sacramento trains students on Broadway.", "Remove template placeholder copy with real class and contact information."],
        "services": ["Kids martial arts", "Adult programs", "Self-discipline & fitness"],
        "layout": "cardhero",
    },
    "59th-street-barbershop": {
        "headline": "59th Street cuts",
        "subhead": "2917 59th St — neighborhood barbershop.",
        "paragraphs": ["59th Street Barbershop serves Oak Park / Tahoe Park area from 59th Street.", "Lead research noted the prior website was down — this preview shows what's possible."],
        "services": ["Haircuts", "Beard trims", "Walk-ins"],
        "layout": "split",
    },
    "sacramento-rug-works": {
        "headline": "65th Street rug cleaning",
        "subhead": "1308 65th St — professional rug care.",
        "paragraphs": ["Sacramento Rug Works cleans area rugs from 65th Street.", "Upgrade from 2016-era XHTML to responsive layout and map embeds."],
        "services": ["Area rug cleaning", "Drop-off service", "Fiber-safe cleaning methods"],
        "layout": "editorial",
        "image_key": "rug",
    },
    "smog-express": {
        "headline": "16th Street STAR smog station",
        "subhead": "2401 16th St — smog testing near midtown.",
        "paragraphs": ["Smog Express offers STAR smog tests on 16th Street.", "Listings mention alternate phone (916) 498-8477 for BAR references — confirm before visiting."],
        "services": ["STAR smog checks", "DMV-required inspections"],
        "aside_html": "<p>Alternate listing phone: (916) 498-8477</p>",
        "layout": "cardhero",
    },
    "johns-towing": {
        "headline": "Elder Creek towing",
        "subhead": "8540 Elder Creek Rd Ste D — Sacramento towing service.",
        "paragraphs": ["John's Towing operates from Elder Creek Road in Sacramento.", "Map listings previously pointed at an unrelated Atlanta site — an owned URL fixes customer confusion."],
        "services": ["Emergency towing", "Roadside assistance", "Local Sacramento coverage"],
        "layout": "split",
        "image_key": "tow",
    },
    "nor-cali-fences-and-concrete": {
        "headline": "Fences & concrete in Sacramento",
        "subhead": "2186 Ferran Ave — residential fence and flatwork.",
        "paragraphs": ["Nor Cali Fences And Concrete builds fences and concrete projects from Ferran Avenue.", "Lead research noted an aging 2016 Wix site — this concept adds clear estimate CTAs."],
        "services": ["Fence installation", "Concrete flatwork", "Residential projects"],
        "layout": "editorial",
        "image_key": "fence",
    },
    "xpert-upholstery-works": {
        "headline": "Upholstery & embroidery studio",
        "subhead": "7941 Amador Ave Suite 3 — commercial and residential upholstery services.",
        "paragraphs": [
            "Xpert Upholstery Works offers upholstery and embroidery services from its Amador Avenue suite.",
            "Public listings show both a Sacramento-area phone and an email at info@xpertupholsteryworks.net — confirm the best number before your project.",
        ],
        "services": ["Custom upholstery", "Embroidery services", "Commercial & residential work"],
        "aside_html": "<p>Listing phone may differ from the number on the business .net site — confirm before visiting.</p>",
        "layout": "editorial",
        "image_key": "fabric",
    },
}


def fonts_query(head, body):
    return (
        f"family={head.replace(' ', '+')}:wght@400;600;700&"
        f"family={body.replace(' ', '+')}:wght@400;500;600"
    )


def default_facts(name, category, notes):
    return {
        "headline": name,
        "subhead": f"{category} serving the greater Sacramento area.",
        "paragraphs": [
            notes.split(". ")[0] + "." if notes else f"{name} welcomes local customers with reliable {category.lower()} service.",
            "This preview concept focuses on mobile-friendly contact, directions, and clear service information.",
        ],
        "highlights": ["Sacramento-area business", "Call for availability", "Directions & map below"],
        "services": [],
    }


def main():
    from lib.slugs import slugify

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out = {}
    with open(os.path.join(ROOT, "leads.csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for idx, row in enumerate(rows):
        slug = slugify(row["business_name"])
        h = int(hashlib.sha256(slug.encode()).hexdigest(), 16)
        fhead, fbody = FONT_PAIRS[idx % len(FONT_PAIRS)]
        fact = FACTS.get(slug, default_facts(row["business_name"], row["category"], row.get("notes", "")))
        layout = fact.get("layout", LAYOUTS[(idx + h) % len(LAYOUTS)])
        img_key = fact.get("image_key", CAT_IMAGE.get(row["category"], "auto"))
        hero_url, hero_credit = IMAGES[img_key]
        palette_idx = (idx * 3 + h) % PALETTE_COUNT
        cat_css = {
            "Barbershop": ".hero h1 { text-transform: uppercase; letter-spacing: .06em; max-width: none; }",
            "Donut shop": ".hero { min-height: 68vh; } .hl { background: color-mix(in srgb, var(--accent) 18%, transparent); }",
            "Mexican restaurant": ".hero h1 { max-width: none; font-style: normal; }",
            "Auto repair": ".services-block { border-top: 4px solid var(--accent); }",
            "Smog check": ".hero-inner { border-left: 4px solid var(--accent2); padding-left: 1.25rem; }",
            "Smog check (STAR)": ".hero-inner { border-left: 4px solid var(--accent2); padding-left: 1.25rem; }",
        }.get(row["category"], "")
        entry = {
            "layout": layout,
            "font_head": fhead,
            "font_body": fbody,
            "fonts_query": fonts_query(fhead, fbody),
            "palette_idx": palette_idx,
            "hero_image": hero_url,
            "hero_credit": hero_credit,
            "favicon_initial": row["business_name"][0],
            "headline": fact.get("headline", row["business_name"]),
            "subhead": fact.get("subhead", ""),
            "meta_description": fact.get("subhead", row["category"])[:155],
            "paragraphs": fact.get("paragraphs", []),
            "highlights": fact.get("highlights", []),
            "services": fact.get("services") or [],
            "hours": fact.get("hours", []),
            "hours_note": fact.get("hours_note", ""),
            "menu_categories": fact.get("menu_categories", []),
            "menu_heading": fact.get("menu_heading", ""),
            "menu_note": fact.get("menu_note", ""),
            "services_heading": fact.get("services_heading", "Services"),
            "aside_html": fact.get("aside_html", ""),
            "sections": fact.get(
                "sections",
                ["story", "services", "menu", "hours", "location", "contact"],
            ),
            "nav": fact.get(
                "nav",
                '<a href="#about">About</a><a href="#services">Services</a><a href="#visit">Visit</a><a href="#contact">Contact</a>',
            ),
            "layout_css": (fact.get("layout_css") or "") + cat_css,
        }
        if not entry["services"]:
            entry["services"] = [
                f"{row['category']} for local customers",
                "Transparent contact & directions",
                "Call ahead for availability",
            ]
        out[slug] = entry
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("Wrote", len(out), "profiles to", OUT)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
