import spacy
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os
from backend.nlp.entities import entity_extraction
from backend.geo.geocoder import geocode_location
load_dotenv()

GEOPOLITICAL_VERBS = {"intercept", "ground", "divert", "resume", "seize", "ban", "restrict", "close", "jamming", "gps", "gnss", "spoofing"}
GEOPOLITICAL_NOUNS = {"airspace", "sanction", "notam", "corridor", "border", "conflict", "missile"}
HIGH_PRIORITY_REGIONS = {"ukraine", "gaza", "iran", "taiwan", "hormuz"}
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

engine = create_async_engine(os.getenv("DATABASE_URL"))
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def process_data(db_session: AsyncSession):
    found_locations = []
    from backend.db.queries import load_db
    events = await load_db(db_session)
    combined_text = "".join([e.description for e in events if e.description])
    if not combined_text:
        print("No text found to process")
        return

    

    loop = asyncio.get_running_loop()

    for event in events:
        if not event.description:
            continue

        text_to_analyze = event.description
        doc = await loop.run_in_executor(None, nlp, text_to_analyze)
        #print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        #print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
        found_verbs = [token.lemma_ for token in doc if token.pos_ == "VERB" and token.lemma_ in GEOPOLITICAL_VERBS]
        found_nouns = [token.text.lower() for token in doc if token.text.lower() in GEOPOLITICAL_NOUNS]
        signal_locations = [token.text.lower() for token in doc if token.text.lower() in HIGH_PRIORITY_REGIONS]

        if found_verbs or found_nouns or signal_locations:
            found_locations.extend(signal_locations)
            print(f"\n✅ High Signal: {event.title[:50]}...")
            print(f"   Signals: {set(found_verbs)} | {set(found_nouns)} | {set(signal_locations)}")
            locations = await entity_extraction(doc)
              # This now gets ['Taiwan', 'Iran'] instead of None
            if locations:
                    found_locations.extend(locations)
                
            
            # Logic: Only extract entities for high-signal articles
            
        else:
            print(f"❌ Low Signal: {event.title[:50]}... Skipping.")

        event.processed = False
        
    try:
        await db_session.commit()
        print(f"\n✅ Processed {len(events)} events")
    except Exception as e:
        await db_session.rollback()
        print(f"❌ Failed to commit updates: {e}")
        raise e
    if found_locations:
        return found_locations
    else:
        print("No locations found in any articles.")
        return []
async def main():
    async with AsyncSessionLocal() as session:
        found_locations = await process_data(session)
        await geocode_location(found_locations)

if __name__ == "__main__":
     asyncio.run(main())
