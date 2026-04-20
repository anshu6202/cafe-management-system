# Images for Login and Signup pages - CURRENTLY USING EXTERNAL URLs

The login and signup pages are currently using external image URLs from Unsplash for immediate functionality.
For production, you should replace these with local images for better performance and reliability.

Current external URLs being used:
- Logo: https://images.unsplash.com/photo-1559056199-641a0ac8b55e?auto=format&fit=crop&w=100&q=80
- Login decoration: https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=200&q=80
- Signup decoration: https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=200&q=80
- Login background: https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1200&q=80
- Signup background: https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80

To use local images instead, add these files to this folder:
1. cafe-logo.png - A circular logo for CafeMate (80x80px recommended)
2. login-bg.jpg - Background image for login page (1200x800px recommended, coffee/cafe related)
3. signup-bg.jpg - Background image for signup page (1200x800px recommended, welcoming/cafe related)
4. coffee-cup.png - Decorative coffee cup image for login panel (120x120px recommended)
5. cafe-signup.png - Decorative image for signup panel (120x120px recommended)

Then update the templates and CSS to use {% static 'images/filename' %} instead of external URLs.