# EasyAV - Antivirus Software

A lightweight antivirus scanner built with Python and Tkinter.

## Features

- **File and Folder Scanning**: Scan individual files or entire directories
- **Threat Detection**: Identify potentially dangerous files
- **Scan History**: Keep track of previous scans
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **User-Friendly GUI**: Built with Tkinter for easy use

## Why Virtual Environment (venv)?

Even though Python may be installed on your system, we recommend creating a virtual environment to isolate project dependencies. However, the automated setup scripts now install dependencies directly to your system Python for simplicity.

If you prefer to use a virtual environment, you can create one manually:

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Project Structure

```
EasyAV/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules (excludes venv/)
├── setup.sh                 # Automated setup script (macOS/Linux)
├── setup.bat                # Automated setup script (Windows)
├── scanner/                # File scanning module
│   ├── __init__.py
│   ├── file_scanner.py     # File scanning logic
│   └── threat_detector.py  # Threat detection engine
├── database/               # Database module
│   ├── __init__.py
│   └── signature_db.py     # Signature database management
├── ui/                     # User interface module
│   ├── __init__.py
│   └── main_window.py      # Main GUI window
└── utils/                  # Utility functions
    ├── __init__.py
    └── hash_util.py        # Hash calculation utilities
```

## Setup Instructions

### Option 1: Automated Setup (Recommended)

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
setup.bat
```

The automated setup will:
- Check if Python 3.7+ is installed
- Offer to install Python if missing
- Install all required dependencies directly to system Python
- Provide clear instructions for next steps

### Option 2: Manual Setup

#### Prerequisites

- Python 3.7 or higher
- pip (usually included with Python)

If Python is not installed, the setup scripts will offer to install it for you.

#### Optional: Create Virtual Environment

```bash
cd /path/to/EasyAV
python3 -m venv venv
```

#### Optional: Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

Note: Tkinter is usually included with Python. If not installed, use:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Should be included with Python from python.org

#### 4. Run the Application

```bash
python3 main.py
```

## Usage

1. **Scan a File**: Click "Scan File" to select and scan a single file
2. **Scan a Folder**: Click "Scan Folder" to scan an entire directory
3. **View Results**: Results are displayed in the results pane
4. **Stop Scan**: Click "Stop Scan" to halt the current operation
5. **View History**: Click "View History" to see previous scans

## Features in Detail

### File Scanner
- Calculates SHA256 hashes of files
- Scans individual files and directories
- Supports recursive directory scanning
- Reports file information and threats

### Threat Detector
- Identifies known malware signatures
- Scans file content for threat patterns
- Provides threat severity levels
- Generates threat reports

### Signature Database
- Stores malware signatures
- Tracks scan history
- Manages signature updates
- Stores scan results

## Development

### Adding New Features

1. **New Scan Type**: Modify `scanner/file_scanner.py`
2. **New Detection Rules**: Update `scanner/threat_detector.py`
3. **UI Components**: Modify `ui/main_window.py`
4. **Database Operations**: Update `database/signature_db.py`

### Testing

Create a test file using EICAR test string to verify detection:
```bash
python3
>>> with open('test_file.txt', 'w') as f:
...     f.write('X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*')
```

## Future Enhancements

- [ ] Real-time file monitoring
- [ ] Quarantine system for infected files
- [ ] Network scanning capabilities
- [ ] Auto-update of signatures
- [ ] Scheduled scanning
- [ ] System tray integration
- [ ] Advanced filtering options
- [ ] Dark mode UI

## Requirements

- Python 3.7+
- Tkinter (included with most Python installations)
- No external dependencies by default

## License

See LICENSE file for details.

## Support

For issues or feature requests, please create an issue in the repository.
