# 🏗️ ARCHITECTURE DIAGRAM

## System Architecture - PlanMyValentine

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                               │
│                    (Bootstrap 5 + Custom CSS)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Landing Page (/)           Planner Form            Result Page     │
│  ┌──────────┐              ┌──────────┐           ┌──────────┐    │
│  │ 4 CTA    │              │ 7 Fields │           │ AI Plan  │    │
│  │ Buttons  │──────────────│ + Submit │──────────│ Display  │    │
│  │          │              │          │           │          │    │
│  └──────────┘              └──────────┘           └──────────┘    │
│       │                         │                       │          │
│       │                         │                       │          │
│       └─────────────────────────┴───────────────────────┘          │
│                                 │                                  │
└─────────────────────────────────┼──────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        DJANGO BACKEND                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐         ┌──────────────────┐                │
│  │   CORE APP       │         │   PLANNER APP    │                │
│  ├──────────────────┤         ├──────────────────┤                │
│  │ • home view      │         │ • planner_form   │                │
│  │ • prompts.py     │◄────────│ • result         │                │
│  │ • utils.py       │         │ • share          │                │
│  │ • city data      │         │ • reactions      │                │
│  └──────────────────┘         │ • love_letter    │                │
│                               └──────────────────┘                │
│                                        │                            │
│                                        ▼                            │
│  ┌─────────────────────────────────────────────┐                  │
│  │              URL ROUTING                     │                  │
│  ├─────────────────────────────────────────────┤                  │
│  │ /                    → home                  │                  │
│  │ /planner/create/     → planner_form         │                  │
│  │ /planner/result/<>   → result               │                  │
│  │ /planner/share/<>    → share                │                  │
│  │ /planner/letter/<>   → view_letter          │                  │
│  └─────────────────────────────────────────────┘                  │
│                                                                      │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────┐                ┌────────────────────┐      │
│  │   OpenAI API       │                │   WhatsApp API     │      │
│  ├────────────────────┤                ├────────────────────┤      │
│  │ • GPT-3.5-turbo    │                │ • Share links      │      │
│  │ • Plan generation  │                │ • Pre-filled text  │      │
│  │ • Love letters     │                │                    │      │
│  │ • Fallback mode    │                │                    │      │
│  └────────────────────┘                └────────────────────┘      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DATABASE                                     │
│                      (SQLite / PostgreSQL)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ ValentinePlan    │  │ Reaction         │  │ LoveLetter       │ │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤ │
│  │ • plan_id (PK)   │  │ • id (PK)        │  │ • id (PK)        │ │
│  │ • share_code     │  │ • plan (FK) ─────┼──│ • plan (FK) ─────┼ │
│  │ • names          │  │ • reaction_type  │  │ • letter_content │ │
│  │ • relationship   │  │ • created_at     │  │ • created_at     │ │
│  │ • city, budget   │  │ • reactor_ip     │  │                  │ │
│  │ • plan_content   │  └──────────────────┘  └──────────────────┘ │
│  │ • view_count     │                                              │
│  │ • is_anonymous   │                                              │
│  └──────────────────┘                                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
USER JOURNEY - Creating a Valentine Plan
═══════════════════════════════════════

1. Landing Page
   │
   ├─► User clicks CTA button (Valentine/Crush/Bestie)
   │
   ▼
2. Planner Form
   │
   ├─► User fills 7 fields
   │   • Your name, Partner name
   │   • Relationship type
   │   • City, Budget
   │   • Duration, Vibe
   │
   ├─► Form validates
   │
   ├─► Submit button clicked
   │
   ▼
3. Backend Processing
   │
   ├─► Django view receives POST data
   │
   ├─► Create ValentinePlan object
   │
   ├─► Generate unique share_code
   │
   ├─► Build AI prompt based on inputs
   │   └─► Include city suggestions if available
   │
   ├─► Call OpenAI API
   │   ├─► Success: Use AI-generated plan
   │   └─► Failure: Use fallback plan
   │
   ├─► Save plan to database
   │
   ├─► Store plan_id in session
   │
   ▼
4. Result Page
   │
   ├─► Display generated plan
   │
   ├─► Show share buttons
   │   ├─► WhatsApp
   │   ├─► Copy link
   │   └─► Download/Print
   │
   ├─► Action buttons (if creator)
   │   ├─► Generate Love Letter
   │   └─► Make Anonymous
   │
   ├─► View reactions
   │
   ▼
5. Sharing
   │
   ├─► User shares link
   │
   ├─► Recipient opens link
   │
   ├─► Share page displays
   │   ├─► Anonymous mode check
   │   └─► Show plan content
   │
   ├─► Recipient reacts
   │   └─► Reaction saved to DB
   │
   ▼
6. Viral Loop
   │
   └─► Recipient creates own plan
       └─► Cycle repeats
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HTML Templates           CSS Styling         JavaScript        │
│  ┌──────────────┐        ┌──────────┐        ┌──────────┐     │
│  │ base.html    │◄───────│ style.css│◄───────│ main.js  │     │
│  │ home.html    │        │          │        │          │     │
│  │ form.html    │        │ • Theme  │        │ • Toggle │     │
│  │ result.html  │        │ • Colors │        │ • Copy   │     │
│  │ share.html   │        │ • Layout │        │ • Share  │     │
│  │ letter.html  │        │          │        │          │     │
│  └──────────────┘        └──────────┘        └──────────┘     │
│         │                                            │          │
└─────────┼────────────────────────────────────────────┼──────────┘
          │                                            │
          ▼                                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MIDDLEWARE LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Django Middleware Stack                                        │
│  ┌────────────────────────────────────────────────────┐        │
│  │ • Security                                          │        │
│  │ • Session                                           │        │
│  │ • CSRF Protection                                   │        │
│  │ • Authentication (not used but available)           │        │
│  │ • Messages                                          │        │
│  └────────────────────────────────────────────────────┘        │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Django Views              Forms                Models           │
│  ┌──────────────┐        ┌──────────┐        ┌──────────┐     │
│  │ home()       │        │ Planner  │        │ Valentine│     │
│  │ planner_form │◄───────│ Form     │◄───────│ Plan     │     │
│  │ result()     │        │          │        │          │     │
│  │ share()      │        │ Reaction │        │ Reaction │     │
│  │ add_reaction │        │ Form     │        │          │     │
│  │ generate_    │        │          │        │ Love     │     │
│  │ letter()     │        │          │        │ Letter   │     │
│  └──────────────┘        └──────────┘        └──────────┘     │
│         │                                            │          │
│         ├────────────────────────────────────────────┘          │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────┐         │
│  │            Business Logic                         │         │
│  ├──────────────────────────────────────────────────┤         │
│  │ • prompts.py (AI integration)                    │         │
│  │ • utils.py (helper functions)                    │         │
│  │ • City suggestions (hardcoded)                   │         │
│  └──────────────────────────────────────────────────┘         │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Django ORM               Database              Cache            │
│  ┌──────────────┐        ┌──────────┐        ┌──────────┐     │
│  │ QuerySets    │◄───────│ SQLite   │        │ Session  │     │
│  │ Managers     │        │          │        │ Storage  │     │
│  │ Validators   │        │ Tables:  │        │          │     │
│  │              │        │ • plans  │        │ • plan_id│     │
│  │              │        │ • react  │        │ • theme  │     │
│  │              │        │ • letters│        │          │     │
│  └──────────────┘        └──────────┘        └──────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Feature Dependency Map

```
FEATURE RELATIONSHIPS
═══════════════════

Core Features
├─ Landing Page
│  └─ Directs to → Planner Form
│
├─ Planner Form
│  ├─ Requires → Form validation
│  ├─ Requires → Database connection
│  ├─ Creates → ValentinePlan
│  └─ Triggers → AI Generation
│
├─ AI Generation
│  ├─ Uses → OpenAI API
│  ├─ Uses → City suggestions
│  ├─ Falls back → Fallback plans
│  └─ Produces → Plan content
│
└─ Result Display
   ├─ Shows → Generated plan
   └─ Enables → Share features

Viral Features
├─ Share System
│  ├─ Generates → Unique share code
│  ├─ Creates → Shareable link
│  └─ Tracks → View count
│
├─ Reaction System
│  ├─ Requires → Shared link
│  ├─ Creates → Reaction objects
│  └─ Displays → Reaction counts
│
├─ Confession Mode
│  ├─ Toggles → is_anonymous flag
│  ├─ Hides → Sender name
│  └─ Allows → Reveal action
│
└─ Love Letter
   ├─ Uses → OpenAI API
   ├─ Creates → LoveLetter object
   └─ Links to → Parent plan

UI Features
├─ Theme Toggle
│  ├─ Switches → Light/Dark mode
│  ├─ Saves → Local storage
│  └─ Updates → CSS variables
│
├─ Mobile Responsive
│  ├─ Uses → Bootstrap grid
│  ├─ Adapts → Card layouts
│  └─ Optimizes → Touch targets
│
└─ Animations
   ├─ Fade-in → On scroll
   ├─ Confetti → On success
   └─ Transitions → On hover
```

## Security Architecture

```
SECURITY LAYERS
═══════════════

1. CSRF Protection
   └─ All POST forms include {% csrf_token %}

2. Input Validation
   ├─ Django Forms validation
   ├─ Database field constraints
   └─ HTML5 client-side validation

3. SQL Injection Prevention
   └─ Django ORM (parameterized queries)

4. XSS Prevention
   ├─ Template auto-escaping
   └─ Safe content rendering

5. Environment Variables
   ├─ API keys in .env
   ├─ SECRET_KEY protected
   └─ Never committed to git

6. Optional Privacy
   ├─ No user accounts required
   ├─ Anonymous sharing option
   └─ IP tracking (optional, for analytics)
```

---

**Architecture Summary:**

- **Layered MVC Architecture**: Clean separation of concerns
- **Stateless Session**: No login required, session for creator tracking only
- **API Integration**: OpenAI with graceful degradation
- **Responsive Frontend**: Bootstrap 5 with custom styling
- **Scalable Database**: SQLite dev → PostgreSQL prod
- **Viral Mechanics**: Share codes, reactions, anonymous mode
- **Security First**: CSRF, XSS, SQL injection protection
- **Mobile Optimized**: Touch-friendly, responsive design

---

This architecture supports:
- ✅ Rapid development and deployment
- ✅ Easy maintenance and updates
- ✅ Horizontal scaling potential
- ✅ Feature extensibility
- ✅ Security best practices
- ✅ Performance optimization
