# 🚀 Streamlit Cloud Deployment Guide

## Deploy CrowdFlow AI on Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://share.streamlit.io/)

### Step 1: Prepare Your Repository

1. **Ensure your repository is on GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Verify these files are in your repository:**
   - `streamlit_app.py` (main entry point)
   - `requirements.txt` (dependencies)
   - `.streamlit/config.toml` (configuration)
   - `src/` (source code)
   - `src/config.yaml` (configuration)

### Step 2: Deploy on Streamlit Cloud

**Option A: Simple Deployment (Recommended)**
1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository: `Kenvin26/Crowdflow-AI`
   - Set main file path: `streamlit_app_simple.py`
   - Click "Deploy!"

**Option B: Full Deployment (May have OpenCV issues)**
1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select your repository: `Kenvin26/Crowdflow-AI`
   - Set main file path: `streamlit_app.py`
   - Click "Deploy!"

3. **Wait for Deployment**
   - Streamlit will install dependencies
   - This may take 5-10 minutes for the first deployment
   - You'll see build logs in real-time

### Step 3: Access Your App

- Your app will be available at: `https://your-app-name.streamlit.app`
- Share this URL with others!

### Step 4: Monitor and Update

- **View logs**: Click on your app → "Manage app" → "Logs"
- **Update**: Push changes to GitHub → Streamlit auto-deploys
- **Settings**: Configure in `.streamlit/config.toml`

## 🔧 Configuration Options

### Environment Variables (Optional)
In Streamlit Cloud settings, you can set:
- `YOLO_MODEL_PATH`: Custom YOLO model path
- `API_URL`: Custom API endpoint
- `DEBUG_MODE`: Enable debug logging

### Custom Domain (Optional)
- Upgrade to Streamlit Teams for custom domains
- Configure in app settings

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors**
   - Check `requirements.txt` has all dependencies
   - Verify import paths in `streamlit_app.py`

2. **File Not Found**
   - Ensure all files are committed to GitHub
   - Check file paths are relative to repository root

3. **Memory Issues**
   - Streamlit Cloud has memory limits
   - Optimize video processing for smaller files
   - Consider using sample videos for demo

4. **Build Failures**
   - Check build logs in Streamlit Cloud
   - Verify Python version compatibility
   - Ensure all dependencies are available

### Performance Tips:

1. **Optimize for Cloud**
   - Use smaller video files for demo
   - Implement caching with `@st.cache_data`
   - Limit video processing time

2. **Reduce Dependencies**
   - Remove unused packages from `requirements.txt`
   - Use lighter alternatives where possible

3. **Error Handling**
   - Add try-catch blocks for file operations
   - Provide user-friendly error messages

## 📊 Monitoring

### Streamlit Cloud Dashboard:
- **Usage**: View app usage statistics
- **Performance**: Monitor response times
- **Errors**: Check error logs
- **Deployments**: Track deployment history

### Logs to Watch:
- Import errors
- File access issues
- Memory usage warnings
- Processing timeouts

## 🔄 Updates and Maintenance

### Automatic Updates:
- Push to `main` branch → auto-deploy
- Streamlit rebuilds on every push

### Manual Updates:
- Go to app settings → "Reboot app"
- Useful for clearing cache/memory

### Version Control:
- Tag releases: `git tag v1.0.0`
- Use branches for features
- Keep `main` branch stable

## 🎯 Best Practices

1. **Keep it Light**
   - Small video files for demo
   - Efficient processing algorithms
   - Minimal dependencies

2. **User Experience**
   - Clear error messages
   - Loading indicators
   - Responsive design

3. **Security**
   - Validate file uploads
   - Sanitize user inputs
   - Use environment variables for secrets

4. **Documentation**
   - Clear README
   - In-app help
   - Code comments

## 🚀 Advanced Features

### Custom Components:
- Create custom Streamlit components
- Integrate with external APIs
- Add real-time updates

### Database Integration:
- Connect to external databases
- Store user preferences
- Cache processed results

### Authentication:
- Add user authentication
- Restrict access to features
- Track usage per user

---

**Your CrowdFlow AI app is now live on Streamlit Cloud! 🎉** 