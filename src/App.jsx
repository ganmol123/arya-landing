import React, { useState } from "react";

/* ------------------------------------------------------------------ *
 * BRAND — every colour below is lifted from the locked "Tree of
 * Learning" logo. Do not introduce colours from outside this palette.
 * ------------------------------------------------------------------ */
const C = {
  green: "#4DAA57", // wordmark green (primary)
  greenMid: "#6BCB77", // foliage
  greenLite: "#8FE09A", // highlight foliage
  greenPale: "#F4FBF4", // panel background
  greenSoft: "#DFF3E3", // soft fill
  red: "#FF6B6B", // left child's shirt
  yellow: "#FFD93D",
  blue: "#4D96FF", // right child's shirt
  purple: "#9B59B6",
  orange: "#FF9F1C",
  pink: "#FF6B9D",
  ink: "#2D3436",
  grey: "#6B7280",
};

const SCHOOL = {
  name: "Arya Vidya Play School",
  address: "Near Power Sub Station, Hocher \u2013 834006",
  phones: ["+91 95766 74230", "+91 95700 90086"],
  ages: "Ages 2\u20136 Years",
  tagline: "Where Every Child Shines!",
};

/* WhatsApp click-to-chat. wa.me wants country code + number, digits only
   (no "+", no spaces). This is the first school line: +91 95766 74230.
   To use the other number instead, swap the digits below. */
const WHATSAPP_NUMBER = "919576674230";
const WHATSAPP_MSG = "Hi! I'd like to know more about admissions at Arya Vidya Play School.";
const waLink = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(WHATSAPP_MSG)}`;

/* ------------------------------------------------------------------ *
 * LOGO — locked "Tree of Learning" master artwork.
 * Geometry is verbatim from the approved SVG. Do not edit.
 * withText=false renders the mark alone (no wordmark).
 * ------------------------------------------------------------------ */
const TreeLogo = ({ size = 200, withText = true }) => (
  <svg
    viewBox={withText ? "0 0 300 300" : "45 25 210 215"}
    width={size}
    height={withText ? size : size * 1.02}
    role="img"
    aria-label={SCHOOL.name}
  >
    <defs>
      <linearGradient id="treeTop" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stopColor="#6BCB77" />
        <stop offset="100%" stopColor="#4DAA57" />
      </linearGradient>
      <linearGradient id="trunk" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stopColor="#8B5A2B" />
        <stop offset="100%" stopColor="#A0522D" />
      </linearGradient>
    </defs>

    {/* trunk */}
    <path d="M140 180 L145 130 L155 130 L160 180 Z" fill="url(#trunk)" />

    {/* foliage */}
    <circle cx="150" cy="85" r="45" fill="url(#treeTop)" />
    <circle cx="115" cy="105" r="32" fill="#5DBB6A" />
    <circle cx="185" cy="105" r="32" fill="#5DBB6A" />
    <circle cx="130" cy="75" r="28" fill="#7ED687" />
    <circle cx="170" cy="75" r="28" fill="#7ED687" />
    <circle cx="150" cy="55" r="22" fill="#8FE09A" />

    {/* fruits */}
    <circle cx="125" cy="70" r="8" fill="#FF6B6B" />
    <circle cx="175" cy="70" r="8" fill="#FFD93D" />
    <circle cx="150" cy="50" r="8" fill="#4D96FF" />
    <circle cx="110" cy="100" r="7" fill="#9B59B6" />
    <circle cx="190" cy="100" r="7" fill="#FF9F1C" />
    <circle cx="140" cy="90" r="6" fill="#FF6B9D" />
    <circle cx="160" cy="90" r="6" fill="#00D9FF" />

    {/* left child */}
    <circle cx="80" cy="175" r="12" fill="#FFEAA7" />
    <circle cx="76" cy="173" r="2" fill="#2D3436" />
    <circle cx="84" cy="173" r="2" fill="#2D3436" />
    <path d="M76 179 Q80 183 84 179" stroke="#2D3436" strokeWidth="1.5" fill="none" />
    <ellipse cx="80" cy="205" rx="12" ry="18" fill="#FF6B6B" />
    <line x1="68" y1="200" x2="60" y2="190" stroke="#FFEAA7" strokeWidth="4" strokeLinecap="round" />
    <line x1="92" y1="200" x2="100" y2="190" stroke="#FFEAA7" strokeWidth="4" strokeLinecap="round" />

    {/* right child */}
    <circle cx="220" cy="175" r="12" fill="#DFB48C" />
    <circle cx="216" cy="173" r="2" fill="#2D3436" />
    <circle cx="224" cy="173" r="2" fill="#2D3436" />
    <path d="M216 179 Q220 183 224 179" stroke="#2D3436" strokeWidth="1.5" fill="none" />
    <ellipse cx="220" cy="205" rx="12" ry="18" fill="#4D96FF" />
    <line x1="208" y1="200" x2="200" y2="190" stroke="#DFB48C" strokeWidth="4" strokeLinecap="round" />
    <line x1="232" y1="200" x2="240" y2="190" stroke="#DFB48C" strokeWidth="4" strokeLinecap="round" />

    {/* ground */}
    <ellipse cx="150" cy="225" rx="100" ry="12" fill="#90EE90" opacity="0.5" />

    {withText && (
      <>
        <text
          x="150"
          y="260"
          textAnchor="middle"
          fontFamily="'Bubblegum Sans', 'Comic Sans MS', cursive"
          fontSize="26"
          fontWeight="bold"
          fill="#4DAA57"
        >
          Arya Vidya
        </text>
        <text
          x="150"
          y="285"
          textAnchor="middle"
          fontFamily="'Poppins', sans-serif"
          fontSize="14"
          fill="#6B7280"
          letterSpacing="2"
        >
          PLAY SCHOOL
        </text>
      </>
    )}
  </svg>
);

/* ------------------------------------------------------------------ *
 * WHATSAPP ICON — official glyph. Always white; it sits on a green button.
 * ------------------------------------------------------------------ */
const WhatsAppIcon = ({ size = 26 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="#fff" aria-hidden="true">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
  </svg>
);

/* ------------------------------------------------------------------ *
 * CONTENT
 * ------------------------------------------------------------------ */
const activities = [
  { emoji: "\u{1F3A8}", title: "Art & Craft", desc: "Finger painting, clay modeling & creative expression", color: C.red, bg: "#FEE2E2" },
  { emoji: "\u{1F3B5}", title: "Music & Dance", desc: "Rhymes, songs & joyful movement activities", color: C.purple, bg: "#F3E8FA" },
  { emoji: "\u{1F4DA}", title: "Story Time", desc: "Magical tales that spark imagination", color: C.blue, bg: "#DBEAFE" },
  { emoji: "\u{1F9E9}", title: "Brain Games", desc: "Puzzles & activities for growing minds", color: C.orange, bg: "#FEF3C7" },
  { emoji: "\u{1F331}", title: "Nature Play", desc: "Garden exploration & outdoor adventures", color: C.green, bg: "#D1FAE5" },
  { emoji: "\u{1F91D}", title: "Social Skills", desc: "Learning to share, care & make friends", color: C.pink, bg: "#FCE7F3" },
];

const features = [
  { icon: "\u{1F3F0}", text: "Safe & Colourful Campus" },
  { icon: "\u{1F469}\u200D\u{1F3EB}", text: "Trained & Caring Teachers" },
  { icon: "\u{1F34E}", text: "Healthy Snacks Provided" },
  { icon: "\u{1F4F9}", text: "CCTV Monitored Premises" },
  { icon: "\u{1F392}", text: "Stationery & Kit Included" },
  { icon: "\u{1F468}\u200D\u{1F469}\u200D\u{1F467}", text: "Regular Parent Updates" },
];

/* These mirror Arya-Vidya-Fee-Structure-A4-2up.pdf exactly.
   If fees change, update BOTH the PDF and this array. */
const fees = [
  { name: "Tuition Fee", tag: "monthly", amount: "1,500", color: C.green },
  { name: "Development Fee", tag: "one-time", amount: "3,000", color: C.orange },
  { name: "Admission Fee", tag: "one-time", amount: "10,500", color: C.blue },
];

const included = [
  { text: "2 Complimentary Uniform Sets", color: C.red },
  { text: "Stationery & School Kit", color: C.blue },
  { text: "First Month\u2019s Tuition Fee", color: C.purple },
];

/* Paste a Formspree form ID here to make the callback form live.
   Free at https://formspree.io -> create form -> copy the ID (e.g. "xvgpabcd").
   While this is empty the submit button stays disabled, so leads are never
   silently swallowed by a form that goes nowhere. */
const FORMSPREE_ID = "mjgnkdya";

const AryaVidyaLanding = () => {
  const [formData, setFormData] = useState({ name: "", phone: "", email: "" });
  const [status, setStatus] = useState("idle"); // idle | sending | done | error

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!FORMSPREE_ID) return;

    setStatus("sending");
    try {
      const res = await fetch("https://formspree.io/f/" + FORMSPREE_ID, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("bad response");
      setStatus("done");
    } catch {
      setStatus("error");
    }
  };

  const scrollTo = (id) => () =>
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });

  return (
    <div style={{ fontFamily: "'Quicksand', 'Segoe UI', sans-serif", overflowX: "hidden", background: "#FFFDF7" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Bubblegum+Sans&family=Baloo+2:wght@600;800&family=Quicksand:wght@500;600;700&family=Poppins:wght@400;500;600&display=swap');

        @keyframes float  { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-20px) rotate(5deg); } }
        @keyframes bounce { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
        @keyframes popIn  { 0% { transform: scale(0); opacity: 0; } 50% { transform: scale(1.1); } 100% { transform: scale(1); opacity: 1; } }
        @keyframes pulse  { 0%,100% { transform: scale(1); } 50% { transform: scale(1.08); } }
        @keyframes wave   { 0%,60%,100% { transform: rotate(0deg); } 10%,30% { transform: rotate(14deg); } 20% { transform: rotate(-8deg); } 40% { transform: rotate(14deg); } 50% { transform: rotate(-4deg); } }
        @keyframes blob   { 0%,100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; } 50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; } }

        .float-emoji { position: absolute; animation: float 6s ease-in-out infinite; opacity: .55; pointer-events: none; }
        .hero-blob   { position: absolute; width: 380px; height: 380px; background: linear-gradient(135deg, ${C.greenLite}, ${C.greenMid}); opacity: .16; animation: blob 12s ease-in-out infinite; pointer-events: none; }

        .section-title { font-family: 'Baloo 2', cursive; font-weight: 800; font-size: clamp(1.9rem, 5vw, 2.9rem); text-align: center; margin-bottom: 12px; }
        .section-sub   { text-align: center; color: ${C.grey}; font-size: 1.05rem; font-weight: 600; margin-bottom: 42px; }

        .card { background: #fff; border-radius: 24px; padding: 28px; box-shadow: 0 8px 26px rgba(45,52,54,.09); transition: transform .3s, box-shadow .3s; }
        .card:hover { transform: translateY(-8px); box-shadow: 0 16px 38px rgba(77,170,87,.20); }

        .btn { font-family: 'Baloo 2', cursive; font-weight: 800; border: none; cursor: pointer; border-radius: 50px; transition: transform .2s, box-shadow .2s; }
        .btn:hover:not(:disabled) { transform: translateY(-3px) scale(1.03); }
        .btn:disabled { opacity: .55; cursor: not-allowed; }
        .btn-primary { background: linear-gradient(120deg, ${C.greenMid}, ${C.green}); color: #fff; box-shadow: 0 8px 22px rgba(77,170,87,.38); }
        .btn-ghost   { background: #fff; color: ${C.green}; border: 3px solid ${C.green}; }

        .field { width: 100%; padding: 15px 20px; border: 3px solid ${C.greenSoft}; border-radius: 16px; font-size: 1rem; font-family: 'Quicksand', sans-serif; font-weight: 600; outline: none; transition: border-color .2s; box-sizing: border-box; }
        .field:focus { border-color: ${C.green}; }

        .fee-row { display: flex; justify-content: space-between; align-items: center; padding: 17px 4px; border-bottom: 1px solid #F0F3F1; }
        .fee-tag { font-size: .74rem; font-weight: 700; margin-left: 10px; }

        .tick { width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; color: #fff; font-size: .78rem; font-weight: 800; flex-shrink: 0; }

        @media (max-width: 768px) {
          .hero-blob { width: 220px; height: 220px; }
          .float-emoji { font-size: 1.6rem !important; }
          .card { padding: 22px; }
        }
      `}</style>

      {/* ===================== HERO ===================== */}
      <section
        style={{
          position: "relative",
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "70px 20px",
          background: `linear-gradient(160deg, #FFFDF7 0%, ${C.greenPale} 100%)`,
          textAlign: "center",
        }}
      >
        <div className="hero-blob" style={{ top: -110, left: -110 }} />
        <div className="hero-blob" style={{ bottom: -110, right: -110, animationDelay: "4s" }} />

        <span className="float-emoji" style={{ top: "12%", left: "8%", fontSize: "2.4rem" }}>{"\u{1F308}"}</span>
        <span className="float-emoji" style={{ top: "20%", right: "10%", fontSize: "2.1rem", animationDelay: "1.5s" }}>{"\u2B50"}</span>
        <span className="float-emoji" style={{ bottom: "18%", left: "12%", fontSize: "2.2rem", animationDelay: "3s" }}>{"\u{1F388}"}</span>
        <span className="float-emoji" style={{ bottom: "24%", right: "9%", fontSize: "2rem", animationDelay: "2s" }}>{"\u{1F9F8}"}</span>

        <div style={{ animation: "popIn .8s ease-out", zIndex: 1 }}>
          <TreeLogo size={260} />
        </div>

        <div
          style={{
            display: "inline-block",
            background: C.yellow,
            color: C.ink,
            fontWeight: 800,
            fontFamily: "'Baloo 2', cursive",
            padding: "9px 26px",
            borderRadius: 50,
            marginTop: 22,
            fontSize: "1rem",
            letterSpacing: ".5px",
            boxShadow: "0 6px 16px rgba(255,217,61,.45)",
            animation: "pulse 2.4s infinite",
            zIndex: 1,
          }}
        >
          {"\u2728"} ADMISSIONS OPEN {"\u2728"}
        </div>

        <h1
          style={{
            fontFamily: "'Baloo 2', cursive",
            fontWeight: 800,
            fontSize: "clamp(2.1rem, 6vw, 3.6rem)",
            color: C.green,
            margin: "22px 0 10px",
            zIndex: 1,
          }}
        >
          Learning that feels like play
        </h1>

        <p style={{ color: C.grey, fontSize: "clamp(1rem, 2.4vw, 1.25rem)", fontWeight: 600, maxWidth: 560, lineHeight: 1.65, zIndex: 1 }}>
          A warm, joyful first classroom for little ones{" "}
          <span style={{ display: "inline-block", animation: "wave 2.5s infinite" }}>{"\u{1F44B}"}</span>
          <br />
          {SCHOOL.ages} {"\u00B7"} Now enrolling in Hocher
        </p>

        <div style={{ display: "flex", gap: 14, flexWrap: "wrap", justifyContent: "center", marginTop: 30, zIndex: 1 }}>
          <button className="btn btn-primary" style={{ padding: "16px 38px", fontSize: "1.1rem" }} onClick={scrollTo("visit")}>
            Book a Visit {"\u{1F392}"}
          </button>
          <button className="btn btn-ghost" style={{ padding: "16px 38px", fontSize: "1.1rem" }} onClick={scrollTo("fees")}>
            See Fees {"\u{1F4B0}"}
          </button>
        </div>
      </section>

      {/* ===================== ACTIVITIES ===================== */}
      <section style={{ padding: "90px 20px", background: "#fff" }}>
        <div style={{ maxWidth: 1180, margin: "0 auto" }}>
          <div className="section-title" style={{ color: C.green }}>
            What We Learn Together {"\u{1F3A8}"}
          </div>
          <p className="section-sub">Every day is a new adventure</p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(285px, 1fr))", gap: 26 }}>
            {activities.map((a, i) => (
              <div className="card" key={i} style={{ borderTop: `6px solid ${a.color}` }}>
                <div
                  style={{
                    width: 66,
                    height: 66,
                    borderRadius: 20,
                    background: a.bg,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 32,
                    marginBottom: 16,
                  }}
                >
                  {a.emoji}
                </div>
                <h3 style={{ fontFamily: "'Baloo 2', cursive", fontWeight: 800, fontSize: "1.4rem", color: a.color, marginBottom: 8 }}>
                  {a.title}
                </h3>
                <p style={{ color: C.grey, fontWeight: 600, lineHeight: 1.6, margin: 0 }}>{a.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===================== FEES ===================== */}
      <section id="fees" style={{ padding: "90px 20px", background: C.greenPale }}>
        <div style={{ maxWidth: 980, margin: "0 auto" }}>
          <div className="section-title" style={{ color: C.green }}>
            Simple, Honest Fees {"\u{1F4B0}"}
          </div>
          <p className="section-sub">No hidden charges. Everything below is included.</p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 26, alignItems: "start" }}>
            <div className="card" style={{ padding: 32 }}>
              {fees.map((f, i) => (
                <div className="fee-row" key={i}>
                  <span style={{ fontWeight: 700, color: C.ink }}>
                    {f.name}
                    <span className="fee-tag" style={{ color: f.color }}>{f.tag}</span>
                  </span>
                  <span style={{ fontWeight: 700, fontSize: "1.15rem", color: C.ink, whiteSpace: "nowrap" }}>
                    {"\u20B9"}{f.amount}/-
                  </span>
                </div>
              ))}

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  background: `linear-gradient(120deg, #EAF8EC, ${C.greenSoft})`,
                  borderLeft: `7px solid ${C.green}`,
                  borderRadius: 12,
                  padding: "18px 20px",
                  marginTop: 20,
                }}
              >
                <span style={{ fontWeight: 800, color: C.ink }}>Total at Admission</span>
                <span style={{ fontFamily: "'Bubblegum Sans', cursive", fontSize: "2rem", color: C.green }}>
                  {"\u20B9"}15,000/-
                </span>
              </div>

              <p style={{ fontSize: ".85rem", color: C.grey, fontWeight: 600, lineHeight: 1.55, marginTop: 16, marginBottom: 0 }}>
                One month{"\u2019"}s tuition fee is included in the admission fee. Thereafter {"\u20B9"}1,500/- is payable monthly.
              </p>
            </div>

            <div className="card" style={{ padding: 32 }}>
              <h3 style={{ fontFamily: "'Bubblegum Sans', cursive", fontSize: "1.6rem", color: C.green, marginTop: 0, marginBottom: 22 }}>
                What{"\u2019"}s Included
              </h3>

              {included.map((it, i) => (
                <div key={i} style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 16 }}>
                  <span className="tick" style={{ background: it.color }}>{"\u2713"}</span>
                  <span style={{ fontWeight: 700, color: C.ink }}>{it.text}</span>
                </div>
              ))}

              <a
                href="/Arya-Vidya-Fee-Structure.pdf"
                download
                className="btn btn-primary"
                style={{ display: "block", textAlign: "center", textDecoration: "none", padding: "15px 20px", marginTop: 26, fontSize: "1rem" }}
              >
                Download Fee Structure {"\u2B07\uFE0F"}
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ===================== WHY PARENTS ===================== */}
      <section style={{ padding: "90px 20px", background: "#fff" }}>
        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          <div className="section-title" style={{ color: C.pink }}>
            Why Parents Choose Us {"\u{1F496}"}
          </div>
          <p className="section-sub">Little things that make a big difference</p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(255px, 1fr))", gap: 16 }}>
            {features.map((f, i) => (
              <div
                key={i}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 14,
                  background: C.greenPale,
                  borderRadius: 16,
                  padding: "18px 20px",
                  fontWeight: 700,
                  color: C.ink,
                }}
              >
                <span style={{ fontSize: 28 }}>{f.icon}</span>
                {f.text}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===================== VISIT / CONTACT ===================== */}
      <section id="visit" style={{ padding: "90px 20px", background: C.greenPale }}>
        <div style={{ maxWidth: 1050, margin: "0 auto" }}>
          <div className="section-title" style={{ color: C.green }}>
            Come Say Hello {"\u{1F44B}"}
          </div>
          <p className="section-sub">We{"\u2019"}d love to show you around</p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 26 }}>
            <div className="card" style={{ padding: 34 }}>
              <h3 style={{ fontFamily: "'Baloo 2', cursive", fontWeight: 800, fontSize: "1.6rem", color: C.green, marginTop: 0 }}>
                {"\u{1F4CD}"} Find Us
              </h3>

              <p style={{ fontWeight: 700, color: C.ink, lineHeight: 1.7, fontSize: "1.05rem" }}>
                {SCHOOL.name}
                <br />
                <span style={{ color: C.grey }}>{SCHOOL.address}</span>
              </p>

              <h3 style={{ fontFamily: "'Baloo 2', cursive", fontWeight: 800, fontSize: "1.6rem", color: C.green, marginTop: 28 }}>
                {"\u{1F4DE}"} Call Us
              </h3>

              {SCHOOL.phones.map((p) => (
                <a
                  key={p}
                  href={"tel:" + p.replace(/\s/g, "")}
                  style={{ display: "block", fontWeight: 700, fontSize: "1.15rem", color: C.green, textDecoration: "none", marginBottom: 8 }}
                >
                  {p}
                </a>
              ))}

              <a
                href={waLink}
                target="_blank"
                rel="noopener noreferrer"
                className="btn"
                style={{ display: "inline-flex", alignItems: "center", gap: 10, background: `linear-gradient(120deg, ${C.greenMid}, ${C.green})`, color: "#fff", padding: "13px 24px", fontSize: "1rem", marginTop: 14, textDecoration: "none" }}
              >
                <WhatsAppIcon size={22} /> Chat on WhatsApp
              </a>

              <div style={{ marginTop: 26, padding: "14px 18px", background: "#fff", border: `2px solid ${C.greenSoft}`, borderRadius: 14, fontWeight: 700, color: C.ink }}>
                {"\u{1F553}"} Monday {"\u2013"} Saturday {"\u00B7"} 9:00 AM {"\u2013"} 1:00 PM
              </div>
            </div>

            <div className="card" style={{ padding: 34 }}>
              <h3 style={{ fontFamily: "'Baloo 2', cursive", fontWeight: 800, fontSize: "1.6rem", color: C.green, marginTop: 0 }}>
                {"\u{1F4DD}"} Request a Callback
              </h3>

              {status === "done" ? (
                <div style={{ textAlign: "center", padding: "40px 10px" }}>
                  <div style={{ fontSize: 56, animation: "bounce 1.4s infinite" }}>{"\u{1F389}"}</div>
                  <p style={{ fontWeight: 800, color: C.green, fontSize: "1.3rem", fontFamily: "'Baloo 2', cursive" }}>Thank you!</p>
                  <p style={{ color: C.grey, fontWeight: 600 }}>We{"\u2019"}ll call you back very soon.</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                  <input
                    className="field"
                    placeholder="Parent's Name"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                  <input
                    className="field"
                    type="tel"
                    placeholder="Phone Number"
                    required
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  />
                  <input
                    className="field"
                    type="email"
                    placeholder="Email (optional)"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  />

                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={!FORMSPREE_ID || status === "sending"}
                    style={{ padding: "16px", fontSize: "1.1rem", marginTop: 4 }}
                  >
                    {status === "sending" ? "Sending\u2026" : "Request Callback \u{1F680}"}
                  </button>

                  {!FORMSPREE_ID && (
                    <p style={{ fontSize: ".8rem", color: C.orange, fontWeight: 700, textAlign: "center", margin: 0 }}>
                      {"\u26A0\uFE0F"} Form not connected yet {"\u2014"} add FORMSPREE_ID in App.jsx
                    </p>
                  )}
                  {status === "error" && (
                    <p style={{ fontSize: ".85rem", color: C.red, fontWeight: 700, textAlign: "center", margin: 0 }}>
                      Something went wrong. Please call us instead.
                    </p>
                  )}
                </form>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ===================== FOOTER ===================== */}
      <footer
        style={{
          background: `linear-gradient(120deg, ${C.greenMid}, ${C.green})`,
          color: "#fff",
          textAlign: "center",
          padding: "50px 20px 34px",
        }}
      >
        <div
          style={{
            background: "#fff",
            width: 96,
            height: 96,
            borderRadius: "50%",
            margin: "0 auto 18px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <TreeLogo size={72} withText={false} />
        </div>

        <div style={{ fontFamily: "'Bubblegum Sans', cursive", fontSize: "1.9rem", marginBottom: 6 }}>Arya Vidya</div>
        <div style={{ letterSpacing: 3, fontSize: ".82rem", fontWeight: 600, opacity: 0.95 }}>PLAY SCHOOL</div>

        <p style={{ fontFamily: "'Baloo 2', cursive", fontWeight: 800, fontSize: "1.25rem", marginTop: 22 }}>{SCHOOL.tagline}</p>

        <p style={{ fontWeight: 600, opacity: 0.95, lineHeight: 1.7, marginTop: 14 }}>
          {SCHOOL.address}
          <br />
          {SCHOOL.phones.join("  \u00B7  ")}
        </p>

        <p style={{ marginTop: 26, fontSize: ".85rem", opacity: 0.8, fontWeight: 600 }}>
          {"\u00A9"} {new Date().getFullYear()} {SCHOOL.name} {"\u00B7"} {SCHOOL.ages}
        </p>
      </footer>

      {/* ===================== FLOATING WHATSAPP ===================== */}
      <a
        href={waLink}
        target="_blank"
        rel="noopener noreferrer"
        aria-label="Chat with us on WhatsApp"
        className="btn"
        style={{
          position: "fixed",
          bottom: 22,
          right: 22,
          width: 62,
          height: 62,
          borderRadius: "50%",
          background: `linear-gradient(120deg, ${C.greenMid}, ${C.green})`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          boxShadow: "0 8px 24px rgba(77,170,87,.5)",
          zIndex: 50,
        }}
      >
        <WhatsAppIcon size={34} />
      </a>
    </div>
  );
};

export default AryaVidyaLanding;
