def format_patient_details(patient_file):
    """
    Formats patient details from a PatientFile SQLAlchemy model instance.
    """
    # Get answer by category
    def get_anamnesis(category):
        for anam in patient_file.anamneses:
            if anam.category.lower() == category.lower():
                return anam.answer
        return "Keine Angaben"

    return f"""
    Name: {patient_file.first_name} {patient_file.last_name}
    Geburtsdatum: {patient_file.birth_date.strftime('%d.%m.%Y') if patient_file.birth_date else 'Unbekannt'}
    Ethnie: {patient_file.ethnic_origin or 'Unbekannt'}
    Größe: {patient_file.height or 'Unbekannt'} cm
    Gewicht: {patient_file.weight or 'Unbekannt'} kg
    Geschlecht (medizinisch): {patient_file.gender_medical or 'Unbekannt'}

    --- 
    Krankheitsverlauf:
    {get_anamnesis("Krankheitsverlauf")}

    --- 
    Vorerkrankungen:
    {get_anamnesis("Vorerkrankungen")}

    --- 
    Dauermedikation:
    {get_anamnesis("Medikamente")}

    --- 
    Allergien:
    {get_anamnesis("Allergien")}

    --- 
    Familienanamnese:
    {get_anamnesis("Familienanamnesis")}

    --- 
    Kardiovaskuläre Risikofaktoren:
    {get_anamnesis("Kardiovaskuläre Risikofaktoren")}

    --- 
    Sozial-/Berufsanamnese:
    {get_anamnesis("Sozial-/Berufsanamnesis")}
    """