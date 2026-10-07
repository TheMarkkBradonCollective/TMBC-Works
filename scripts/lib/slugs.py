import re

SLUG_OVERRIDES = {
    "5 STAR SMOG (Star Station)": "5-star-smog",
    "Fix Car's - Automotive Diagnostic & Repair Shop": "fix-cars-auto-repair",
    "J & T Auto Repair": "j-t-auto-repair",
    "K.S Complete Shoe Repair": "ks-complete-shoe-repair",
    "I love my shoe shine": "i-love-my-shoe-shine",
    "Chita's Taquería": "chitas-taqueria",
    "Larson Industrial Services, Inc.": "larson-industrial-services",
    "59th Street Barbershop": "59th-street-barbershop",
    "16th Street Donuts": "16th-street-donuts",
    "Nor Cali Fences And Concrete": "nor-cali-fences-and-concrete",
    "Aluminum and Stainless Weldmasters": "weldmasters",
    "Sacramento Radiator Sales and Service": "sacramento-radiator",
    "Trophy Center & Port Engraving": "trophy-center-port-engraving",
    "Prime Service Co. Appliance Repair": "prime-service-appliance-repair",
    "E Z Tires": "e-z-tires",
    "Pass and Go Smog": "pass-and-go-smog",
    "Aarin's Barbershop": "aarins-barbershop",
    "Aarin\u2019s Barbershop": "aarins-barbershop",
    "Jack's Donuts Wheel": "jacks-donuts-wheel",
    "CK's Donuts": "cks-donuts",
    "Marie's Donuts": "maries-donuts",
    "Mike's Mower Shop": "mikes-mower-shop",
    "Schroeder's Shoe Repair": "schroeders-shoe-repair",
    "Norm's Barber Shop": "norms-barber-shop",
    "Antonio's Barber Shop": "antonios-barber-shop",
    "Jay's Mobile Welding & Fabricating": "jays-mobile-welding",
    "Moore's Martial Arts of Sacramento": "moores-martial-arts",
    "John's Towing": "johns-towing",
    "Pino's Auto Repair": "pinos-auto-repair",
    "El Novillero Restaurant": "el-novillero",
    "Eagle Claw Kung Fu of Sacramento": "eagle-claw-kung-fu-of-sacramento",
}


def slugify(name: str) -> str:
    if name in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[name]
    s = name.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s[:60].strip("-")
