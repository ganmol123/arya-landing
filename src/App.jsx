import React, { useState, useEffect } from "react";

const AryaVidyaLanding = () => {
  const [formData, setFormData] = useState({ name: "", phone: "", email: "" });
  const [submitted, setSubmitted] = useState(false);
  const [countdown, setCountdown] = useState({
    days: 45,
    hours: 12,
    mins: 30,
    secs: 0,
  });

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => {
        let { days, hours, mins, secs } = prev;
        secs--;
        if (secs < 0) {
          secs = 59;
          mins--;
        }
        if (mins < 0) {
          mins = 59;
          hours--;
        }
        if (hours < 0) {
          hours = 23;
          days--;
        }
        if (days < 0) {
          days = 0;
          hours = 0;
          mins = 0;
          secs = 0;
        }
        return { days, hours, mins, secs };
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  // Owl Logo Component
  const OwlLogo = ({ size = 200, mobileSize = 180 }) => {
    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    
    useEffect(() => {
      const handleResize = () => setIsMobile(window.innerWidth < 768);
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }, []);
    
    const logoSize = isMobile ? mobileSize : size;
    
    return (
    <svg viewBox="0 0 300 280" width={logoSize} height={logoSize * 0.93}>
      <defs>
        <linearGradient id="owlBody" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#8B5CF6" />
          <stop offset="100%" stopColor="#7C3AED" />
        </linearGradient>
        <linearGradient id="owlBelly" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#FDF6E3" />
          <stop offset="100%" stopColor="#F5E6D3" />
        </linearGradient>
      </defs>
      <ellipse cx="150" cy="130" rx="60" ry="70" fill="url(#owlBody)" />
      <polygon points="105,70 95,45 120,65" fill="#8B5CF6" />
      <polygon points="195,70 205,45 180,65" fill="#8B5CF6" />
      <ellipse cx="150" cy="145" rx="40" ry="45" fill="url(#owlBelly)" />
      <circle cx="125" cy="110" r="22" fill="#FDF6E3" />
      <circle cx="175" cy="110" r="22" fill="#FDF6E3" />
      <circle cx="125" cy="110" r="15" fill="#2D3436" className="owl-eye" />
      <circle cx="175" cy="110" r="15" fill="#2D3436" className="owl-eye" />
      <circle cx="120" cy="105" r="5" fill="#FFF" />
      <circle cx="170" cy="105" r="5" fill="#FFF" />
      <polygon points="150,125 140,140 150,150 160,140" fill="#FF9F1C" />
      <polygon points="150,48 100,68 150,88 200,68" fill="#2D3436" />
      <rect x="145" y="40" width="10" height="20" fill="#2D3436" />
      <rect x="140" y="35" width="20" height="8" fill="#2D3436" />
      <line
        x1="200"
        y1="68"
        x2="210"
        y2="90"
        stroke="#FFD93D"
        strokeWidth="2"
      />
      <circle cx="210" cy="95" r="6" fill="#FFD93D" />
      <ellipse cx="95" cy="150" rx="20" ry="35" fill="#7C3AED" />
      <ellipse cx="205" cy="150" rx="20" ry="35" fill="#7C3AED" />
      <rect x="115" y="165" width="70" height="10" rx="2" fill="#FF6B6B" />
      <rect x="117" y="167" width="66" height="6" fill="#FDF6E3" />
      <ellipse cx="130" cy="198" rx="15" ry="6" fill="#FF9F1C" />
      <ellipse cx="170" cy="198" rx="15" ry="6" fill="#FF9F1C" />
      <text
        x="150"
        y="235"
        textAnchor="middle"
        fontFamily="'Baloo 2', cursive"
        fontSize="26"
        fontWeight="bold"
        fill="#7C3AED"
      >
        Arya Vidya
      </text>
      <text
        x="150"
        y="262"
        textAnchor="middle"
        fontFamily="'Quicksand', sans-serif"
        fontSize="14"
        fill="#8B5CF6"
        fontWeight="600"
        letterSpacing="3"
      >
        PLAY SCHOOL
      </text>
    </svg>
    );
  };

  const activities = [
    {
      emoji: "🎨",
      title: "Art & Craft",
      desc: "Finger painting, clay modeling & creative expression",
      color: "#FF6B6B",
      bg: "#FEE2E2",
    },
    {
      emoji: "🎵",
      title: "Music & Dance",
      desc: "Rhymes, songs & joyful movement activities",
      color: "#8B5CF6",
      bg: "#EDE9FE",
    },
    {
      emoji: "📚",
      title: "Story Time",
      desc: "Magical tales that spark imagination",
      color: "#3B82F6",
      bg: "#DBEAFE",
    },
    {
      emoji: "🧩",
      title: "Brain Games",
      desc: "Puzzles & activities for growing minds",
      color: "#F59E0B",
      bg: "#FEF3C7",
    },
    {
      emoji: "🌱",
      title: "Nature Play",
      desc: "Garden exploration & outdoor adventures",
      color: "#10B981",
      bg: "#D1FAE5",
    },
    {
      emoji: "🤝",
      title: "Social Skills",
      desc: "Learning to share, care & make friends",
      color: "#EC4899",
      bg: "#FCE7F3",
    },
  ];

  const features = [
    { icon: "🏰", text: "Safe & Colorful Campus" },
    { icon: "👩‍🏫", text: "Trained & Caring Teachers" },
    { icon: "🍎", text: "Healthy Snacks Provided" },
    { icon: "📹", text: "CCTV Monitored Premises" },
    { icon: "🚐", text: "Transport Facility" },
    { icon: "👨‍👩‍👧", text: "Regular Parent Updates" },
  ];

  const testimonials = [
    {
      name: "Priya M.",
      text: "Can't wait for this school to open! The curriculum looks amazing.",
      avatar: "👩",
    },
    {
      name: "Rahul S.",
      text: "Finally a play school that focuses on holistic development!",
      avatar: "👨",
    },
    {
      name: "Anita K.",
      text: "Love the concept! My daughter is so excited to join.",
      avatar: "👩‍🦱",
    },
  ];

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#FFF9E6",
        overflow: "hidden",
        position: "relative",
      }}
    >
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Quicksand:wght@400;500;600;700&family=Fredoka+One&display=swap');
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        @keyframes float { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-20px) rotate(5deg); } }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
        @keyframes wiggle { 0%, 100% { transform: rotate(-3deg); } 50% { transform: rotate(3deg); } }
        @keyframes popIn { 0% { transform: scale(0); opacity: 0; } 50% { transform: scale(1.1); } 100% { transform: scale(1); opacity: 1; } }
        @keyframes slideUp { 0% { transform: translateY(40px); opacity: 0; } 100% { transform: translateY(0); opacity: 1; } }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.08); } }
        @keyframes sparkle { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
        @keyframes wave { 0%, 60%, 100% { transform: rotate(0deg); } 10%, 30% { transform: rotate(14deg); } 20% { transform: rotate(-8deg); } 40% { transform: rotate(14deg); } 50% { transform: rotate(-4deg); } }
        @keyframes rainbow { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes blob { 0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; } 50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; } }
        
        .floating-emoji { position: absolute; animation: float 4s ease-in-out infinite; pointer-events: none; z-index: 1; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.15)); }
        .section-title { font-family: 'Fredoka One', cursive; font-size: clamp(1.8rem, 5vw, 2.8rem); text-align: center; margin-bottom: 15px; }
        .section-subtitle { font-family: 'Quicksand', sans-serif; font-size: clamp(1rem, 2.5vw, 1.2rem); text-align: center; color: #6B7280; font-weight: 600; margin-bottom: 40px; }
        
        .hero-blob {
          position: absolute;
          width: min(400px, 80vw);
          height: min(400px, 80vw);
          background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.15));
          animation: blob 8s ease-in-out infinite;
          filter: blur(40px);
        }
        
        @media (max-width: 768px) {
          .hero-blob {
            width: min(300px, 90vw);
            height: min(300px, 90vw);
          }
        }
        
        .countdown-box {
          background: white;
          border-radius: 20px;
          padding: clamp(12px, 3vw, 15px) clamp(18px, 4vw, 25px);
          text-align: center;
          box-shadow: 0 10px 30px rgba(139, 92, 246, 0.15);
          border: 3px solid #E9D5FF;
          min-width: min(90px, 20vw);
        }
        
        .countdown-number {
          font-family: 'Fredoka One', cursive;
          font-size: clamp(2rem, 5vw, 3rem);
          background: linear-gradient(135deg, #8B5CF6, #EC4899);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        
        .countdown-label {
          font-family: 'Quicksand', sans-serif;
          font-size: 14px;
          color: #9CA3AF;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 1px;
        }
        
        .activity-card {
          background: white;
          border-radius: 24px;
          padding: 30px 25px;
          text-align: center;
          box-shadow: 0 8px 30px rgba(0,0,0,0.08);
          transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
          border: 3px solid transparent;
          position: relative;
          overflow: hidden;
        }
        
        .activity-card:hover {
          transform: translateY(-12px) scale(1.02);
          box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        }
        
        .activity-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 6px;
        }
        
        .feature-pill {
          display: flex;
          align-items: center;
          gap: 12px;
          background: white;
          padding: 16px 24px;
          border-radius: 50px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.08);
          font-family: 'Quicksand', sans-serif;
          font-weight: 700;
          font-size: 15px;
          color: #4B5563;
          transition: all 0.3s ease;
          border: 2px solid #F3F4F6;
        }
        
        .feature-pill:hover {
          transform: scale(1.05);
          border-color: #E9D5FF;
          box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2);
        }
        
        .testimonial-card {
          background: white;
          border-radius: 24px;
          padding: 30px;
          box-shadow: 0 8px 30px rgba(0,0,0,0.08);
          position: relative;
          border: 3px solid #F3F4F6;
        }
        
        .testimonial-card::before {
          content: '"';
          position: absolute;
          top: 15px;
          left: 25px;
          font-size: 60px;
          font-family: Georgia, serif;
          color: #E9D5FF;
          line-height: 1;
        }
        
        .info-card {
          background: white;
          border-radius: 30px;
          padding: clamp(25px, 6vw, 40px);
          box-shadow: 0 20px 60px rgba(139, 92, 246, 0.15);
          border: 4px solid #E9D5FF;
          position: relative;
          overflow: hidden;
        }
        
        @media (max-width: 768px) {
          .info-card {
            border-radius: 24px;
            padding: clamp(20px, 5vw, 30px);
          }
        }
        
        .info-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 8px;
          background: linear-gradient(90deg, #FF6B6B, #FFD93D, #6BCB77, #4D96FF, #9B59B6);
        }
        
        .form-input {
          width: 100%;
          padding: clamp(14px, 3vw, 18px) clamp(18px, 4vw, 24px);
          border: 3px solid #E9D5FF;
          border-radius: 16px;
          font-size: clamp(16px, 4vw, 18px);
          font-family: 'Quicksand', sans-serif;
          font-weight: 600;
          transition: all 0.3s ease;
          background: #FEFCFF;
          color: #5B21B6;
        }
        
        .form-input:focus {
          outline: none;
          border-color: #8B5CF6;
          box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
        }
        
        .form-input::placeholder { color: #C4B5FD; }
        
        .submit-btn {
          width: 100%;
          padding: clamp(16px, 4vw, 20px) clamp(30px, 6vw, 40px);
          background: linear-gradient(135deg, #8B5CF6, #7C3AED, #6D28D9);
          color: white;
          border: none;
          border-radius: 16px;
          font-size: clamp(18px, 4vw, 20px);
          font-family: 'Baloo 2', cursive;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.3s ease;
          box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
          min-height: 48px;
        }
        
        .submit-btn:hover {
          transform: translateY(-4px);
          box-shadow: 0 15px 35px rgba(139, 92, 246, 0.5);
        }
        
        .contact-item {
          display: flex;
          align-items: center;
          gap: 15px;
          padding: 18px 20px;
          background: linear-gradient(135deg, #FDF4FF, #FAF5FF);
          border-radius: 16px;
          transition: all 0.3s ease;
        }
        
        .contact-item:hover {
          transform: translateX(8px);
          box-shadow: 0 4px 15px rgba(139, 92, 246, 0.15);
        }
        
        .age-badge {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          background: linear-gradient(135deg, #FEF3C7, #FDE68A);
          padding: 12px 24px;
          border-radius: 50px;
          font-family: 'Baloo 2', cursive;
          font-size: 18px;
          color: #92400E;
          border: 3px dashed #F59E0B;
        }
        
        .scroll-indicator {
          position: absolute;
          bottom: 30px;
          left: 50%;
          transform: translateX(-50%);
          animation: bounce 2s infinite;
        }
      `}</style>

      {/* Floating Background Blobs */}
      <div className="hero-blob" style={{ top: "-100px", left: "-100px" }} />
      <div
        className="hero-blob"
        style={{ top: "50%", right: "-150px", animationDelay: "4s" }}
      />
      <div
        className="hero-blob"
        style={{ bottom: "-100px", left: "30%", animationDelay: "2s" }}
      />

      {/* Floating Emojis - More of them! */}
      {[
        {
          emoji: "🎨",
          left: "3%",
          top: "8%",
          size: "2.5rem",
          delay: 0,
          duration: 4,
        },
        {
          emoji: "🧸",
          left: "95%",
          top: "12%",
          size: "3rem",
          delay: 0.5,
          duration: 5,
        },
        {
          emoji: "🎪",
          left: "8%",
          top: "25%",
          size: "2rem",
          delay: 1,
          duration: 4.5,
        },
        {
          emoji: "🌈",
          left: "92%",
          top: "28%",
          size: "2.8rem",
          delay: 1.5,
          duration: 5.5,
        },
        {
          emoji: "⭐",
          left: "5%",
          top: "45%",
          size: "2.2rem",
          delay: 2,
          duration: 4,
        },
        {
          emoji: "🎈",
          left: "97%",
          top: "42%",
          size: "2.5rem",
          delay: 0.3,
          duration: 5,
        },
        {
          emoji: "🚀",
          left: "4%",
          top: "65%",
          size: "2rem",
          delay: 1.2,
          duration: 4.8,
        },
        {
          emoji: "🎵",
          left: "94%",
          top: "58%",
          size: "2.3rem",
          delay: 0.8,
          duration: 5.2,
        },
        {
          emoji: "📚",
          left: "6%",
          top: "82%",
          size: "2.4rem",
          delay: 1.8,
          duration: 4.3,
        },
        {
          emoji: "✏️",
          left: "96%",
          top: "75%",
          size: "2rem",
          delay: 2.2,
          duration: 5.1,
        },
        {
          emoji: "🎭",
          left: "12%",
          top: "92%",
          size: "2.2rem",
          delay: 0.6,
          duration: 4.7,
        },
        {
          emoji: "🌟",
          left: "88%",
          top: "88%",
          size: "2.6rem",
          delay: 1.4,
          duration: 5.3,
        },
        {
          emoji: "🦋",
          left: "15%",
          top: "15%",
          size: "2rem",
          delay: 2.5,
          duration: 4.2,
        },
        {
          emoji: "🌸",
          left: "85%",
          top: "5%",
          size: "2.3rem",
          delay: 0.9,
          duration: 5.4,
        },
      ].map((item, i) => (
        <div
          key={i}
          className="floating-emoji"
          style={{
            left: item.left,
            top: item.top,
            fontSize: item.size,
            animationDelay: `${item.delay}s`,
            animationDuration: `${item.duration}s`,
          }}
        >
          {item.emoji}
        </div>
      ))}

      {/* ========== HERO SECTION ========== */}
      <section
        style={{
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "clamp(20px, 5vw, 40px) 20px",
          position: "relative",
          background:
            "linear-gradient(180deg, #FFF9E6 0%, #FFE4F3 50%, #E4F4FF 100%)",
        }}
      >
        {/* Decorative top banner */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: "8px",
            background:
              "linear-gradient(90deg, #FF6B6B, #FFD93D, #6BCB77, #4D96FF, #9B59B6, #FF6B6B)",
            backgroundSize: "200% 100%",
            animation: "rainbow 4s linear infinite",
          }}
        />

        {/* Logo */}
        <div
          style={{
            animation:
              "popIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards",
          }}
        >
          <OwlLogo size={260} mobileSize={180} />
        </div>

        {/* Coming Soon Text */}
        <div
          style={{
            marginTop: 10,
            display: "inline-block",
            background:
              "linear-gradient(135deg, #FF6B6B, #FFD93D, #6BCB77, #4D96FF, #9B59B6)",
            backgroundSize: "200% 200%",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            fontSize: "clamp(2.5rem, 8vw, 5rem)",
            fontFamily: "'Fredoka One', cursive",
            animation:
              "rainbow 4s linear infinite, wiggle 2s ease-in-out infinite",
            textAlign: "center",
          }}
        >
          🎉 Coming Soon! 🎉
        </div>

        <p
          style={{
            fontFamily: "'Quicksand', sans-serif",
            fontSize: "clamp(1.1rem, 3vw, 1.5rem)",
            color: "#6B7280",
            marginTop: 10,
            fontWeight: 600,
            textAlign: "center",
          }}
        >
          A magical place where little minds grow BIG!{" "}
          <span
            style={{ display: "inline-block", animation: "wave 2s infinite" }}
          >
            👋
          </span>
        </p>

        {/* Age Badge */}
        <div className="age-badge" style={{ marginTop: 25 }}>
          👶 Ages 2 to 6 Years
        </div>

        {/* Countdown Timer */}
        <div
          style={{
            display: "flex",
            gap: "clamp(10px, 3vw, 25px)",
            marginTop: 40,
            flexWrap: "wrap",
            justifyContent: "center",
          }}
        >
          {[
            { value: countdown.days, label: "Days" },
            { value: countdown.hours, label: "Hours" },
            { value: countdown.mins, label: "Mins" },
            { value: countdown.secs, label: "Secs" },
          ].map((item, i) => (
            <div key={i} className="countdown-box">
              <div className="countdown-number">
                {String(item.value).padStart(2, "0")}
              </div>
              <div className="countdown-label">{item.label}</div>
            </div>
          ))}
        </div>

        {/* Scroll indicator */}
        <div
          className="scroll-indicator"
          style={{ fontSize: "2rem", color: "#C4B5FD" }}
        >
          ↓
        </div>
      </section>

      {/* ========== ACTIVITIES SECTION ========== */}
      <section
        style={{
          padding: "clamp(40px, 10vw, 80px) 20px",
          background: "linear-gradient(180deg, #E4F4FF 0%, #FFFFFF 100%)",
          position: "relative",
        }}
      >
        <div style={{ maxWidth: 1200, margin: "0 auto" }}>
          <div className="section-title" style={{ color: "#7C3AED" }}>
            🌟 What We'll Learn Together 🌟
          </div>
          <div className="section-subtitle">
            Play-based learning that sparks curiosity and builds confidence
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(min(280px, 100%), 1fr))",
              gap: 25,
            }}
          >
            {activities.map((activity, i) => (
              <div
                key={i}
                className="activity-card"
                style={{
                  animationDelay: `${i * 0.1}s`,
                  borderColor: activity.bg,
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                    right: 0,
                    height: 6,
                    background: activity.color,
                    borderRadius: "24px 24px 0 0",
                  }}
                />
                <div
                  style={{
                    width: 80,
                    height: 80,
                    background: activity.bg,
                    borderRadius: "50%",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "2.5rem",
                    margin: "0 auto 20px",
                  }}
                >
                  {activity.emoji}
                </div>
                <h3
                  style={{
                    fontFamily: "'Baloo 2', cursive",
                    fontSize: "clamp(18px, 4vw, 22px)",
                    color: activity.color,
                    marginBottom: 10,
                  }}
                >
                  {activity.title}
                </h3>
                <p
                  style={{
                    fontFamily: "'Quicksand', sans-serif",
                    fontSize: "clamp(14px, 3vw, 15px)",
                    color: "#6B7280",
                    fontWeight: 500,
                    lineHeight: 1.6,
                  }}
                >
                  {activity.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ========== WHY CHOOSE US SECTION ========== */}
      <section
        style={{
          padding: "clamp(40px, 10vw, 80px) 20px",
          background:
            "linear-gradient(135deg, #FDF4FF 0%, #FAF5FF 50%, #F5F3FF 100%)",
          position: "relative",
        }}
      >
        {/* Decorative shapes */}
        <div
          style={{
            position: "absolute",
            top: 40,
            left: 40,
            width: 100,
            height: 100,
            background: "linear-gradient(135deg, #FFD93D, #FF9F1C)",
            borderRadius: "30% 70% 70% 30% / 30% 30% 70% 70%",
            opacity: 0.3,
            animation: "blob 6s ease-in-out infinite",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: 40,
            right: 40,
            width: 120,
            height: 120,
            background: "linear-gradient(135deg, #6BCB77, #4DAA57)",
            borderRadius: "60% 40% 30% 70% / 60% 30% 70% 40%",
            opacity: 0.3,
            animation: "blob 8s ease-in-out infinite reverse",
          }}
        />

        <div
          style={{
            maxWidth: 1000,
            margin: "0 auto",
            position: "relative",
            zIndex: 2,
          }}
        >
          <div className="section-title" style={{ color: "#EC4899" }}>
            💖 Why Parents Love Us 💖
          </div>
          <div className="section-subtitle">
            Everything your little one needs to thrive
          </div>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: 20,
              justifyContent: "center",
            }}
          >
            {features.map((feature, i) => (
              <div key={i} className="feature-pill">
                <span style={{ fontSize: 28 }}>{feature.icon}</span>
                {feature.text}
              </div>
            ))}
          </div>

          {/* Mini testimonials */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(min(280px, 100%), 1fr))",
              gap: 25,
              marginTop: 50,
            }}
          >
            {testimonials.map((t, i) => (
              <div key={i} className="testimonial-card">
                <p
                  style={{
                    fontFamily: "'Quicksand', sans-serif",
                    fontSize: 16,
                    color: "#4B5563",
                    fontWeight: 500,
                    lineHeight: 1.7,
                    marginBottom: 20,
                    paddingTop: 20,
                  }}
                >
                  {t.text}
                </p>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 36 }}>{t.avatar}</span>
                  <span
                    style={{
                      fontFamily: "'Baloo 2', cursive",
                      fontSize: 16,
                      color: "#7C3AED",
                    }}
                  >
                    {t.name}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ========== CONTACT & FORM SECTION ========== */}
      <section
        style={{
          padding: "clamp(40px, 10vw, 80px) 20px",
          background: "linear-gradient(180deg, #F5F3FF 0%, #FFF9E6 100%)",
        }}
      >
        <div style={{ maxWidth: 1100, margin: "0 auto" }}>
          <div className="section-title" style={{ color: "#7C3AED" }}>
            📬 Get In Touch 📬
          </div>
          <div className="section-subtitle">
            Register your interest and be the first to know when we open!
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(min(280px, 100%), 1fr))",
              gap: "clamp(25px, 5vw, 40px)",
            }}
          >
            {/* Contact Info */}
            <div className="info-card">
              <h3
                style={{
                  fontFamily: "'Baloo 2', cursive",
                  fontSize: 26,
                  color: "#7C3AED",
                  marginBottom: 25,
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                }}
              >
                <span style={{ fontSize: 32 }}>📍</span> Find Us Here!
              </h3>

              <div
                style={{ display: "flex", flexDirection: "column", gap: 15 }}
              >
                <div className="contact-item">
                  <div
                    style={{
                      width: 50,
                      height: 50,
                      background: "linear-gradient(135deg, #FEE2E2, #FECACA)",
                      borderRadius: 15,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 24,
                    }}
                  >
                    🏠
                  </div>
                  <div>
                    <div
                      style={{
                        fontFamily: "'Quicksand', sans-serif",
                        fontWeight: 700,
                        color: "#7C3AED",
                        fontSize: 13,
                      }}
                    >
                      ADDRESS
                    </div>
                    <div
                      style={{
                        fontFamily: "'Quicksand', sans-serif",
                        fontWeight: 600,
                        color: "#4B5563",
                        fontSize: 15,
                      }}
                    >
                      42, Rainbow Lane, Sunshine Nagar
                      <br />
                      Near Happy Park, New Delhi - 110001
                    </div>
                  </div>
                </div>

                <div className="contact-item">
                  <div
                    style={{
                      width: 50,
                      height: 50,
                      background: "linear-gradient(135deg, #D1FAE5, #A7F3D0)",
                      borderRadius: 15,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 24,
                    }}
                  >
                    📞
                  </div>
                  <div>
                    <div
                      style={{
                        fontFamily: "'Quicksand', sans-serif",
                        fontWeight: 700,
                        color: "#7C3AED",
                        fontSize: 13,
                      }}
                    >
                      PHONE
                    </div>
                    <div
                      style={{
                        fontFamily: "'Quicksand', sans-serif",
                        fontWeight: 600,
                        color: "#4B5563",
                        fontSize: 15,
                      }}
                    >
                      +91 98765 43210
                    </div>
                  </div>
                </div>

                <div className="contact-item">
                  <div
                    style={{
                      width: 50,
                      height: 50,
                      background: "linear-gradient(135deg, #DBEAFE, #BFDBFE)",
                      borderRadius: 15,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 24,
                    }}
                  >
                    ✉️
                  </div>
                  <div>
                    <div
                      style={{
                        fontFamily: "'Quicksand', sans-serif",
                        fontWeight: 700,
                        color: "#7C3AED",
                        fontSize: 13,
                      }}
                    >
                      EMAIL
                    </div>
                    <div
                      style={{
                        fontFamily: "'Quicksand', sans-serif",
                        fontWeight: 600,
                        color: "#4B5563",
                        fontSize: 15,
                      }}
                    >
                      hello@aryavidya.play
                    </div>
                  </div>
                </div>
              </div>

              {/* Map placeholder */}
              <div
                style={{
                  marginTop: 25,
                  height: 160,
                  background: "linear-gradient(135deg, #E0E7FF, #C7D2FE)",
                  borderRadius: 20,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexDirection: "column",
                  gap: 10,
                  border: "3px dashed #A5B4FC",
                }}
              >
                <span style={{ fontSize: 40 }}>🗺️</span>
                <span
                  style={{
                    fontFamily: "'Quicksand', sans-serif",
                    fontWeight: 700,
                    color: "#6366F1",
                  }}
                >
                  Map Coming Soon!
                </span>
              </div>
            </div>

            {/* Form */}
            <div className="info-card">
              <h3
                style={{
                  fontFamily: "'Baloo 2', cursive",
                  fontSize: 26,
                  color: "#7C3AED",
                  marginBottom: 10,
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                }}
              >
                <span style={{ fontSize: 32 }}>💌</span> Register Interest
              </h3>
              <p
                style={{
                  fontFamily: "'Quicksand', sans-serif",
                  fontSize: 15,
                  color: "#6B7280",
                  marginBottom: 25,
                  fontWeight: 500,
                }}
              >
                Be the first to know when admissions open!
              </p>

              {!submitted ? (
                <form
                  onSubmit={handleSubmit}
                  style={{ display: "flex", flexDirection: "column", gap: 18 }}
                >
                  <div>
                    <label
                      style={{
                        display: "block",
                        fontFamily: "'Baloo 2', cursive",
                        fontSize: 15,
                        color: "#7C3AED",
                        marginBottom: 8,
                      }}
                    >
                      👶 Parent's Name
                    </label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter your name"
                      value={formData.name}
                      onChange={(e) =>
                        setFormData({ ...formData, name: e.target.value })
                      }
                      required
                    />
                  </div>

                  <div>
                    <label
                      style={{
                        display: "block",
                        fontFamily: "'Baloo 2', cursive",
                        fontSize: 15,
                        color: "#7C3AED",
                        marginBottom: 8,
                      }}
                    >
                      📱 Phone Number
                    </label>
                    <input
                      type="tel"
                      className="form-input"
                      placeholder="Enter your phone number"
                      value={formData.phone}
                      onChange={(e) =>
                        setFormData({ ...formData, phone: e.target.value })
                      }
                      required
                    />
                  </div>

                  <div>
                    <label
                      style={{
                        display: "block",
                        fontFamily: "'Baloo 2', cursive",
                        fontSize: 15,
                        color: "#7C3AED",
                        marginBottom: 8,
                      }}
                    >
                      ✉️ Email Address
                    </label>
                    <input
                      type="email"
                      className="form-input"
                      placeholder="Enter your email"
                      value={formData.email}
                      onChange={(e) =>
                        setFormData({ ...formData, email: e.target.value })
                      }
                      required
                    />
                  </div>

                  <button
                    type="submit"
                    className="submit-btn"
                    style={{ marginTop: 10 }}
                  >
                    🚀 Count Me In!
                  </button>
                </form>
              ) : (
                <div
                  style={{
                    textAlign: "center",
                    padding: "30px 20px",
                    animation:
                      "popIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards",
                  }}
                >
                  <div style={{ fontSize: 70, marginBottom: 15 }}>🎊</div>
                  <h4
                    style={{
                      fontFamily: "'Baloo 2', cursive",
                      fontSize: 24,
                      color: "#059669",
                      marginBottom: 10,
                    }}
                  >
                    Yay! You're on the list!
                  </h4>
                  <p
                    style={{
                      fontFamily: "'Quicksand', sans-serif",
                      fontSize: 15,
                      color: "#6B7280",
                      fontWeight: 500,
                    }}
                  >
                    We'll reach out soon with exciting updates! 🌟
                  </p>
                  <div
                    style={{
                      marginTop: 20,
                      display: "flex",
                      justifyContent: "center",
                      gap: 10,
                      fontSize: 28,
                    }}
                  >
                    {["⭐", "🌟", "✨", "💫", "⭐"].map((s, i) => (
                      <span
                        key={i}
                        style={{
                          animation: `sparkle 1.5s ease-in-out infinite`,
                          animationDelay: `${i * 0.2}s`,
                        }}
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ========== FOOTER ========== */}
      <footer
        style={{
          padding: "clamp(30px, 6vw, 50px) 20px clamp(20px, 4vw, 30px)",
          background: "linear-gradient(135deg, #7C3AED, #8B5CF6)",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Decorative circles */}
        <div
          style={{
            position: "absolute",
            top: -50,
            left: -50,
            width: 150,
            height: 150,
            background: "rgba(255,255,255,0.1)",
            borderRadius: "50%",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: -30,
            right: -30,
            width: 100,
            height: 100,
            background: "rgba(255,255,255,0.1)",
            borderRadius: "50%",
          }}
        />

        <div
          style={{
            maxWidth: 800,
            margin: "0 auto",
            textAlign: "center",
            position: "relative",
            zIndex: 2,
          }}
        >
          <div style={{ marginBottom: 25 }}>
            <OwlLogo size={100} />
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: 20,
              marginBottom: 25,
              flexWrap: "wrap",
            }}
          >
            {["🎨", "🎪", "🎭", "🎵", "📚", "🧸", "🌈", "⭐"].map(
              (emoji, i) => (
                <span
                  key={i}
                  style={{
                    fontSize: 28,
                    animation: `float ${3 + i * 0.3}s ease-in-out infinite`,
                    animationDelay: `${i * 0.2}s`,
                  }}
                >
                  {emoji}
                </span>
              ),
            )}
          </div>

          <p
            style={{
              fontFamily: "'Quicksand', sans-serif",
              fontSize: 16,
              color: "rgba(255,255,255,0.9)",
              fontWeight: 600,
              marginBottom: 10,
            }}
          >
            © 2025 Arya Vidya Play School • Where Every Child Shines! ✨
          </p>
          <p
            style={{
              fontFamily: "'Quicksand', sans-serif",
              fontSize: 14,
              color: "rgba(255,255,255,0.6)",
            }}
          >
            Made with 💜 for little learners
          </p>
        </div>

        {/* Wave decoration */}
        <svg
          viewBox="0 0 1440 100"
          style={{ position: "absolute", top: 0, left: 0, right: 0 }}
        >
          <path
            fill="#FFF9E6"
            d="M0,64L60,58.7C120,53,240,43,360,48C480,53,600,75,720,80C840,85,960,75,1080,64C1200,53,1320,43,1380,37.3L1440,32L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z"
          />
        </svg>
      </footer>
    </div>
  );
};

export default AryaVidyaLanding;
