# 💘 PlanMyValentine - Quick Start Guide

## ✅ PROJECT STATUS: READY TO RUN!

All components have been successfully created and configured.

## 🚀 How to Run

### 1. Set Up OpenAI API Key (Required for AI features)

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Get your API key:** https://platform.openai.com/api-keys

**Note:** The app will still work without an API key using fallback plans, but AI-powered personalization won't be available.

### 2. Start the Server

```powershell
python manage.py runserver
```

Or use the Python path:
```powershell
D:/Valentine/.venv/Scripts/python.exe manage.py runserver
```

### 3. Open in Browser

Navigate to: **http://127.0.0.1:8000/**

### 4. Create Admin User (Optional)

To access the admin panel:

```powershell
python manage.py createsuperuser
```

Then visit: **http://127.0.0.1:8000/admin/**

## 📁 What's Been Built

### ✅ Complete Features

1. **Landing Page** 💘
   - Beautiful pink/red gradient theme
   - 4 CTA options (Valentine, Crush, Bestie, Self-Love)
   - Dark mode toggle
   - Fully responsive

2. **Planner Form** 📝
   - Chat-style form with emoji labels
   - Fields: Names, relationship type, city, budget, duration, vibe
   - Real-time validation
   - Loading states

3. **AI Plan Generation** 🤖
   - OpenAI GPT-3.5 integration
   - Different prompts for each relationship type
   - City-based suggestions (5 cities hardcoded)
   - Fallback plans if API unavailable
   - Structured 1-day or 7-day format

4. **Result Page** ✨
   - Beautiful plan display
   - WhatsApp share integration
   - Copy link functionality
   - View counter
   - Action buttons for extra features

5. **Viral Features** 🔥
   - **Confession Mode**: Anonymous sharing with reveal option
   - **Love Letter Generator**: AI-powered personalized letters
   - **Reaction System**: 5 emoji reactions (Loved, Shocked, Emotional, Laughing, Crying)
   - **Share Page**: Public view with reaction buttons

6. **Location Intelligence** 📍
   - Hardcoded suggestions for:
     - Bhubaneswar (temples, cafes, walks)
     - Delhi (India Gate, Hauz Khas, etc.)
     - Mumbai (Marine Drive, Gateway, etc.)
     - Bangalore (Lalbagh, Cubbon Park, etc.)
     - Kolkata (Victoria Memorial, Park Street, etc.)

7. **Design & UX** 🎨
   - Bootstrap 5 responsive design
   - Pink/red gradient theme
   - Dark mode support
   - Mobile-first approach
   - Animations and transitions
   - Confetti celebration effect
   - Print-friendly styles

### 📊 Database Models

- **ValentinePlan**: Stores plans, tracks views, handles anonymous mode
- **Reaction**: Stores emoji reactions to shared plans
- **LoveLetter**: Stores AI-generated love letters

### 🎯 URLs

| URL | Description |
|-----|-------------|
| `/` | Landing page |
| `/planner/create/` | Plan creation form |
| `/planner/result/<code>/` | Creator's result page |
| `/planner/share/<code>/` | Public share page |
| `/planner/letter/<code>/` | Love letter view |
| `/admin/` | Admin panel |

## 🧪 Testing the App

### Test Flow 1: Valentine Plan
1. Click "Plan for My Valentine"
2. Fill form with:
   - Names: "Rajeeb" & "Ananya"
   - Relationship: Girlfriend/Boyfriend
   - City: "Bhubaneswar"
   - Budget: 3000
   - Duration: 1 Day
   - Vibe: Romantic
3. Submit and see AI-generated plan
4. Try WhatsApp share
5. Generate love letter

### Test Flow 2: Crush Mode
1. Click "Plan for My Crush"
2. Fill details with vibe "Funny"
3. Get bold and mysterious plan
4. Enable "Confession Mode"
5. Share anonymously

### Test Flow 3: Bestie Anti-Valentine
1. Click "Plan for My Friend"
2. Select "Best Friend" relationship
3. Get roast-style fun plan with pizza & memes

### Test Flow 4: Reactions
1. Create and share a plan
2. Open share link in incognito/another browser
3. Add reactions (emojis)
4. See reaction count update

## 🎨 Theme Customization

Colors are defined in `static/css/style.css`:

```css
:root {
    --primary-pink: #ff1744;
    --gradient-start: #ff1744;
    --gradient-end: #ff4081;
}
```

Toggle dark mode with the moon/sun button (top-right).

## 🔧 Configuration

### settings.py
- Apps: `core`, `planner`
- Database: SQLite (easy to switch to PostgreSQL)
- Static files configured
- Timezone: Asia/Kolkata

### API Configuration
- OpenAI API key in `.env`
- Model: GPT-3.5-turbo
- Temperature: 0.8 (creative)
- Max tokens: 2000

## 📱 Mobile Testing

The app is fully responsive. Test on:
- Chrome DevTools mobile view
- Real mobile devices
- Tablet sizes

## 🐛 Common Issues

### Issue: OpenAI API Error
**Solution:** Check API key in `.env` or use without API (fallback mode)

### Issue: Static files not loading
**Solution:** Make sure you're in the correct directory
```powershell
cd d:\Valentine
python manage.py runserver
```

### Issue: Port already in use
**Solution:** Use different port
```powershell
python manage.py runserver 8080
```

## 🚀 Next Steps

### Before Launch
1. ✅ Add your OpenAI API key to `.env`
2. ✅ Test all features thoroughly
3. ✅ Create some sample plans
4. ✅ Test on mobile devices

### For Production
1. Change `SECRET_KEY` in settings
2. Set `DEBUG = False`
3. Add domain to `ALLOWED_HOSTS`
4. Switch to PostgreSQL
5. Set up proper static file serving
6. Configure SSL certificate

### Marketing & Launch
1. Domain: planmyvalentine.ai
2. Deploy on Render/Railway
3. Create social media assets
4. Share on Product Hunt
5. Reddit launch (r/SideProject)
6. LinkedIn post for portfolio

## 💡 Tips

1. **Test Without API**: The app works with fallback plans if no API key
2. **Dark Mode**: Automatically saves user preference
3. **Share Links**: Each plan gets unique shareable URL
4. **Admin Panel**: Monitor all plans, reactions, analytics
5. **No Login**: Zero friction = higher conversion

## 🎯 Portfolio Highlights

When showcasing this project:

✅ **Full-Stack Django App**
✅ **AI/ML Integration (OpenAI GPT)**
✅ **Modern UI/UX (Bootstrap 5, Dark Mode)**
✅ **Viral Features (Confession Mode, Reactions)**
✅ **Mobile-First Responsive Design**
✅ **Zero-Login Architecture**
✅ **Production-Ready Code Structure**

## 📸 Screenshots to Take

1. Landing page (light & dark mode)
2. Form with filled data
3. Generated plan result
4. Love letter
5. Share page with reactions
6. Mobile view
7. Admin panel

## 🎉 You're Ready!

Everything is set up and ready to run. Just add your OpenAI API key and start the server!

```powershell
python manage.py runserver
```

**Happy Valentine's Day! 💘**

---

Need help? Check the main README.md for detailed documentation.
