from datetime import datetime, timedelta, timezone
from typing import Optional
import os
import time
from collections import defaultdict, deque

import jwt
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pwdlib import PasswordHash
from sqlalchemy import create_engine, String, Text, Integer, Boolean, DateTime, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./portfolio.db")
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
JWT_SECRET = os.getenv("JWT_SECRET", "local-development-secret-change-this-before-deploying")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com").strip().lower()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-me-now")
password_hash = PasswordHash.recommended()
bearer = HTTPBearer(auto_error=False)

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    stack: Mapped[str] = mapped_column(String(300), default="")
    github_url: Mapped[str] = mapped_column(String(500), default="")
    live_url: Mapped[str] = mapped_column(String(500), default="")
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=100)

class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    category: Mapped[str] = mapped_column(String(80), default="Tools")
    sort_order: Mapped[int] = mapped_column(Integer, default=100)

class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    organization: Mapped[str] = mapped_column(String(180), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    date_label: Mapped[str] = mapped_column(String(80), default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=100)

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    subject: Mapped[str] = mapped_column(String(160), default="")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ProjectIn(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=5, max_length=3000)
    stack: str = Field(default="", max_length=300)
    github_url: str = Field(default="", max_length=500)
    live_url: str = Field(default="", max_length=500)
    featured: bool = False
    sort_order: int = 100

class SkillIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    category: str = Field(default="Tools", max_length=80)
    sort_order: int = 100

class AchievementIn(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    organization: str = Field(default="", max_length=180)
    description: str = Field(default="", max_length=3000)
    date_label: str = Field(default="", max_length=80)
    sort_order: int = 100

class ContactIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(default="", max_length=160)
    message: str = Field(min_length=10, max_length=4000)

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=256)

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class ProjectOut(ORMModel):
    id: int
    title: str
    description: str
    stack: str
    github_url: str
    live_url: str
    featured: bool
    sort_order: int

class SkillOut(ORMModel):
    id: int
    name: str
    category: str
    sort_order: int

class AchievementOut(ORMModel):
    id: int
    title: str
    organization: str
    description: str
    date_label: str
    sort_order: int

class MessageOut(ORMModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    created_at: datetime

app = FastAPI(title="Priyanshu Raj Portfolio API", version="1.0.0", description="Portfolio content, contact, and admin APIs")
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:8080,http://localhost:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Authorization", "Content-Type"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def dump(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}

def seed_data(db: Session):
    if db.scalar(select(Project.id).limit(1)) is None:
        db.add_all([
            Project(title="DeployGuard — AI-Powered CI/CD Failure Detection", description="A developer-tool project focused on detecting failed GitHub Actions runs and helping investigate the failure context. Keep feature claims aligned with the version that is publicly deployed and tested.", stack="React · TypeScript · Python · FastAPI · GitHub Actions", github_url="", featured=True, sort_order=1),
            Project(title="AI Resume Analyzer", description="A resume-analysis application with resume parsing, ATS-style score analysis, AI-generated interview questions, and JWT authentication, as described in the public repository README.", stack="React · Node.js · Express · MongoDB · Gemini AI", github_url="https://github.com/Priyanshu87571/AI-Resume-Analyzer", featured=True, sort_order=2),
            Project(title="Event Booking Platform", description="A full-stack event booking platform with user authentication, email OTP verification, event management, ticket booking, and booking history.", stack="React · Node.js · Express · MongoDB · JWT", github_url="https://github.com/Priyanshu87571/Event-Booking", featured=True, sort_order=3),
            Project(title="Smart Inventory & Order Management", description="A MERN application for product and inventory CRUD, order processing, order history, and operational statistics.", stack="React · Node.js · Express · MongoDB · MERN", github_url="https://github.com/Priyanshu87571/smart-inventory-order-management", featured=False, sort_order=4),
        ])
    if db.scalar(select(Skill.id).limit(1)) is None:
        skills = [
            ("C++", "Programming"), ("Python", "Programming"), ("C", "Programming"), ("JavaScript", "Programming"), ("TypeScript", "Programming"),
            ("React", "Frontend"), ("HTML & CSS", "Frontend"), ("Node.js", "Backend"), ("Express.js", "Backend"), ("FastAPI", "Backend"),
            ("REST APIs", "Backend"), ("MongoDB", "Database"), ("PostgreSQL", "Database"), ("SQL", "Database"),
            ("Git & GitHub", "Tools"), ("Docker", "Tools"), ("Google Cloud", "AI & Cloud"), ("Vertex AI", "AI & Cloud"), ("BigQuery", "AI & Cloud"),
            ("Data Structures & Algorithms", "Computer Science"),
        ]
        db.add_all([Skill(name=n, category=c, sort_order=i) for i, (n,c) in enumerate(skills, 1)])
    if db.scalar(select(Achievement.id).limit(1)) is None:
        db.add_all([
            Achievement(title="Microsoft Learn Student Ambassadors — Associate Milestone", organization="Microsoft", description="Community and learning milestone. Confirm the exact current program title and date before publishing.", date_label="2026", sort_order=1),
            Achievement(title="GeeksforGeeks Campus Mantri", organization="GeeksforGeeks", description="Campus community role promoting coding practice and technical learning.", date_label="", sort_order=2),
            Achievement(title="Campus Ambassador", organization="Edwise International", description="Campus ambassador and student engagement activities.", date_label="", sort_order=3),
            Achievement(title="Software Engineer Intern Certificate", organization="Certificate", description="Add issuer, date, and verified details of the certificate.", date_label="", sort_order=4),
            Achievement(title="Front-End Developer Intern", organization="CODEXINTERN", description="Experience described on the supplied GitHub profile README; verify dates and exact responsibilities.", date_label="", sort_order=5),
            Achievement(title="GeeksforGeeks Problem Solving", organization="GeeksforGeeks", description="Previously shared profile metrics: 254+ problems solved and coding score 759. Update to current verified figures.", date_label="", sort_order=6),
        ])
    db.commit()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_data(db)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(select(1))
    return {"status": "ok", "database": "connected"}

@app.get("/api/profile")
def profile():
    return {
        "name": "Priyanshu Raj",
        "headline": "Software Engineer Aspirant · Full-Stack Development · DSA · AI & Cloud",
        "location": "India",
        "education": "Computer Science & Design Undergraduate · 2023–2027",
        "summary": "I’m a Computer Science and Design undergraduate (2023–2027) focused on software engineering, full-stack development, backend systems, and AI-powered applications. I build with the MERN stack, practice DSA in C++, and explore Google Cloud and generative AI.",
        "github": "https://github.com/Priyanshu87571",
        "linkedin": "https://www.linkedin.com/in/priyanshu-raj-162763306/",
        "geeksforgeeks": "https://www.geeksforgeeks.org/profile/priyansh4ipj",
        "email": "priyanshu875717@gmail.com",
        "resume_url": "",
        "problem_solving": "260+ DSA problems solved (GitHub profile; update as needed)"
    }

@app.get("/api/projects", response_model=list[ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    return list(db.scalars(select(Project).order_by(Project.sort_order, Project.id)))

@app.get("/api/skills", response_model=list[SkillOut])
def get_skills(db: Session = Depends(get_db)):
    return list(db.scalars(select(Skill).order_by(Skill.category, Skill.sort_order, Skill.id)))

@app.get("/api/achievements", response_model=list[AchievementOut])
def get_achievements(db: Session = Depends(get_db)):
    return list(db.scalars(select(Achievement).order_by(Achievement.sort_order, Achievement.id)))

# Small in-memory rate limiter. For multi-worker/production deployments, use a shared store such as Redis.
_contact_attempts = defaultdict(deque)
@app.post("/api/contact", status_code=201)
def create_contact(payload: ContactIn, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    attempts = _contact_attempts[ip]
    while attempts and now - attempts[0] > 3600:
        attempts.popleft()
    if len(attempts) >= 5:
        raise HTTPException(status_code=429, detail="Too many messages. Please try again later.")
    attempts.append(now)
    msg = ContactMessage(name=payload.name.strip(), email=str(payload.email).lower(), subject=payload.subject.strip(), message=payload.message.strip())
    db.add(msg)
    db.commit()
    return {"message": "Thanks! Your message has been saved."}

def require_admin(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        if payload.get("sub") != ADMIN_EMAIL or payload.get("role") != "admin":
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please sign in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@app.post("/api/auth/login")
def login(payload: LoginIn):
    if payload.email.lower() != ADMIN_EMAIL or not ADMIN_PASSWORD or ADMIN_PASSWORD == "change-me-now":
        # Never allow the shipped fallback credentials to log in.
        raise HTTPException(status_code=401, detail="Invalid email or password. Configure admin credentials in .env.")
    # The configured password is hashed per process; the environment value is never returned.
    configured_hash = password_hash.hash(ADMIN_PASSWORD)
    if not password_hash.verify(payload.password, configured_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    expiry = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    token = jwt.encode({"sub": ADMIN_EMAIL, "role": "admin", "exp": expiry}, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer", "expires_in": JWT_EXPIRE_MINUTES * 60}

@app.get("/api/admin/messages", response_model=list[MessageOut], dependencies=[Depends(require_admin)])
def admin_messages(db: Session = Depends(get_db)):
    return list(db.scalars(select(ContactMessage).order_by(ContactMessage.created_at.desc())))

@app.delete("/api/admin/messages/{message_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_message(message_id: int, db: Session = Depends(get_db)):
    obj = db.get(ContactMessage, message_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(obj)
    db.commit()
    return None

def admin_create(model, payload, db):
    obj = model(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def admin_update(model, item_id, payload, db):
    obj = db.get(model, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in payload.model_dump().items():
        setattr(obj, key, value)
    db.commit(); db.refresh(obj)
    return obj

def admin_delete(model, item_id, db):
    obj = db.get(model, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(obj); db.commit()
    return None

@app.post("/api/admin/projects", response_model=ProjectOut, status_code=201, dependencies=[Depends(require_admin)])
def create_project(payload: ProjectIn, db: Session = Depends(get_db)): return admin_create(Project, payload, db)
@app.put("/api/admin/projects/{item_id}", response_model=ProjectOut, dependencies=[Depends(require_admin)])
def update_project(item_id: int, payload: ProjectIn, db: Session = Depends(get_db)): return admin_update(Project, item_id, payload, db)
@app.delete("/api/admin/projects/{item_id}", status_code=204, dependencies=[Depends(require_admin)])
def remove_project(item_id: int, db: Session = Depends(get_db)): return admin_delete(Project, item_id, db)

@app.post("/api/admin/skills", response_model=SkillOut, status_code=201, dependencies=[Depends(require_admin)])
def create_skill(payload: SkillIn, db: Session = Depends(get_db)): return admin_create(Skill, payload, db)
@app.put("/api/admin/skills/{item_id}", response_model=SkillOut, dependencies=[Depends(require_admin)])
def update_skill(item_id: int, payload: SkillIn, db: Session = Depends(get_db)): return admin_update(Skill, item_id, payload, db)
@app.delete("/api/admin/skills/{item_id}", status_code=204, dependencies=[Depends(require_admin)])
def remove_skill(item_id: int, db: Session = Depends(get_db)): return admin_delete(Skill, item_id, db)

@app.post("/api/admin/achievements", response_model=AchievementOut, status_code=201, dependencies=[Depends(require_admin)])
def create_achievement(payload: AchievementIn, db: Session = Depends(get_db)): return admin_create(Achievement, payload, db)
@app.put("/api/admin/achievements/{item_id}", response_model=AchievementOut, dependencies=[Depends(require_admin)])
def update_achievement(item_id: int, payload: AchievementIn, db: Session = Depends(get_db)): return admin_update(Achievement, item_id, payload, db)
@app.delete("/api/admin/achievements/{item_id}", status_code=204, dependencies=[Depends(require_admin)])
def remove_achievement(item_id: int, db: Session = Depends(get_db)): return admin_delete(Achievement, item_id, db)
