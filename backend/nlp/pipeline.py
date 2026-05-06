import spacy
import asyncio
from backend.db.models import MapAlerts
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
IGNORE_LOCATIONS = {"us", "united states", "europe", "africa"}
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

engine = create_async_engine(os.getenv("DATABASE_URL"))
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def process_data(db_session: AsyncSession):
    from backend.db.queries import load_db
    events = await load_db(db_session)
    
    if not events:
        print("No text found to process")
        return []

    loop = asyncio.get_running_loop()

    for event in events:
        print(f"\nProcessing Event ID {event.id}: {event.title[:50]}...")
        if not event.description:
            continue

        # 1. NLP Analysis
        text_to_analyze = event.description
        doc = await loop.run_in_executor(None, nlp, text_to_analyze)
        
        found_verbs = [token.lemma_ for token in doc if token.pos_ == "VERB" and token.lemma_ in GEOPOLITICAL_VERBS]
        found_nouns = [token.text.lower() for token in doc if token.text.lower() in GEOPOLITICAL_NOUNS]
        signal_locations = [token.text.lower() for token in doc if token.text.lower() in HIGH_PRIORITY_REGIONS]

        # 2. Signal Check
        if found_verbs or found_nouns or signal_locations:
            print(f"\n✅ High Signal: {event.title[:50]}...")
            
            # 3. Entity Extraction
            extracted = await entity_extraction(doc)
            all_hits = list(set(signal_locations + (extracted or [])))
            
            # 4. Geocode (The logic previously in main)
            if all_hits:
                print(f"DEBUG: Found hits for {event.id}: {all_hits}")
                geo_results = await geocode_location(all_hits)
                
                # Add this to see what you're actually working with
                print(f"DEBUG: Geocoder returned {len(geo_results)} results: {geo_results}")
                
                for res in geo_results:
                    lat, lon, addr = None, None, "Unknown"

                    # Handle Dictionary (the original expectation)
                    if isinstance(res, dict):
                        lat = res.get("lat")
                        lon = res.get("lon")
                        addr = res.get("address", "Unknown")
                    
                    # Handle Tuple (what your logs show you are actually getting)
                    elif isinstance(res, (tuple, list)) and len(res) >= 2:
                        lat = res[0]
                        lon = res[1]
                        # If your tuple has a 3rd element for address, use res[2]
                        addr = res[2] if len(res) > 2 else "Unknown"

                    # Final Check: Do we have the coordinates now?
                    if lat and lon:
                        new_alert = MapAlerts(
                            raw_event_id=event.id,
                            location_name=addr,
                            latitude=float(lat), # Ensure they are floats for the DB
                            longitude=float(lon),
                            signals={"source": "nlp_pipeline"}
                        )
                        db_session.add(new_alert)
                        print(f"   📍 Alert Staged: {addr} ({lat}, {lon})")
                    else:
                        print(f"   ⚠️ Result skipped: Could not parse coordinates from {res}")
        # 6. Mark as processed
        event.processed = True

    # Final logic: Commit everything at once
    try:
        await db_session.commit()
        print(f"\n✅ Pipeline Complete: Processed {len(events)} events.")
    except Exception as e:
        await db_session.rollback()
        print(f"❌ Failed to commit: {e}")
        raise e