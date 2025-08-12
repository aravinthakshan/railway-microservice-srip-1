# Rainfall PDF Parser Microservice

A FastAPI-based microservice for parsing rainfall PDF reports and extracting structured data.

## 🚀 Quick Deploy to Render

### 1. **Push to GitHub**
```bash
git add .
git commit -m "Add rainfall PDF parser microservice"
git push origin main
```

### 2. **Deploy on Render**
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the `pdf-parser-microservice` folder
5. Configure:
   - **Name**: `rainfall-pdf-parser`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
6. Click **"Create Web Service"**

### 3. **Get Your Service URL**
Render will provide a URL like: `https://your-service.onrender.com`

## 📁 Project Structure

```
pdf-parser-microservice/
├── main.py              # FastAPI application
├── parser.py            # PDF parsing logic (copied from python-scripts)
├── requirements.txt     # Python dependencies
├── render.yaml          # Render configuration
├── README.md           # This file
└── test_local.py       # Test script for local testing
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
curl -X POST "https://your-service.onrender.com/process-pdf" \
  -F "pdf_file=@rainfall_report.pdf" \
  -F "date=15/01/2024"
```

### **2. Process Base64 PDF**
```bash
curl -X POST "https://your-service.onrender.com/process-pdf-base64" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_data": "base64_encoded_pdf_content",
    "date": "15/01/2024"
  }'
```

## 🔗 Integration with Vercel

Update your Vercel app to call this Render service:

```typescript
// In your Vercel actions.ts
async function callRenderService(pdfFile: File, date: string) {
  const formData = new FormData()
  formData.append('pdf_file', pdfFile)
  formData.append('date', date)
  
  const response = await fetch('https://your-service.onrender.com/process-pdf', {
    method: 'POST',
    body: formData
  })
  
  return response.json()
}
```

## 🌍 Environment Variables

Render will automatically set:
- `PORT` - Service port (Render sets this)
- `RENDER_EXTERNAL_URL` - Your service URL

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
1. Check Render logs in the dashboard
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
- Go to your Render dashboard
- Click on your service
- Go to "Logs" tab

### **Service Status**
- Check the "Events" tab in Render dashboard
- Monitor uptime and performance

### **Service URL**
- Found in your service overview
- Usually `https://service-name.onrender.com`

## 🔄 Updates

To update your service:
1. Make changes to your code
2. Commit and push to GitHub
3. Render will automatically redeploy

## 💰 Costs

- **Render Free Plan**: $0/month (with limitations)
- **Render Starter Plan**: $7/month (more resources)
- **Render Standard Plan**: $25/month (production ready)

## 🎯 Next Steps

1. **Deploy to Render** using the steps above
2. **Test the endpoints** with a sample PDF
3. **Update your Vercel app** to call this service
4. **Monitor performance** and adjust as needed

## 🆘 Support

If you encounter issues:
1. Check Render logs in the dashboard
2. Verify service health: `GET /health`
3. Test parser: `GET /test-parser`
4. Check Render service status

## 🆚 Render vs Railway

| Feature | Render | Railway |
|---------|--------|---------|
| **Free Tier** | ✅ Yes | ❌ No ($5/month min) |
| **Python Support** | ✅ Excellent | ✅ Good |
| **Deployment** | GitHub integration | CLI + GitHub |
| **HTTPS** | ✅ Automatic | ✅ Automatic |
| **Custom Domains** | ✅ Yes | ✅ Yes |
| **Cost** | $0/month (free) | $5/month minimum | 