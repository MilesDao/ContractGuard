from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas.response import ApiResponse
from backend.core.privacy import ephemeral_bytes

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/octet-stream"
}

def create_app() -> FastAPI:
    app = FastAPI(
        title="ContractGuard API",
        version="1.0.0",
        description="AI-Powered Vietnamese Contract Risk Analyzer"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    async def health_check():
        return ApiResponse(success=True, data={"status": "ok", "service": "ContractGuard API"})

    @app.post("/api/analyze")
    async def analyze_contract(file: UploadFile = File(...)):
        if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed.")

        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10 MB limit.")

        with ephemeral_bytes(content):
            # In production, parses bytes -> calls PhoBERT model -> returns JSON
            # For quick verification, return standard response envelope
            result = {
                "contractTitle": file.filename or "Hợp đồng đã tải lên",
                "contractType": "LABOR",
                "overallScore": 75,
                "statusGrade": "RUI_RO_CAO",
                "summary": {
                    "totalClauses": 5,
                    "riskyClauses": 3,
                    "criticalCount": 2,
                    "highCount": 1,
                    "mediumCount": 0
                },
                "clauses": []
            }

        return ApiResponse(success=True, data=result)

    return app

app = create_app()
