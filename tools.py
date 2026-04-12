from langchain.tools import Tool

def symptom_checker(query: str) -> str:
    q = query.lower()
    if "fever" in q:
        return "Possible causes: viral infection, flu. Monitor temperature and rest."
    elif "cough" in q:
        return "Possible causes: cold, allergy, or respiratory infection."
    elif "headache" in q:
        return "Possible causes: stress, dehydration, or migraine."
    elif "nausea" in q or "vomiting" in q:
        return "Possible causes: food poisoning, viral infection, or motion sickness."
    elif "fatigue" in q or "tired" in q:
        return "Possible causes: anaemia, poor sleep, or viral illness."
    elif "rash" in q:
        return "Possible causes: allergic reaction, eczema, or viral infection."
    elif "pain" in q:
        return "Pain can have many causes. Please describe the location and nature for better guidance."
    return "Symptoms unclear. Please consult a doctor for proper diagnosis."

symptom_tool = Tool(
    name="Symptom Checker",
    func=symptom_checker,
    description=(
        "Use this tool when the user describes personal symptoms they are experiencing, "
        "such as fever, cough, headache, nausea, rash, or fatigue."
    ),
)