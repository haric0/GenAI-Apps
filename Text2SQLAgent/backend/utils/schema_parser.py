import re
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def parse_schema_file(schema_text: str) -> list:
    """
    Parses the schema into complete tables.
    Each table schema (from CREATE TABLE to closing ");") is returned as a single entry.
    """
    logger.info("Starting schema parsing...")

    lines = schema_text.splitlines()
    cleaned = [line.strip() for line in lines if line.strip()]
    
    # Check if there's any valid schema content
    if not cleaned:
        logger.warning("Schema text is empty after cleanup.")
    
    # This regex captures everything between CREATE TABLE and the closing );
    # It handles foreign keys and nested column definitions
    pattern = re.compile(
        r"CREATE\s+TABLE\s+`?(\w+)`?\s?\((.*?)\);",  # Match the CREATE TABLE ... with column definitions
        re.IGNORECASE | re.DOTALL
    )
    
    # Find all matches for table schemas
    matches = pattern.findall(schema_text)

    if not matches:
        logger.warning("No table schemas found in the provided schema text.")
    
    table_schemas = []
    
    # For each match, reformat into a logical table schema
    for table_name, schema in matches:
        logger.info(f"Parsing schema for table: {table_name}")

        # Clean up and normalize schema content
        schema = schema.replace("\n", " ").strip()
        schema = re.sub(r'\s{2,}', ' ', schema)  # Remove extra spaces between column definitions
        
        table_schemas.append(f"CREATE TABLE {table_name} ({schema});")
        logger.debug(f"Processed schema for {table_name}: {table_schemas[-1]}")
    
    logger.info(f"Parsed {len(table_schemas)} tables successfully.")
    
    return table_schemas
