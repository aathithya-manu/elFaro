# El Faro 🏙️

**Report local civic issues easily with the power of AI and location services**

El Faro is a web application that empowers citizens to report civic issues by uploading images, automatically generating detailed reports using AI, and facilitating communication with local authorities.

## ✨ Features

- **📸 Image Upload & Analysis**: Upload photos of civic issues for AI-powered analysis
- **🗺️ Interactive Maps**: Google Maps integration with location selection and search
- **🤖 AI Report Generation**: Automatic generation of detailed civic reports from images
- **📧 Email Integration**: Direct communication with relevant authorities
- **📄 PDF Export**: Download reports as PDF documents
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🎨 Modern UI**: Clean, intuitive interface with smooth animations

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Flask web framework
- Google Maps API key
- AI/ML service for image analysis (configuration dependent on your backend)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/el-faro.git
cd el-faro
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file and add your API keys
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
# Add other required API keys for image analysis
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## 🔧 Configuration

### Google Maps API

1. Get a Google Maps API key from the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the following APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API
3. Replace the API key in the HTML file or use environment variables

### Backend Routes

The application expects the following Flask routes to be implemented:

- `POST /analyze_image` - Handles image upload and AI analysis
- `POST /submit_report` - Processes and submits the generated report
- `POST /download_pdf` - Generates and downloads PDF reports
- `POST /send_email` - Sends reports via email to authorities

## 📁 Project Structure

```
el-faro/
│
├── templates/
│   └── index.html          # Main application template
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/            # Directory for uploaded images
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .env                   # Environment variables (not in repo)
```

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python Flask
- **Maps**: Google Maps JavaScript API
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)

## 🎨 UI Features

- **Modern Design**: Clean, professional interface with smooth animations
- **Responsive Layout**: CSS Grid layout that adapts to different screen sizes
- **Interactive Elements**: Hover effects, smooth transitions, and visual feedback
- **Accessibility**: Proper contrast ratios and semantic HTML structure

## 🔄 Workflow

1. **Upload Image**: Users upload photos of civic issues
2. **Select Location**: Interactive map allows precise location selection
3. **AI Analysis**: Backend processes the image and generates a detailed report
4. **Edit & Review**: Users can edit the auto-generated report before submission
5. **Submit**: Reports are sent to relevant authorities via email
6. **Export**: Users can download PDF copies of their reports

## 🚦 API Endpoints

### Image Analysis
```
POST /analyze_image
Content-Type: multipart/form-data

Parameters:
- image: Image file
- location_address: Street address
- location_latlng: Latitude,longitude coordinates
```

### Report Submission
```
POST /submit_report
Content-Type: application/x-www-form-urlencoded

Parameters:
- edited_report: Modified report text
- recipient_email: Authority email address
```

### PDF Download
```
POST /download_pdf
Content-Type: application/x-www-form-urlencoded

Parameters:
- report_to_download: Report content for PDF generation
```

### Email Sending
```
POST /send_email
Content-Type: application/x-www-form-urlencoded

Parameters:
- recipient_email: Destination email
- report_to_send: Report content
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any problems or have suggestions, please open an issue on GitHub or contact the maintainers.

## 🙏 Acknowledgments

- Google Maps API for location services
- Font Awesome for icons
- Google Fonts for typography
- The open-source community for inspiration and tools

---

**Made with ❤️ for better civic engagement**
