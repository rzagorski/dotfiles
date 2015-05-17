server {
    listen 80;

    root /home/virtual/malinowski.be;
    index index.html;

    server_name malinowski.be;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
