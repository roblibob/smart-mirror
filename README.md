# Smart Mirror - Smart Home AI Assistant

This project is a **smart mirror** powered by **face recognition**, **Gemini AI**, and **Electron UI**, with integrations for **Home Assistant**.

---

## **1. Installation**

### **1.1 Clone the Repository**
```bash
git clone https://github.com/yourusername/magic-mirror.git
cd smart-mirror
```

### **1.2 Set Up Python Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# On Windows (if needed): venv\Scripts\activate
```

### **1.3 Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **1.4 Set Up Node.js for Electron UI**
Ensure **Node.js** and **npm** are installed:
```bash
node -v  # Check Node.js version
npm -v   # Check npm version
```
If not installed, install it via [Node.js website](https://nodejs.org/) or:
```bash
brew install node  # macOS
sudo apt install nodejs npm  # Ubuntu/Debian
```

Then, install Electron dependencies:
```bash
cd ui
npm install
cd ..
```

---

## **2. Configuration**

### **2.1 Set Up API Keys**
Update the `.env` file inside the project root:
```
GEMINI_API_KEY=your-google-api-key
HOME_ASSISTANT_URL=http://your-home-assistant-ip:8123
```

### **2.2 Ensure Camera Permissions**
If running on macOS, grant access to the camera in `System Preferences > Security & Privacy > Camera`.

---

## **3. Running the Smart Mirror**

### **3.1 Start the FastAPI Server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **3.2 Start Face Recognition**
```bash
python face_detect.py
```

### **3.3 Start Electron UI**
```bash
cd magic-mirror-electron
electron .
```

---

## **4. Additional Features**
- **Face recognition with multi-face tracking**
- **Real-time greetings via Gemini AI**
- **Home Assistant integration for automation**
- **Electron-based UI for smart display**
