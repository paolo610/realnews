# News Feed Site

A simple, clean news feed site that allows authorized users to post content with images. The site uses Python (Flask) for the backend and modern HTML/CSS/JavaScript for the frontend.

## Features

- Clean, modern interface
- User authentication via security keys
- Image upload support
- Mobile-responsive design
- Easy to deploy to GitHub Pages
- No database required (uses CSV files for storage)

## Setup

1. Install Python 3.7 or higher
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `data` directory in the project root
4. Create a `data/users.csv` file with the following format:
   ```
   username,security_key
   ```
   Example:
   ```
   admin,abc123
   user1,xyz789
   ```

## Running Locally

1. Start the Flask server:
   ```
   python app.py
   ```
2. Open your browser and navigate to `http://localhost:5000`

## Deploying to GitHub Pages

1. Create a new GitHub repository
2. Push your code to the repository
3. Enable GitHub Pages in your repository settings
4. Set the source to the main branch

## Security Notes

- Keep your `users.csv` file secure and never commit it to version control
- Regularly rotate security keys
- Consider adding rate limiting for production use

## File Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files
│   ├── style.css      # CSS styles
│   └── uploads/       # Uploaded images
├── templates/         # HTML templates
│   └── index.html     # Main page template
└── data/             # Data storage
    ├── users.csv     # User credentials
    └── posts.csv     # Post content
``` 