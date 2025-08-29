from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import re

app = FastAPI()

# -------------------------
# Request & Response Models
# -------------------------
class InputData(BaseModel):
    data: List[str]

# Replace with your actual details
FULL_NAME = "john_doe"           # <-- CHANGE THIS to your full name in lowercase
BIRTH_DATE = "17091999"          # <-- CHANGE THIS to your DOB in ddmmyyyy format
EMAIL = "john@xyz.com"           # <-- CHANGE THIS
ROLL_NUMBER = "ABCD123"          # <-- CHANGE THIS

USER_ID = f"{FULL_NAME}_{BIRTH_DATE}"

@app.post("/bfhl")
def process_data(input_data: InputData) -> Dict[str, Any]:
    try:
        data = input_data.data
        even_numbers = []
        odd_numbers = []
        alphabets = []
        special_characters = []
        numbers_sum = 0

        # For concatenating alphabets in reverse order
        alpha_only = ""

        for item in data:
            if isinstance(item, str):
                # Check if it's a number (digits only)
                if item.isdigit():
                    num = int(item)
                    numbers_sum += num
                    if num % 2 == 0:
                        even_numbers.append(item)  # Keep as string
                    else:
                        odd_numbers.append(item)
                # Check if it's an alphabet string (only letters)
                elif item.isalpha():
                    # Only single characters are expected, but handle multi-char
                    cleaned = ''.join(ch for ch in item if ch.isalpha())
                    upper_cleaned = cleaned.upper()
                    alphabets.append(upper_cleaned)
                    alpha_only += cleaned  # collect original for reverse concat
                else:
                    # Contains non-alphanumeric (special characters)
                    # Extract special characters
                    for ch in item:
                        if not ch.isalnum():
                            special_characters.append(ch)
                        elif ch.isalpha():
                            # It's a letter, treat separately
                            alphabets.append(ch.upper())
                            alpha_only += ch
                        elif ch.isdigit():
                            num = int(ch)
                            numbers_sum += num
                            if num % 2 == 0:
                                even_numbers.append(ch)
                            else:
                                odd_numbers.append(ch)
            else:
                # If not string, skip or convert? We expect strings per spec.
                continue

        # Remove duplicates from special characters while preserving order
        seen = set()
        special_filtered = []
        for x in special_characters:
            if x not in seen:
                seen.add(x)
                special_filtered.append(x)

        # Concatenate all alphabetical characters in reverse order with alternating caps
        reversed_alpha = alpha_only[::-1]  # Reverse the string
        concat_string = ""
        for idx, char in enumerate(reversed_alpha):
            if idx % 2 == 0:
                concat_string += char.upper()
            else:
                concat_string += char.lower()

        # Prepare response
        return {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": list(set(alphabets)),  # Deduplicate uppercase alphabets
            "special_characters": special_filtered,
            "sum": str(numbers_sum),  # Return sum as string
            "concat_string": concat_string
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid input or processing error")

# Health check route (optional)
@app.get("/")
def home():
    return {"message": "BFHL API is running. Use POST /bfhl"}

# Run with: uvicorn main:app --reload