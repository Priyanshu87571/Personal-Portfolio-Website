# Deployment checklist

- [ ] Verify every profile detail, achievement, project description, and link.
- [ ] Replace example admin credentials and generate a unique JWT secret.
- [ ] Configure a managed PostgreSQL database for production.
- [ ] Set environment variables in the hosting provider; do not upload `.env`.
- [ ] Configure the frontend API URL to the public HTTPS API endpoint.
- [ ] Set exact production CORS origins and enable HTTPS.
- [ ] Run backend tests and build the frontend (`npm run build`).
- [ ] Add database migrations, backups, logging, and production rate limiting before relying on the site.
- [ ] Add your resume PDF if you want a download link.
