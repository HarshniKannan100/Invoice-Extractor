from fastapi import FastAPI, File, UploadFile, HTTPException
from pdf2image import convert_from_path
from imagepreprocessing.denoise import median_blur
from imagepreprocessing.rotate import detect_rotation, rotate_to_upright    
import cv2
import os
import uuid
import json
from llm.gemini_extractor import extract_invoice_from_image
from llm.prompt import PROMPT_TEXT
from pydantic import ValidationError
from infrastructure.db.dbschema import VendorSchema
from infrastructure.db.dbschema import InvoiceHeaderSchema
from infrastructure.db.dbschema import InvoiceItemsSchema
from infrastructure.db.dbschema import InvoiceSummarySchema
from fastapi import Depends
from infrastructure.db.repository import delete_invoice_item, get_all_invoices, save_invoice, get_invoice_by_id
from infrastructure.db.connections import get_db  # your existing DB dependency
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
IMAGE_DIR = "images"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)   

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...),db = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    pdf_name = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(UPLOAD_DIR, pdf_name)

    with open(pdf_path, "wb") as f:
        f.write(await file.read())
    
    images = convert_from_path(pdf_path,dpi=200)
    image_paths = []
    for i, image in enumerate(images):
        image_name = f"{pdf_name}_page_{i+1}.png"
        image_path = os.path.join(IMAGE_DIR, image_name)
        image.save(image_path, "PNG")
        image_paths.append(image_path)


    denoised_image_paths = []
    for image_path in image_paths:
        image = cv2.imread(image_path)
        if image is None:
            continue

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised_image = median_blur(gray_image, kernel_size=5)
        denoised_image_path = image_path.replace(".png", "_denoised.png")
        cv2.imwrite(denoised_image_path, denoised_image)
        denoised_image_paths.append(denoised_image_path)
    angle=0
    rotated_image_paths = []    
    for image_path in denoised_image_paths:
            image = cv2.imread(image_path)
            if image is None:
                continue
            angle = detect_rotation(image)
            if angle in [90, 180, 270]:
                image = rotate_to_upright(image, angle)
                rotated_image_path = image_path.replace("_denoised.png", "_rotated.png")
                cv2.imwrite(rotated_image_path, image)
                rotated_image_paths.append(rotated_image_path)
            else:
                rotated_image_paths.append(image_path)
    final_image_path = rotated_image_paths[0]  # first page for now

    gemini_response = extract_invoice_from_image(
        image_path=final_image_path,
        prompt=PROMPT_TEXT
    )
    parsed_data = json.loads(gemini_response)
    try:
        vendor_data = VendorSchema.model_validate(parsed_data["vendor"])
        invoice_header_data = InvoiceHeaderSchema.model_validate(
            parsed_data["invoice_header"]
        )
        invoice_items_data = [
            InvoiceItemsSchema.model_validate(item)
            for item in parsed_data["invoice_items"]
        ]
        invoice_summary_data = InvoiceSummarySchema.model_validate(
            parsed_data["invoice_summary"]
        )
    except ValidationError as e:
        raise HTTPException(
        status_code=422,
        detail="Gemini returned invalid invoice data"
        )
    
    return {
    "vendor": vendor_data,
    "invoice_header": invoice_header_data,
    "invoice_items": invoice_items_data,
    "invoice_summary": invoice_summary_data
}


@app.get("/invoice/{invoice_id}")
async def fetch_invoice(invoice_id: int, db=Depends(get_db)):
    data = await get_invoice_by_id(db, invoice_id)

    if not data:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return data

@app.get("/invoices")
async def fetch_all_invoices(db=Depends(get_db)):
    data = await get_all_invoices(db)
    return data

@app.delete("/deleteinvoice/{invoice_id}")
async def delete_item(invoice_id: int, db=Depends(get_db)):
    await delete_invoice_item(db, invoice_id)
    return {"message": "Invoice deleted"}

@app.post("/save-invoice")
async def save_invoice_endpoint(
    payload: dict = Body(...),
    db=Depends(get_db)
):
    try:
        vendor_data = VendorSchema.model_validate(payload["vendor"])
        invoice_header_data = InvoiceHeaderSchema.model_validate(payload["invoice_header"])
        invoice_items_data = [
            InvoiceItemsSchema.model_validate(item)
            for item in payload["invoice_items"]
        ]
        invoice_summary_data = InvoiceSummarySchema.model_validate(payload["invoice_summary"])
    except ValidationError:
        raise HTTPException(status_code=422, detail="Invalid invoice data")

    invoice_id = await save_invoice(
        db=db,
        vendor_data=vendor_data,
        invoice_header_data=invoice_header_data,
        invoice_items_data=invoice_items_data,
        invoice_summary_data=invoice_summary_data
    )

    return {
        "message": "Invoice saved successfully",
        "invoice_id": invoice_id
    }

@app.delete("/invoice-item/{item_id}")
async def delete_invoice_item_endpoint(
    item_id: int,
    db=Depends(get_db)
):
    await delete_invoice_item(db, item_id)
    return {"message": "Invoice item deleted"}
