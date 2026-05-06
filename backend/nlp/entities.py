async def entity_extraction(doc):
    for entity in doc.ents:
                # Focusing on locations for your map
                if entity.label_ in ["GPE", "LOC", "FAC"]:
                    print(f"   📍 Location: {entity.text} ({entity.label_})")