PATIENT_INNEN = {
    "DEFAULT_DEMENTE_PATIENTIN": {
        "name": "Anna Zank",
        "alter": "89 Jahre",
        "geburtsdatum": "01.09.1935",
        "ethnie": "kaukasisch",
        "bmi": "20,5",

        "krankheitsverlauf": """
        Heute morgen auf die rechte Seite gestürzt, mit dem RTW in die Klinik geliefert
        """,

        "vorerkrankungen": [
            "Art. Hypertonie",
            "ausgeprägte senile Alzheimer Demenz",
            "chronische Niereninsuffizienz G3A2",
            "Varikosis bds.",
            "Z.n. offene Appendektomie (im Alter von 21 Jahren)"
        ],

        "dauermedikation": {
            "Ramipril": "5mg p.o. 1-0-1",
            "Amlodipin": "5mg p.o. 1-0-1",
            "Donepezil": "10mg p.o. 0-0-1",
            "Vitamin D": "10.000 IE 1x /Woche"
        },

        "allergien": "keine",

        "familienanamnese": {
            "vater": "verstorben an Prostata-CA",
            "mutter": "Diabetes Typ II ab 55 Jahren"
        },

        "kardiovaskuläre_risikofaktoren": [
            "Art. Hypertonie",
            "kein Alkohol- oder Nikotinabusus"
        ],

        "sozial_berufsanamnese": {
            "beruf": "pensioniert, war Lehrerin",
            "familienstand": "verheiratet",
            "kinder": "2 Töchter"
        }
    },

    "PSEUDOTUMOR_CEREBRI": {
        "name": "Maria Meier",
        "alter": "42 Jahre",
        "geburtsdatum": "01.09.1983",
        "ethnie": "kaukasisch",
        "bmi": "20,5",

        "krankheitsverlauf": """
        holozephaler Kopfschmerz, von dumpfen, drückendem Charakter mit retrobulbärem Fokus, fortbestehend seit einer rezenten Covid-19 Infektion vor zwei Wochen. Lageabhängigkeit der Schmerzen verneint. Die Patientin gibt keine häufigen Kopfschmerzen in der Vorgeschichte an. Aktuell bestehe keine akute Beeinträchtigung der Sehkraft. Subjektiv besteht kein Gesichtsfeldausfall.
        """,

        "vorerkrankungen": [
            "Dermatologisch: stressinduzierte Akne/Rosazea conglobata, Botox-Injektion fazial vor 1 Monat",
            "Gynäkologisch: Hysterektomie vor 10 Jahren nach mehreren Fehlgeburten",
            "Pädiatrisch: EBV in Jugend"
        ],

        "dauermedikation": {
            "Isotretinoin": "20mg p.o. 1-0-1-0 seit 40 Tagen wegen Rosazea",
            "Dexamethason dihydrogenphosphat-Dinatrium 1 mg/1 ml Neomycin sulfat 3,5 mg/1 ml ": "5mg p.o. 1-0-1 wegen Konjunktivitid seit 3 Wochen",
        },

        "allergien": "keine",

        "familienanamnese": {
            "Schwester": "Trigeminusneuralgie mit 10 Jahren",
        },

        "kardiovaskuläre_risikofaktoren": [
            "1 Glas Wein/d",
            "kein Nikotinkonsum"
        ],

        "sozial_berufsanamnese": {
            "beruf": "kaufmännische Abteilung als Privatassistenz, überwiegend Büroarbeit",
            "familienstand": "geschieden",
            "kinder": "1 Sohn"
        }
    }
}

# Function to format patient data into a string
def format_patient_details(patient):
    return f"""
    Name: {patient.get("name", "Unbekannt")}
    Alter: {patient.get("alter", "Unbekannt")}
    Geburtsdatum: {patient.get("geburtsdatum", "Unbekannt")}
    Ethnie: {patient.get("ethnie", "Unbekannt")}
    BMI: {patient.get("bmi", "Unbekannt")}

    --- 
    Krankheitsverlauf:
    {patient.get("krankheitsverlauf", "Keine Angaben").strip()}

    --- 
    Vorerkrankungen:
    {'; '.join(patient.get("vorerkrankungen", ["Keine"]))}

    --- 
    Dauermedikation:
    {'; '.join([f"{med}: {dose}" for med, dose in patient.get("dauermedikation", {}).items()])}

    --- 
    Allergien:
    {patient.get("allergien", "Keine")}

    --- 
    Familienanamnese:
    Vater: {patient.get("familienanamnese", {}).get("vater", "Keine Angaben")}; 
    Mutter: {patient.get("familienanamnese", {}).get("mutter", "Keine Angaben")}

    --- 
    Kardiovaskuläre Risikofaktoren:
    {'; '.join(patient.get("kardiovaskuläre_risikofaktoren", ["Keine"]))}

    --- 
    Sozial-/Berufsanamnese:
    Beruf: {patient.get("sozial_berufsanamnese", {}).get("beruf", "Keine Angaben")}; 
    Familienstand: {patient.get("sozial_berufsanamnese", {}).get("familienstand", "Keine Angaben")}; 
    Kinder: {patient.get("sozial_berufsanamnese", {}).get("kinder", "Keine Angaben")}
    """
