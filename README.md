# SafeChat: A Secure and Abuse-Resistant Messaging Platform

SafeChat is a lightweight, secure messaging platform designed to prioritize user safety and privacy. This project demonstrates real-world applications of trust and safety engineering, including secure user authentication, real-time messaging, and abuse detection. 

## Features

### User Authentication
- Secure user login and registration using JSON Web Tokens (JWT).
- Passwords are hashed and salted with bcrypt for enhanced security.

### Real-Time Messaging
- Users can send and receive messages in real-time via WebSocket or REST-based polling.
- Messages are stored securely in a MySQL database with timestamps and sender/receiver information.

### Spam and Abuse Detection
- Rule-based and machine-learning-based abuse detection.
- Flag messages containing spam or offensive content and notify users.

### RESTful API
- APIs for user registration, login, message sending, and abuse reporting.
- Robust error handling, input validation, and rate-limiting.

### Secure Data Transmission
- HTTPS for secure communication.
- End-to-end encryption for messages (planned in future updates).

### Interactive SwiftUI Client (Planned)
- A user-friendly iOS/macOS app for sending and receiving messages.
- Displays flagged content and abuse warnings.

## Getting Started

### Prerequisites
- Python 3.8+
- MySQL Server
- Git
- Flask and required libraries (listed in `requirements.txt`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SafeChat.git
   cd SafeChat
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database in `config.py`:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/safechat'
   ```

5. Run the app:
   ```bash
   flask run
   ```

### Usage
- Register a new user: `POST /auth/register`
- Login: `POST /auth/login`
- Send messages: `POST /messages`
- Fetch messages: `GET /messages`
- Report abuse: `POST /report`

## Folder Structure
```
SafeChat/
├── app/
│   ├── __init__.py         # App initialization and configuration
│   ├── models.py           # Database models
│   ├── routes.py           # API routes for authentication and messaging
│   ├── utils.py            # Utility functions (e.g., abuse detection)
├── migrations/             # Database migrations
├── config.py               # Configuration file
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Future Enhancements
- **End-to-End Encryption:** Encrypt messages for enhanced privacy.
- **Machine Learning Integration:** Advanced sentiment analysis for abuse detection.
- **Interactive SwiftUI Client:** Build a polished iOS/macOS app for SafeChat.
- **Scalability Improvements:** Optimize performance for high-concurrency scenarios.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contact
For questions or feedback, please contact the project maintainer:
- Name: Michael Danylchuk
- Email: mn_danylchuk@me.com
