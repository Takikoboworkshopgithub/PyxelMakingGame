
#!/bin/bash

cd "$(dirname "$0")"

echo "Starting server..."
echo "Open http://localhost:8000/index.html in your browser."
echo "Press Ctrl+C to stop the server."

python3 -m http.server 8000
