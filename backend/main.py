"""
WhatsApp Chat Analyzer Backend API
Handles file upload, parsing, and analytics computation
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import parse_whatsapp_chat
from analytics import compute_analytics

app = FastAPI(title="WhatsApp Chat Analyzer API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "WhatsApp Chat Analyzer API"}


@app.post("/api/analyze")
async def analyze_chat(file: UploadFile = File(...)):
    """
    Upload and analyze WhatsApp chat file
    
    Expected file format: WhatsApp exported .txt file
    Returns analytics data for the last 7 days
    """
    print(f"Received file upload request: {file.filename}, content_type: {file.content_type}")
    
    # Validate file type
    if not file.filename or not file.filename.endswith('.txt'):
        print(f"Invalid file type: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a .txt file exported from WhatsApp."
        )
    
    # Validate file size (max 10MB)
    contents = await file.read()
    file_size = len(contents)
    print(f"File size: {file_size} bytes")
    
    if file_size > 10 * 1024 * 1024:
        print(f"File too large: {file_size} bytes")
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 10MB."
        )
    
    if file_size == 0:
        print("File is empty")
        raise HTTPException(
            status_code=400,
            detail="File is empty. Please upload a valid chat file."
        )
    
    try:
        # Decode file contents
        text_content = contents.decode('utf-8', errors='replace')
        print(f"Decoded file content length: {len(text_content)} characters")
        
        # Parse WhatsApp chat
        messages = parse_whatsapp_chat(text_content)
        print(f"Parsed {len(messages)} messages from file")
        
        if not messages:
            raise HTTPException(
                status_code=400,
                detail="No valid messages found in the chat file. Please check the file format."
            )
        
        # Compute analytics
        analytics = compute_analytics(messages)
        print(f"Computed analytics for {len(messages)} messages")
        
        return {
            "success": True,
            "data": analytics,
            "total_messages": len(messages)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
