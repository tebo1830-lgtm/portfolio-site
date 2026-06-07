# Portfolio Site File Viewer - Deployment Guide

## ✅ What Was Implemented

### 1. **Interactive File Viewer**
- Files are now clickable in the Projects page
- Clicking a file opens a modal with file content preview
- Text files (`.txt`, `.py`, `.sh`, `.sql`, `.js`, `.html`, `.css`, `.json`, `.csv`, `.xml`, `.md`) display content inline
- Binary files show file info with a download button
- **View-only access** - Users cannot edit or delete files

### 2. **Secure API Endpoints**
Two new REST API endpoints were added to `app.py`:

#### `/api/file-content` (POST)
- Serves file content for viewing
- Includes security checks to prevent directory traversal attacks
- Returns formatted JSON with file content

**Request:**
```json
{
  "path": "C:\\path\\to\\file.txt"
}
```

**Response (Text File):**
```json
{
  "success": true,
  "content": "file contents here...",
  "filename": "filename.txt",
  "type": "text",
  "file_ext": ".txt"
}
```

**Response (Binary File):**
```json
{
  "success": true,
  "filename": "document.pdf",
  "type": "binary",
  "file_ext": ".pdf",
  "size": 1024000,
  "mime_type": "application/pdf",
  "message": "This is a binary file. Click the download button to view/save it."
}
```

#### `/api/file-download` (POST)
- Allows downloading files for viewing
- Same security checks as file-content endpoint
- Returns the file for browser download

**Request:**
```json
{
  "path": "C:\\path\\to\\file.pdf"
}
```

### 3. **Professional File Viewer Modal**
- Clean, centered modal interface
- Shows loading spinner while fetching
- Displays file content with syntax highlighting for code
- Includes error handling with user-friendly messages
- Download button for binary files
- Close button to dismiss modal
- Click outside modal to close
- Responsive design works on different screen sizes

### 4. **Enhanced UI**
- Files are now interactive with blue underlined links
- Hover effects on file links
- Collapsible folder structure remains unchanged
- File icons indicate file types (📄 docs, 🐍 Python, 🗄️ SQL, etc.)

---

## 🚀 Deploying to a Website

To make this accessible from anywhere without needing a local computer, you have several options:

### **Option 1: Heroku (Easiest for Beginners)**

1. **Create Heroku Account**
   - Go to https://www.heroku.com
   - Sign up for a free account
   - Install Heroku CLI

2. **Prepare Your Project**
   ```powershell
   # Initialize git in your project
   git init
   git add .
   git commit -m "Initial commit"
   
   # Create Procfile if not exists (check if yours exists)
   # It should contain: web: python app.py
   ```

3. **Deploy to Heroku**
   ```powershell
   # Login to Heroku
   heroku login
   
   # Create Heroku app
   heroku create your-portfolio-name
   
   # Deploy
   git push heroku main
   ```

4. **Result**: Your site will be at `https://your-portfolio-name.herokuapp.com`

**Pros**: Free tier available, automatic HTTPS, easy deployment
**Cons**: App sleeps after 30 mins of inactivity on free tier

### **Option 2: PythonAnywhere**

1. **Sign Up**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload Files**
   - Use the web interface to upload your project

3. **Configure**
   - Set up virtual environment
   - Configure web app settings

4. **Result**: Your site will be at `https://yourusername.pythonanywhere.com`

**Pros**: Python-specific, good free tier, always on
**Cons**: Need to configure web app settings

### **Option 3: AWS/DigitalOcean (Most Control)**

1. **Create Server Instance**
   - AWS EC2, DigitalOcean Droplet, or similar
   - Install Python, pip, virtualenv

2. **Deploy**
   ```bash
   # SSH into your server
   ssh user@your-server-ip
   
   # Clone/upload your project
   git clone your-repo-url
   cd portfolio-site
   
   # Create virtualenv and install
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Use Production Server**
   - Install Gunicorn: `pip install gunicorn`
   - Run: `gunicorn app:app`
   - Use Nginx as reverse proxy
   - Set up SSL with Let's Encrypt

**Pros**: Full control, scalable, good for production
**Cons**: More technical setup, costs money

### **Option 4: Google Cloud / Microsoft Azure**

Similar to AWS but with their own interfaces. Offer free credits for new users.

---

## 🔒 Security Considerations for Remote Access

When deploying to a website, important security measures are already in place:

### ✅ Already Implemented:
- **Path Validation**: The `is_safe_path()` function prevents directory traversal attacks
- **View-Only Access**: Users cannot modify or delete files through the API
- **Allowed Paths**: Only specific directories can be accessed
- **File Permissions**: Files must exist and be readable

### ⚠️ Additional Recommendations for Production:

1. **Add Authentication**
```python
# Install flask-login
pip install flask-login

# In app.py:
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/api/file-content', methods=['POST'])
@login_required  # Add this decorator
def get_file_content():
    # ... rest of function
```

2. **Add Rate Limiting**
```python
pip install flask-limiter

from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/file-content', methods=['POST'])
@limiter.limit("100 per hour")
def get_file_content():
    # ... rest of function
```

3. **HTTPS Only** (Use production WSGI server)
- Heroku: Automatic
- PythonAnywhere: Automatic
- AWS/DigitalOcean: Configure with nginx + Let's Encrypt

4. **Environment Variables** for sensitive data
```python
import os
# Instead of hardcoding paths:
BASE_PATH = os.getenv('BASE_FILE_PATH', r'C:\Users\User\...')
```

---

## 📦 File Structure for Deployment

```
portfolio-site/
├── app.py                 # Main Flask app (UPDATED)
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version for Heroku
├── static/
│   ├── style.css
│   └── images/
├── templates/
│   ├── base.html
│   ├── projects.html    # UPDATED with file viewer
│   └── ...
├── DEPLOYMENT_GUIDE.md   # This file
└── README.md
```

---

## 🧪 Testing File Viewer Locally

The file viewer is already working locally! To test:

1. **Expand a course folder** (e.g., IT210)
2. **Expand a week/topic folder** (e.g., AWS keys)
3. **Click on any file** - Modal should open
4. **Text files** will show content inline
5. **Binary files** will show info with download button
6. **Close button** dismisses the modal

---

## 📝 Files Modified

### `app.py`
- Added `import json, base64, mimetypes`
- Added `is_safe_path()` security function
- Added `ALLOWED_PATHS` configuration
- Added `/api/file-content` endpoint
- Added `/api/file-download` endpoint

### `templates/projects.html`
- Added file viewer modal HTML
- Added CSS styles for modal and file links
- Added JavaScript `viewFile()` function
- Added JavaScript `downloadCurrentFile()` function
- Files now render as clickable links with `onclick="viewFile(...)"`

---

## 🎯 Next Steps

1. **Test Locally**: Verify everything works (Done ✓)
2. **Choose Hosting**: Pick an option from above
3. **Create Account**: Sign up for the service
4. **Deploy**: Follow the platform's deployment guide
5. **Test Remote**: Verify file viewer works remotely
6. **Add Authentication** (Optional): Add login if needed
7. **Monitor**: Check logs for any errors

---

## ⚡ Features Included

✅ Interactive file browser with collapsible folders  
✅ Click files to view in modal  
✅ Text file preview with syntax highlighting  
✅ Binary file download  
✅ Security checks prevent directory traversal  
✅ View-only access (no modifications)  
✅ Error handling and user feedback  
✅ Responsive design  
✅ Mobile-friendly modal  

---

## 🆘 Troubleshooting

### Modal doesn't open
- Check browser console for JavaScript errors
- Verify `/api/file-content` endpoint is accessible
- Check Flask server logs

### "File not found" error
- Verify file path is correct
- Check file permissions
- Ensure file is within `ALLOWED_PATHS`

### Files not displaying as links
- Check that `file.path` is being passed correctly
- Verify template is updated with onclick handlers
- Clear browser cache and reload

### Download button not working
- Check CORS settings if on different domain
- Verify `/api/file-download` endpoint works
- Check file size limits

---

## 📞 Support

For issues, check:
1. Flask documentation: https://flask.palletsprojects.com
2. JavaScript console for errors (F12)
3. Flask server logs for backend errors
4. Your hosting provider's documentation

---

**Ready to deploy? Pick an option from the deployment section above!** 🚀
