from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io

from google_sheet import get_sheet_data
from google_drive import download_image_from_drive_url
from matcher import images_are_similar

app = FastAPI()

SPREADSHEET_ID = "161yriujUrXgFJDYbryAuOlcV2apTBT8lYOiGMs52240"
RANGE_NAME = "Sheet1!A2:C"  # [Drive URL, Price, Stock]

@app.post("/match_image")
async def match_image(file: UploadFile = File(...)):
    content = await file.read()
    uploaded_image = Image.open(io.BytesIO(content))
    
    sheet_rows = get_sheet_data(SPREADSHEET_ID, RANGE_NAME)
    print(f"Loaded {len(sheet_rows)} rows from sheet")

    for row in sheet_rows:
        try:
            drive_url, price, stock = row
            print(f"Trying image: {drive_url}")
            sheet_img = download_image_from_drive_url(drive_url)
            if sheet_img:
                if images_are_similar(uploaded_image, sheet_img):
                    print("MATCH FOUND!")
                    return {
                        "matched_image_url": drive_url,
                        "price": price,
                        "stock": stock
                    }
                else:
                    print("No match with this image.")
            else:
                print("Could not load image from Drive.")
        except Exception as e:
            print(f"Error during comparison: {e}")
            continue

    return JSONResponse(content={"message": "No match found"}, status_code=404)
