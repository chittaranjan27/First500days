# WhatsApp Chat Analyzer

A full-stack web application for analyzing WhatsApp group chat activity. Upload your exported WhatsApp chat file to get insights about user activity over the last 7 days.

## Features

- 📤 **File Upload**: Drag-and-drop or click to upload WhatsApp exported `.txt` files
- 📊 **Analytics Dashboard**: View comprehensive statistics about chat activity
- 📈 **Interactive Charts**: Visualize daily active users and new users with bar charts
- 👥 **User Insights**: Identify most active users (active 4+ days in last 7 days)
- 🎨 **Modern UI**: Clean, responsive design with smooth animations

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: Modern React with hooks
- **Chart.js**: Interactive charting library
- **Plain CSS**: Custom styling (no frameworks)

## Project Structure

```
First500days/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── parser.py         # WhatsApp chat parser
│   ├── analytics.py      # Analytics computation
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js
│   │   │   ├── AnalyticsSummary.js
│   │   │   ├── ChartSection.js
│   │   │   └── UserList.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The app will open at `http://localhost:3000`

## How to Export WhatsApp Chat

1. Open the WhatsApp group chat you want to analyze
2. Tap the three dots menu (⋮) in the top right
3. Select **"More"** → **"Export chat"**
4. Choose **"Without media"** (to keep file size small)
5. Save the `.txt` file to your computer
6. Upload it using the web application

**Note**: The analyzer processes messages from the last 7 days. Make sure your exported chat contains recent messages for meaningful analytics. A sample chat file (`sample_chat.txt`) is included for testing purposes.

## API Endpoints

### `POST /api/analyze`

Upload and analyze a WhatsApp chat file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (file upload)

**Response:**
```json
{
  "success": true,
  "data": {
    "daily_data": [
      {
        "date": "2024-01-15",
        "date_display": "2024-01-15",
        "active_users": 5,
        "new_users": 1
      }
    ],
    "users_active_4plus_days": ["User1", "User2"],
    "summary": {
      "total_active_users": 10,
      "total_new_users": 2,
      "avg_daily_active_users": 5.5,
      "users_active_4plus_days_count": 3
    }
  },
  "total_messages": 150
}
```

## Features Explained

### Chat Parsing
- Handles multiple date formats (DD/MM/YYYY, MM/DD/YYYY, etc.)
- Supports both 12-hour and 24-hour time formats
- Detects system messages (user joined/left)
- Handles multiline messages correctly

### Analytics Computation
- Calculates metrics for the last 7 days (including today)
- Tracks daily active users (users who sent messages)
- Tracks new users (users who joined the group)
- Identifies users active on 4+ different days

### Data Visualization
- Interactive bar chart showing:
  - Blue bars: Active users per day
  - Orange bars: New users per day
- Responsive design that works on all screen sizes

## Error Handling

The application handles various error cases:
- Invalid file types (non-.txt files)
- Files exceeding 10MB size limit
- Malformed chat files
- Network errors
- Empty or invalid chat exports

## Browser Support

Optimized for the latest Chrome browser. Other modern browsers should work but may have minor styling differences.

## Development Notes

- Backend uses FastAPI for automatic API documentation (available at `http://localhost:8000/docs`)
- Frontend uses React hooks for state management
- All components are modular and reusable
- CSS uses modern features like CSS Grid and Flexbox
- No external CSS frameworks used (pure CSS)

## License

This project is created for educational/demonstration purposes.
