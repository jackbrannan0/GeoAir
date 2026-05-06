async def entity_extraction(doc):
    for entity in doc.ents:
                extracted_locations = []
                # Focusing on locations for your map
                if entity.label_ in ["GPE", "LOC", "FAC"]:
                    print(f"   📍 Location: {entity.text} ({entity.label_})")
                    extracted_locations.append(entity.text)
                return extracted_locations