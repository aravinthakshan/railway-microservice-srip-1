from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64
import tempfile
import os
import logging
from typing import Optional
import uvicorn
from pydantic import BaseModel

# Import our parser
from parser import FixedRainfallParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Rainfall PDF Parser API",
    description="Microservice for parsing rainfall PDF reports and uploading to MongoDB",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PDFProcessRequest(BaseModel):
    pdf_data: str  # base64 encoded PDF
    date: str

class PDFProcessResponse(BaseModel):
    success: bool
    records_count: int
    message: str
    processing_time_ms: int

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Rainfall PDF Parser API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Test if parser can be imported
        parser = FixedRainfallParser(debug=False)
        return {
            "status": "healthy",
            "parser": "available",
            "timestamp": "2024-01-15T12:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")

@app.post("/process-pdf", response_model=PDFProcessResponse)
async def process_pdf(
    pdf_file: UploadFile = File(...),
    date: str = Form(...)
):
    """
    Process a rainfall PDF file and return extracted data
    
    Args:
        pdf_file: PDF file to process
        date: Date in DD/MM/YYYY format
    
    Returns:
        JSON response with processing results
    """
    import time
    start_time = time.time()
    
    try:
        # Validate file type
        if not pdf_file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if pdf_file.size > max_size:
            raise HTTPException(status_code=400, detail="File size must be less than 10MB")
        
        logger.info(f"Processing PDF: {pdf_file.filename}, Size: {pdf_file.size} bytes, Date: {date}")
        
        # Read PDF file
        pdf_content = await pdf_file.read()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(pdf_content)
            temp_path = temp_file.name
        
        try:
            # Process PDF using our parser
            parser = FixedRainfallParser(debug=False)
            df = parser.process_pdf_to_dataframe(temp_path)
            
            if df.empty:
                raise HTTPException(status_code=400, detail="No data could be extracted from the PDF")
            
            # Add date column
            df['date'] = date
            
            # Convert to records
            records = df.to_dict('records')
            records_count = len(records)
            
            # Upload to MongoDB
            try:
                from pymongo import MongoClient
                import os
                
                MONGO_URI = os.environ.get('MONGODB_URI')
                if not MONGO_URI:
                    raise HTTPException(status_code=500, detail="MONGODB_URI environment variable not set")
                
                client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
                # Test connection
                client.admin.command('ping')
                
                db = client['rainfall-data']
                collection = db['rainfalldatas']
                
                # Insert records into MongoDB
                if records:
                    result = collection.insert_many(records)
                    logger.info(f"Successfully uploaded {len(result.inserted_ids)} records to MongoDB")
                else:
                    logger.warning("No records to upload to MongoDB")
                
                client.close()
                
            except Exception as e:
                logger.error(f"MongoDB upload failed: {e}")
                raise HTTPException(status_code=500, detail=f"MongoDB upload failed: {str(e)}")
            
            processing_time = int((time.time() - start_time) * 1000)
            
            logger.info(f"Successfully processed PDF: {records_count} records in {processing_time}ms")
            
            return PDFProcessResponse(
                success=True,
                records_count=records_count,
                message=f"PDF processed successfully. {records_count} records extracted and uploaded to MongoDB.",
                processing_time_ms=processing_time
            )
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@app.post("/process-pdf-base64", response_model=PDFProcessResponse)
async def process_pdf_base64(request: PDFProcessRequest):
    """
    Process a base64 encoded PDF and return extracted data
    
    Args:
        request: PDFProcessRequest with base64 PDF data and date
    
    Returns:
        JSON response with processing results
    """
    import time
    start_time = time.time()
    
    try:
        logger.info(f"Processing base64 PDF, Date: {request.date}")
        
        # Decode base64 PDF data
        try:
            pdf_data = base64.b64decode(request.pdf_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 data: {str(e)}")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(pdf_data)
            temp_path = temp_file.name
        
        try:
            # Process PDF using our parser
            parser = FixedRainfallParser(debug=False)
            df = parser.process_pdf_to_dataframe(temp_path)
            
            if df.empty:
                raise HTTPException(status_code=400, detail="No data could be extracted from the PDF")
            
            # Add date column
            df['date'] = request.date
            
            # Convert to records
            records = df.to_dict('records')
            records_count = len(records)
            
            # Upload to MongoDB
            try:
                from pymongo import MongoClient
                import os
                
                MONGO_URI = os.environ.get('MONGODB_URI')
                if not MONGO_URI:
                    raise HTTPException(status_code=500, detail="MONGODB_URI environment variable not set")
                
                client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
                # Test connection
                client.admin.command('ping')
                
                db = client['rainfall-data']
                collection = db['rainfalldatas']
                
                # Insert records into MongoDB
                if records:
                    result = collection.insert_many(records)
                    logger.info(f"Successfully uploaded {len(result.inserted_ids)} records to MongoDB")
                else:
                    logger.warning("No records to upload to MongoDB")
                
                client.close()
                
            except Exception as e:
                logger.error(f"MongoDB upload failed: {e}")
                raise HTTPException(status_code=500, detail=f"MongoDB upload failed: {str(e)}")
            
            processing_time = int((time.time() - start_time) * 1000)
            
            logger.info(f"Successfully processed base64 PDF: {records_count} records in {processing_time}ms")
            
            return PDFProcessResponse(
                success=True,
                records_count=records_count,
                message=f"PDF processed successfully. {records_count} records extracted and uploaded to MongoDB.",
                processing_time_ms=processing_time
            )
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing base64 PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@app.get("/test-parser")
async def test_parser():
    """Test endpoint to verify parser functionality"""
    try:
        parser = FixedRainfallParser(debug=False)
        return {
            "status": "success",
            "message": "Parser is working correctly",
            "parser_class": str(type(parser))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parser test failed: {str(e)}")

if __name__ == "__main__":
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Set to False for production
    ) 