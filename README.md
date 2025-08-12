# Rainfall PDF Parser Microservice

A FastAPI-based microservice for parsing rainfall PDF reports and extracting structured data.

## 🚀 Quick Deploy to Railway

### 1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

### 2. **Login to Railway**
```bash
railway login
```

### 3. **Initialize Project**
```bash
cd railway-microservice
railway init
```

### 4. **Deploy to Railway**
```bash
railway up
```

### 5. **Get Your Service URL**
```bash
railway status
```

## 📁 Project Structure

```
railway-microservice/
├── main.py              # FastAPI application
├── parser.py            # PDF parsing logic (copied from python-scripts)
├── requirements.txt     # Python dependencies
├── railway.json         # Railway configuration
├── Procfile            # Railway startup command
└── README.md           # This file
```

## 🔧 API Endpoints

### **Health Check**
- `GET /` - Basic health check
- `GET /health` - Detailed health check
- `GET /test-parser` - Test parser functionality

### **PDF Processing**
- `POST /process-pdf` - Upload PDF file directly
- `POST /process-pdf-base64` - Send base64 encoded PDF

## 📊 Usage Examples

### **1. Process PDF File**
```bash
curl -X POST "https://your-service.railway.app/process-pdf" \
  -F "pdf_file=@rainfall_report.pdf" \
  -F "date=15/01/2024"
```

### **2. Process Base64 PDF**
```bash
curl -X POST "https://your-service.railway.app/process-pdf-base64" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_data": "base64_encoded_pdf_content",
    "date": "15/01/2024"
  }'
```

## 🔗 Integration with Vercel

Update your Vercel app to call this Railway service:

```typescript
// In your Vercel actions.ts
async function callRailwayService(pdfFile: File, date: string) {
  const formData = new FormData()
  formData.append('pdf_file', pdfFile)
  formData.append('date', date)
  
  const response = await fetch('https://your-service.railway.app/process-pdf', {
    method: 'POST',
    body: formData
  })
  
  return response.json()
}
```

## 🌍 Environment Variables

Railway will automatically set:
- `PORT` - Service port (Railway sets this)
- `RAILWAY_STATIC_URL` - Your service URL

## 📝 Dependencies

The service requires these Python packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pandas` - Data processing
- `pdfplumber` - PDF text extraction
- `pymongo` - MongoDB client
- `numpy` - Numerical computing

## 🚨 Troubleshooting

### **Service Won't Start**
1. Check `railway logs` for errors
2. Verify all dependencies are in `requirements.txt`
3. Ensure `parser.py` is in the same directory

### **Parser Import Error**
1. Make sure `parser.py` is copied correctly
2. Check file permissions
3. Verify Python version (3.7+)

### **PDF Processing Fails**
1. Check PDF file format
2. Verify file size (< 10MB)
3. Check date format (DD/MM/YYYY)

## 📈 Monitoring

### **View Logs**
```bash
railway logs
```

### **Service Status**
```bash
railway status
```

### **Service URL**
```bash
railway domain
```

## 🔄 Updates

To update your service:
1. Make changes to your code
2. Commit and push to GitHub
3. Run `railway up` to redeploy

## 💰 Costs

- **Railway Hobby Plan**: $5/month
- **Railway Pro Plan**: $20/month (includes more resources)

## 🎯 Next Steps

1. **Deploy to Railway** using the commands above
2. **Test the endpoints** with a sample PDF
3. **Update your Vercel app** to call this service
4. **Monitor performance** and adjust as needed

## 🆘 Support

If you encounter issues:
1. Check Railway logs: `railway logs`
2. Verify service health: `GET /health`
3. Test parser: `GET /test-parser`
4. Check Railway status: `railway status` 