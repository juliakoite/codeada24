from med_llama import askme  # bc we are using med_lamma ??

def get_medical_explanation(procedure):
    """Get AI explanation for a medical procedure"""
    question = f"Can you explain this medical charge on my medical bill? Here is the item: {procedure}"
    return askme(question)
