<!-- SpecForge - Result & Download -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&amp;family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        body {
            background-color: #1a1a1a; /* Level 0 Background */
        }
        .custom-download-card {
            background-color: #f2f2f2; /* Primary Button Style Contrast */
            color: #1a1a1a;
            border-radius: 10px;
            width: 400px;
            height: 140px;
        }
        .canvas-bg {
            background-image: radial-gradient(circle at 2px 2px, #333333 1px, transparent 0);
            background-size: 32px 32px;
        }
    </style>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "primary": "#ffffff",
                    "surface-dim": "#141313",
                    "on-secondary-fixed": "#1b1c1c",
                    "tertiary-fixed-dim": "#cec5c1",
                    "inverse-primary": "#5d5f5f",
                    "secondary": "#c7c6c6",
                    "inverse-on-surface": "#313030",
                    "surface": "#141313",
                    "background": "#1a1a1a",
                    "on-primary-fixed-variant": "#454747",
                    "primary-fixed": "#e2e2e2",
                    "on-surface-variant": "#c4c7c8",
                    "on-error-container": "#ffdad6",
                    "surface-container-high": "#2a2a2a",
                    "secondary-fixed": "#e3e2e2",
                    "surface-container-highest": "#353434",
                    "on-primary-fixed": "#1a1c1c",
                    "on-primary-container": "#636565",
                    "outline-variant": "#444748",
                    "on-tertiary": "#342f2d",
                    "error": "#ffb4ab",
                    "on-error": "#690005",
                    "secondary-container": "#464747",
                    "on-surface": "#e5e2e1",
                    "on-primary": "#2f3131",
                    "surface-bright": "#3a3939",
                    "tertiary-container": "#eae1dd",
                    "surface-tint": "#c6c6c7",
                    "surface-container": "#201f1f",
                    "tertiary-fixed": "#eae1dd",
                    "surface-variant": "#353434",
                    "error-container": "#93000a",
                    "on-secondary": "#303031",
                    "on-tertiary-container": "#696360",
                    "primary-fixed-dim": "#c6c6c7",
                    "secondary-fixed-dim": "#c7c6c6",
                    "on-background": "#e5e2e1",
                    "on-secondary-container": "#b5b5b5",
                    "on-tertiary-fixed": "#1f1b19",
                    "primary-container": "#e2e2e2",
                    "on-secondary-fixed-variant": "#464747",
                    "surface-container-lowest": "#0e0e0e",
                    "on-tertiary-fixed-variant": "#4b4643",
                    "outline": "#333333",
                    "surface-container-low": "#222222",
                    "inverse-surface": "#e5e2e1",
                    "tertiary": "#ffffff"
            },
            "borderRadius": {
                    "DEFAULT": "0.25rem",
                    "lg": "0.5rem",
                    "xl": "0.75rem",
                    "full": "9999px"
            },
            "spacing": {
                    "nav_height": "48px",
                    "xs": "4px",
                    "gutter": "24px",
                    "lg": "24px",
                    "md": "16px",
                    "base": "8px",
                    "sm": "8px",
                    "xl": "32px",
                    "margin_desktop": "40px",
                    "margin_mobile": "16px"
            },
            "fontFamily": {
                    "headline-lg-mobile": ["DM Sans"],
                    "code-md": ["DM Mono"],
                    "display": ["DM Sans"],
                    "headline-lg": ["DM Sans"],
                    "label-md": ["DM Sans"],
                    "body-lg": ["DM Sans"],
                    "headline-md": ["DM Sans"],
                    "body-md": ["DM Sans"]
            },
            "fontSize": {
                    "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                    "code-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                    "display": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                    "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
                    "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "500"}],
                    "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                    "headline-md": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
                    "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}]
            }
          },
        },
      }
    </script>
</head>
<body class="bg-background text-on-surface font-body-md overflow-hidden h-screen canvas-bg">
<!-- TopNavBar Suppression Check: Transactional screen, but requirement specified Nav "Start Over" -->
<nav class="fixed top-0 w-full h-[48px] bg-surface-container-low border-b border-outline flex items-center px-margin_desktop z-50">
<div class="flex-1 flex items-center">
<button class="flex items-center gap-xs text-on-surface-variant hover:text-primary transition-colors duration-200 cursor-pointer active:opacity-80" onclick="window.location.reload()">
<span class="material-symbols-outlined text-[20px]">arrow_back</span>
<span class="font-label-md text-label-md">Start over</span>
</button>
</div>
<div class="flex-none flex items-center gap-xs">
<span class="material-symbols-outlined text-primary font-bold text-[24px]">architecture</span>
<span class="font-headline-md text-headline-md font-bold text-primary tracking-tight">SpecForge</span>
</div>
<div class="flex-1"></div>
</nav>
<!-- Main Content: Centered Content Stack -->
<main class="h-full w-full flex flex-col items-center justify-center p-xl">
<div class="flex flex-col items-center animate-in fade-in duration-700 slide-in-from-bottom-4">
<!-- Logo Lockup Centered Above Card -->
<div class="flex flex-col items-center mb-xl">
<div class="w-16 h-16 bg-surface-container-high border border-outline rounded-xl flex items-center justify-center mb-md">
<span class="material-symbols-outlined text-[32px] text-primary">terminal</span>
</div>
<h1 class="font-headline-lg text-headline-lg text-primary mb-xs">SpecForge</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant">Your spec is ready.</p>
</div>
<!-- Download Card (Primary Focal Element) -->
<button class="custom-download-card flex flex-col items-center justify-center gap-sm group active:scale-[0.98] transition-all duration-200 border border-transparent hover:border-primary/20">
<span class="material-symbols-outlined text-[48px] transition-transform duration-300 group-hover:-translate-y-1">download</span>
<span class="font-body-lg text-body-lg font-bold" style="font-size: 18px;">Download specs.zip</span>
</button>
<!-- Metadata & Verification Below Card -->
<div class="mt-lg flex flex-col items-center gap-xs">
<p class="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest">
                    Contains 5 markdown files • 18 KB
                </p>
<div class="flex items-center gap-xs text-secondary">
<span class="material-symbols-outlined text-[16px]" style="font-variation-settings: 'FILL' 1;">check_circle</span>
<span class="font-label-md text-label-md">Verified generation complete</span>
</div>
</div>
<!-- Decorative Visual: File List Teaser -->
<div class="mt-xl grid grid-cols-5 gap-md opacity-20">
<div class="w-8 h-10 border border-outline rounded-sm flex items-end p-xs">
<div class="w-full h-1 bg-outline-variant"></div>
</div>
<div class="w-8 h-10 border border-outline rounded-sm flex items-end p-xs">
<div class="w-full h-2 bg-outline-variant"></div>
</div>
<div class="w-8 h-10 border border-outline rounded-sm flex items-end p-xs">
<div class="w-full h-1.5 bg-outline-variant"></div>
</div>
<div class="w-8 h-10 border border-outline rounded-sm flex items-end p-xs">
<div class="w-full h-1 bg-outline-variant"></div>
</div>
<div class="w-8 h-10 border border-outline rounded-sm flex items-end p-xs">
<div class="w-full h-2.5 bg-outline-variant"></div>
</div>
</div>
</div>
</main>
<!-- Visual Polish: Subtle Ambient Gradient -->
<div class="fixed inset-0 pointer-events-none overflow-hidden z-0">
<div class="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] bg-primary/5 blur-[120px] rounded-full"></div>
<div class="absolute -bottom-[20%] -right-[10%] w-[50%] h-[50%] bg-primary/5 blur-[120px] rounded-full"></div>
</div>
<script>
        // Micro-interaction for feedback
        document.querySelector('.custom-download-card').addEventListener('click', function() {
            const originalText = this.querySelector('span:last-child').innerText;
            const icon = this.querySelector('.material-symbols-outlined');
            
            this.querySelector('span:last-child').innerText = 'Preparing...';
            icon.innerText = 'sync';
            icon.classList.add('animate-spin');
            
            setTimeout(() => {
                this.querySelector('span:last-child').innerText = 'Downloaded';
                icon.innerText = 'check';
                icon.classList.remove('animate-spin');
                
                setTimeout(() => {
                    this.querySelector('span:last-child').innerText = originalText;
                    icon.innerText = 'download';
                }, 2000);
            }, 1200);
        });
    </script>
</body></html>

<!-- SpecForge - Processing -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>SpecForge — AI Agent Pipeline</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=DM+Mono&amp;family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@100..900&amp;display=swap" rel="stylesheet"/>
<style>
        @keyframes pulse-ring {
            0% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.2); opacity: 0.2; }
            100% { transform: scale(0.8); opacity: 0.5; }
        }
        .pulse-effect {
            animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .shimmer-line {
            background: linear-gradient(90deg, #272727 25%, #333333 50%, #272727 75%);
            background-size: 200% 100%;
            animation: shimmer 2s infinite linear;
        }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 24;
        }
    </style>
<script id="tailwind-config">
        tailwind.config = {
          darkMode: "class",
          theme: {
            extend: {
              "colors": {
                      "primary": "#ffffff",
                      "surface-dim": "#141313",
                      "on-secondary-fixed": "#1b1c1c",
                      "tertiary-fixed-dim": "#cec5c1",
                      "inverse-primary": "#5d5f5f",
                      "secondary": "#c7c6c6",
                      "inverse-on-surface": "#313030",
                      "surface": "#141313",
                      "background": "#141313",
                      "on-primary-fixed-variant": "#454747",
                      "primary-fixed": "#e2e2e2",
                      "on-surface-variant": "#c4c7c8",
                      "on-error-container": "#ffdad6",
                      "surface-container-high": "#2a2a2a",
                      "secondary-fixed": "#e3e2e2",
                      "surface-container-highest": "#353434",
                      "on-primary-fixed": "#1a1c1c",
                      "on-primary-container": "#636565",
                      "outline-variant": "#444748",
                      "on-tertiary": "#342f2d",
                      "error": "#ffb4ab",
                      "on-error": "#690005",
                      "secondary-container": "#464747",
                      "on-surface": "#e5e2e1",
                      "on-primary": "#2f3131",
                      "surface-bright": "#3a3939",
                      "tertiary-container": "#eae1dd",
                      "surface-tint": "#c6c6c7",
                      "surface-container": "#201f1f",
                      "tertiary-fixed": "#eae1dd",
                      "surface-variant": "#353434",
                      "error-container": "#93000a",
                      "on-secondary": "#303031",
                      "on-tertiary-container": "#696360",
                      "primary-fixed-dim": "#c6c6c7",
                      "secondary-fixed-dim": "#c7c6c6",
                      "on-background": "#e5e2e1",
                      "on-secondary-container": "#b5b5b5",
                      "on-tertiary-fixed": "#1f1b19",
                      "primary-container": "#e2e2e2",
                      "on-secondary-fixed-variant": "#464747",
                      "surface-container-lowest": "#0e0e0e",
                      "on-tertiary-fixed-variant": "#4b4643",
                      "outline": "#8e9192",
                      "surface-container-low": "#1c1b1b",
                      "inverse-surface": "#e5e2e1",
                      "tertiary": "#ffffff"
              },
              "borderRadius": {
                      "DEFAULT": "0.25rem",
                      "lg": "0.5rem",
                      "xl": "0.75rem",
                      "full": "9999px"
              },
              "spacing": {
                      "nav_height": "48px",
                      "xs": "4px",
                      "gutter": "24px",
                      "lg": "24px",
                      "md": "16px",
                      "base": "8px",
                      "sm": "8px",
                      "xl": "32px",
                      "margin_desktop": "40px",
                      "margin_mobile": "16px"
              },
              "fontFamily": {
                      "headline-lg-mobile": ["DM Sans"],
                      "code-md": ["DM Mono"],
                      "display": ["DM Sans"],
                      "headline-lg": ["DM Sans"],
                      "label-md": ["DM Sans"],
                      "body-lg": ["DM Sans"],
                      "headline-md": ["DM Sans"],
                      "body-md": ["DM Sans"]
              },
              "fontSize": {
                      "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                      "code-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                      "display": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                      "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
                      "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "500"}],
                      "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                      "headline-md": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
                      "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}]
              }
            },
          },
        }
    </script>
</head>
<body class="bg-background text-on-surface font-body-md overflow-x-hidden antialiased">
<!-- Top Navigation (Shell Implementation) -->
<nav class="fixed top-0 w-full h-[48px] bg-surface-container border-b border-outline-variant flex justify-center items-center px-margin_desktop z-50">
<div class="flex items-center gap-base">
<span class="font-headline-md text-headline-md font-bold text-primary tracking-tight">SpecForge</span>
</div>
</nav>
<!-- Main Content Canvas -->
<main class="pt-[72px] pb-xl max-w-[640px] mx-auto flex flex-col items-center">
<!-- Headers -->
<div class="text-center mb-xl">
<h1 class="font-headline-lg text-[26px] leading-[32px] text-primary mb-xs">Analyzing your requirements</h1>
<p class="font-label-md text-[13px] text-on-surface-variant uppercase tracking-widest">3 agents running in sequence</p>
</div>
<!-- Step Indicator -->
<div class="flex items-center w-full justify-between px-xl mb-xl relative">
<!-- Connector Lines -->
<div class="absolute top-1/2 left-0 w-full h-[1px] bg-outline-variant -z-10 transform -translate-y-1/2"></div>
<!-- Node 1: Parse (Done) -->
<div class="flex flex-col items-center gap-xs bg-background px-base">
<div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-surface-dim">
<span class="material-symbols-outlined text-[18px]" style="font-variation-settings: 'wght' 700;">check</span>
</div>
<span class="font-label-md text-primary">Parse</span>
</div>
<!-- Node 2: Debate (Active) -->
<div class="flex flex-col items-center gap-xs bg-background px-base">
<div class="w-8 h-8 rounded-full border-2 border-dashed border-primary flex items-center justify-center relative">
<div class="w-3 h-3 bg-primary rounded-full"></div>
<div class="absolute inset-0 rounded-full border border-primary pulse-effect"></div>
</div>
<span class="font-label-md text-primary font-bold">Debate</span>
</div>
<!-- Node 3: Write (Pending) -->
<div class="flex flex-col items-center gap-xs bg-background px-base opacity-40">
<div class="w-8 h-8 rounded-full border border-outline flex items-center justify-center">
<div class="w-2 h-2 bg-outline rounded-full"></div>
</div>
<span class="font-label-md text-on-surface-variant">Write</span>
</div>
</div>
<!-- Agent Cards Stack -->
<div class="w-full space-y-md px-margin_mobile md:px-0">
<!-- Card 1: Requirement Parser -->
<div class="bg-surface-container-low border border-outline-variant p-md rounded-lg flex items-center gap-md">
<div class="w-10 h-10 rounded bg-surface-container-highest flex items-center justify-center text-primary">
<span class="material-symbols-outlined">data_object</span>
</div>
<div class="flex-1">
<div class="flex justify-between items-center mb-xs">
<span class="font-headline-md text-body-md text-primary font-bold">Requirement Parser</span>
<span class="font-label-md text-primary text-[10px] bg-surface-container-highest px-sm py-xs rounded">COMPLETED</span>
</div>
<p class="text-on-surface-variant text-body-md">Extracted 14 core entities and 3 system constraints.</p>
</div>
</div>
<!-- Card 2: Strategic Debate (Active) -->
<div class="bg-surface-container border-2 border-dashed border-primary p-md rounded-lg flex items-center gap-md relative overflow-hidden">
<div class="w-10 h-10 rounded bg-primary flex items-center justify-center text-surface-dim">
<span class="material-symbols-outlined">psychology</span>
</div>
<div class="flex-1">
<div class="flex justify-between items-center mb-xs">
<span class="font-headline-md text-body-md text-primary font-bold">Strategic Debate</span>
<div class="flex items-center gap-xs">
<span class="w-1.5 h-1.5 bg-primary rounded-full animate-pulse"></span>
<span class="font-label-md text-primary text-[10px]">PROCESSING</span>
</div>
</div>
<p class="text-primary text-body-md">Evaluating architectural trade-offs between SQL and NoSQL storage...</p>
</div>
</div>
<!-- Card 3: Spec Writer (Pending) -->
<div class="bg-surface-container-low border border-outline-variant p-md rounded-lg flex items-center gap-md opacity-40">
<div class="w-10 h-10 rounded bg-surface-container-highest flex items-center justify-center text-on-surface-variant">
<span class="material-symbols-outlined">edit_note</span>
</div>
<div class="flex-1">
<div class="flex justify-between items-center mb-xs">
<span class="font-headline-md text-body-md text-on-surface-variant font-bold">Spec Writer</span>
<span class="font-label-md text-on-surface-variant text-[10px]">WAITING</span>
</div>
<p class="text-on-surface-variant text-body-md italic">Waiting for debate conclusion...</p>
</div>
</div>
</div>
<!-- Debate Summary Panel -->
<div class="w-full mt-xl px-margin_mobile md:px-0">
<div class="bg-surface-container-lowest border border-dashed border-outline-variant p-lg rounded-xl">
<div class="flex items-center gap-sm mb-md">
<span class="material-symbols-outlined text-primary text-[18px]">forum</span>
<h3 class="font-label-md text-on-surface-variant uppercase tracking-widest">Live Debate Feed</h3>
</div>
<div class="space-y-md">
<div class="space-y-sm">
<div class="h-2 w-[85%] shimmer-line rounded-full opacity-40"></div>
<div class="h-2 w-[95%] shimmer-line rounded-full opacity-60"></div>
<div class="h-2 w-[60%] shimmer-line rounded-full opacity-30"></div>
</div>
<div class="pt-sm border-t border-outline-variant/30 flex justify-between items-center">
<span class="font-code-md text-label-md text-on-surface-variant opacity-50">AGENT_02: hashing_logic_v3...</span>
<span class="font-code-md text-label-md text-primary">72% confidence</span>
</div>
</div>
</div>
</div>
</main>
<!-- Footer Decoration -->
<footer class="fixed bottom-0 w-full py-md flex justify-center pointer-events-none opacity-20">
<div class="text-label-md font-code-md tracking-tighter text-on-surface-variant">
            PIPELINE_STATUS: 0x2A99_ACTIVE_SEQUENCE
        </div>
</footer>
<script>
        // Micro-interaction for shimmering effect variation
        document.querySelectorAll('.shimmer-line').forEach((el, index) => {
            el.style.animationDelay = `${index * 0.4}s`;
        });

        // Simulating Agent activity changes
        const textStates = [
            "Analyzing concurrency requirements...",
            "Validating schema consistency...",
            "Resolving data dependency conflicts...",
            "Comparing performance benchmarks..."
        ];
        let stateIndex = 0;
        const activeText = document.querySelector('.bg-surface-container .text-primary.text-body-md');
        
        if (activeText) {
            setInterval(() => {
                stateIndex = (stateIndex + 1) % textStates.length;
                activeText.style.opacity = '0';
                setTimeout(() => {
                    activeText.textContent = textStates[stateIndex];
                    activeText.style.opacity = '1';
                }, 300);
            }, 3000);
            activeText.style.transition = 'opacity 0.3s ease-in-out';
        }
    </script>
</body></html>

<!-- SpecForge - File Selected -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=DM+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
          darkMode: "class",
          theme: {
            extend: {
              "colors": {
                      "primary": "#ffffff",
                      "surface-dim": "#141313",
                      "on-secondary-fixed": "#1b1c1c",
                      "tertiary-fixed-dim": "#cec5c1",
                      "inverse-primary": "#5d5f5f",
                      "secondary": "#c7c6c6",
                      "inverse-on-surface": "#313030",
                      "surface": "#141313",
                      "background": "#141313",
                      "on-primary-fixed-variant": "#454747",
                      "primary-fixed": "#e2e2e2",
                      "on-surface-variant": "#c4c7c8",
                      "on-error-container": "#ffdad6",
                      "surface-container-high": "#2a2a2a",
                      "secondary-fixed": "#e3e2e2",
                      "surface-container-highest": "#353434",
                      "on-primary-fixed": "#1a1c1c",
                      "on-primary-container": "#636565",
                      "outline-variant": "#444748",
                      "on-tertiary": "#342f2d",
                      "error": "#ffb4ab",
                      "on-error": "#690005",
                      "secondary-container": "#464747",
                      "on-surface": "#e5e2e1",
                      "on-primary": "#2f3131",
                      "surface-bright": "#3a3939",
                      "tertiary-container": "#eae1dd",
                      "surface-tint": "#c6c6c7",
                      "surface-container": "#201f1f",
                      "tertiary-fixed": "#eae1dd",
                      "surface-variant": "#353434",
                      "error-container": "#93000a",
                      "on-secondary": "#303031",
                      "on-tertiary-container": "#696360",
                      "primary-fixed-dim": "#c6c6c7",
                      "secondary-fixed-dim": "#c7c6c6",
                      "on-background": "#e5e2e1",
                      "on-secondary-container": "#b5b5b5",
                      "on-tertiary-fixed": "#1f1b19",
                      "primary-container": "#e2e2e2",
                      "on-secondary-fixed-variant": "#464747",
                      "surface-container-lowest": "#0e0e0e",
                      "on-tertiary-fixed-variant": "#4b4643",
                      "outline": "#8e9192",
                      "surface-container-low": "#1c1b1b",
                      "inverse-surface": "#e5e2e1",
                      "tertiary": "#ffffff"
              },
              "borderRadius": {
                      "DEFAULT": "0.25rem",
                      "lg": "0.5rem",
                      "xl": "0.75rem",
                      "full": "9999px"
              },
              "spacing": {
                      "nav_height": "48px",
                      "xs": "4px",
                      "gutter": "24px",
                      "lg": "24px",
                      "md": "16px",
                      "base": "8px",
                      "sm": "8px",
                      "xl": "32px",
                      "margin_desktop": "40px",
                      "margin_mobile": "16px"
              },
              "fontFamily": {
                      "headline-lg-mobile": ["DM Sans"],
                      "code-md": ["DM Mono"],
                      "display": ["DM Sans"],
                      "headline-lg": ["DM Sans"],
                      "label-md": ["DM Sans"],
                      "body-lg": ["DM Sans"],
                      "headline-md": ["DM Sans"],
                      "body-md": ["DM Sans"]
              },
              "fontSize": {
                      "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                      "code-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                      "display": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                      "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
                      "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "500"}],
                      "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                      "headline-md": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
                      "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}]
              }
            },
          },
        }
    </script>
<style>
        body {
            background-color: #1a1a1a;
            color: #f2f2f2;
            -webkit-font-smoothing: antialiased;
        }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            vertical-align: middle;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #1a1a1a;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #333333;
            border-radius: 2px;
        }
    </style>
</head>
<body class="font-body-md text-body-md min-h-screen overflow-hidden">
<!-- TopNavBar -->
<header class="fixed top-0 w-full h-[48px] z-50 bg-surface-container dark:bg-surface-container border-b border-outline-variant flex justify-between items-center px-margin_desktop">
<div class="flex items-center gap-xl">
<span class="font-headline-md text-headline-md font-bold text-primary tracking-tight">SpecForge</span>
<nav class="hidden md:flex gap-lg">
<a class="font-body-md text-body-md text-primary border-b-2 border-primary pb-1 cursor-pointer active:opacity-80 transition-colors duration-200" href="#">Projects</a>
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary cursor-pointer active:opacity-80 transition-colors duration-200" href="#">Pipeline</a>
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary cursor-pointer active:opacity-80 transition-colors duration-200" href="#">Assets</a>
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary cursor-pointer active:opacity-80 transition-colors duration-200" href="#">Documentation</a>
</nav>
</div>
<div class="flex items-center gap-md">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer" data-icon="settings">settings</button>
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer" data-icon="help">help</button>
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer" data-icon="account_circle">account_circle</button>
</div>
</header>
<!-- SideNavBar -->
<aside class="fixed left-0 top-[48px] h-[calc(100vh-48px)] w-64 bg-surface-container-low dark:bg-surface-container-low border-r border-outline-variant flex flex-col py-md z-40">
<div class="px-md mb-xl">
<div class="flex items-center gap-sm mb-xs">
<div class="w-8 h-8 rounded bg-primary flex items-center justify-center text-surface">
<span class="material-symbols-outlined" data-icon="terminal">terminal</span>
</div>
<div>
<div class="font-headline-md text-headline-md font-bold text-primary">SpecForge</div>
<div class="text-[10px] uppercase tracking-widest text-on-surface-variant">v1.0.4</div>
</div>
</div>
</div>
<nav class="flex-grow px-sm flex flex-col gap-xs">
<a class="flex items-center gap-md px-md py-sm rounded bg-surface-container-highest text-primary font-bold transition-all duration-150 ease-in-out" href="#">
<span class="material-symbols-outlined" data-icon="code">code</span>
<span class="font-label-md text-label-md">Editor</span>
</a>
<a class="flex items-center gap-md px-md py-sm rounded text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all duration-150 ease-in-out" href="#">
<span class="material-symbols-outlined" data-icon="memory">memory</span>
<span class="font-label-md text-label-md">Agent Pipeline</span>
</a>
<a class="flex items-center gap-md px-md py-sm rounded text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all duration-150 ease-in-out" href="#">
<span class="material-symbols-outlined" data-icon="folder_open">folder_open</span>
<span class="font-label-md text-label-md">Files</span>
</a>
<a class="flex items-center gap-md px-md py-sm rounded text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all duration-150 ease-in-out" href="#">
<span class="material-symbols-outlined" data-icon="history">history</span>
<span class="font-label-md text-label-md">History</span>
</a>
</nav>
<div class="px-sm mt-auto flex flex-col gap-xs border-t border-outline-variant pt-md">
<a class="flex items-center gap-md px-md py-sm rounded text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all duration-150 ease-in-out" href="#">
<span class="material-symbols-outlined" data-icon="contact_support">contact_support</span>
<span class="font-label-md text-label-md">Support</span>
</a>
<a class="flex items-center gap-md px-md py-sm rounded text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all duration-150 ease-in-out" href="#">
<span class="material-symbols-outlined" data-icon="settings">settings</span>
<span class="font-label-md text-label-md">Settings</span>
</a>
</div>
</aside>
<!-- Main Content Canvas -->
<main class="ml-64 mt-[48px] h-[calc(100vh-48px)] p-margin_desktop bg-surface-dim overflow-y-auto custom-scrollbar">
<div class="max-w-4xl mx-auto flex flex-col gap-xl">
<!-- Header Section -->
<header class="flex flex-col gap-sm">
<h1 class="font-headline-lg text-headline-lg text-primary">New Project Specification</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">Refine your technical requirements by uploading source documents or describing the core logic in the workspace below.</p>
</header>
<!-- Editor Section -->
<div class="flex flex-col gap-lg">
<!-- Input Canvas (The "Body" from Screen 1) -->
<div class="bg-[#272727] border border-[#333333] rounded-xl p-xl flex flex-col gap-xl transition-all duration-300">
<!-- File Selection Area (Replaces Drop Zone) -->
<div class="flex flex-wrap items-center gap-md">
<!-- File Chip -->
<div class="h-[40px] px-md bg-[#272727] border border-[#333333] rounded-lg flex items-center gap-sm group">
<span class="material-symbols-outlined text-secondary text-[20px]" data-icon="description">description</span>
<div class="flex items-baseline gap-xs">
<span class="font-code-md text-[12px] text-primary">requirements.md</span>
<span class="font-label-md text-on-surface-variant">4.2 KB</span>
</div>
<button class="ml-xs hover:text-error transition-colors flex items-center justify-center p-xs">
<span class="material-symbols-outlined text-[16px]" data-icon="close">close</span>
</button>
</div>
<!-- Add Button (Subtle) -->
<button class="h-[40px] px-md bg-transparent border border-[#333333] border-dashed rounded-lg text-on-surface-variant hover:border-[#444444] hover:text-primary flex items-center gap-sm transition-all">
<span class="material-symbols-outlined text-[20px]" data-icon="add">add</span>
<span class="font-label-md">Attach more</span>
</button>
</div>
<!-- Textarea Workspace -->
<div class="flex flex-col gap-base">
<label class="font-label-md text-on-surface-variant uppercase tracking-widest text-[10px]">Contextual Details</label>
<div class="relative group">
<textarea class="w-full min-h-[320px] bg-[#222222] border border-[#333333] rounded-lg p-lg font-code-md text-code-md text-primary placeholder-[#555555] focus:outline-none focus:border-[#444444] resize-none transition-all custom-scrollbar" placeholder="Paste or type additional logic requirements here... (Optional)"># Project: Neural Interface Dashboard
## Technical Scope
1. Secure OAuth2 authentication flow for hardware nodes.
2. Real-time telemetry visualization using WebGL.
3. Event-driven architecture for low-latency synchronization.

The dashboard needs to prioritize system health and signal integrity over aesthetic flourishes. Ensure the API integrates directly with the Forge core service.</textarea>
<!-- Line Numbers Visual Effect -->
<div class="absolute left-[-40px] top-lg flex flex-col gap-base text-right pr-base select-none text-[#444444] font-code-md text-[12px] opacity-50">
<span>01</span><span>02</span><span>03</span><span>04</span><span>05</span><span>06</span><span>07</span><span>08</span>
</div>
</div>
</div>
<!-- Action Bar -->
<div class="flex justify-between items-center pt-lg border-t border-[#333333]">
<div class="flex items-center gap-lg text-[#888888]">
<div class="flex items-center gap-xs">
<span class="material-symbols-outlined text-[18px]" data-icon="lock_open">lock_open</span>
<span class="font-label-md">Encryption active</span>
</div>
<div class="flex items-center gap-xs">
<span class="material-symbols-outlined text-[18px]" data-icon="auto_awesome">auto_awesome</span>
<span class="font-label-md">Auto-complete: ON</span>
</div>
</div>
<!-- CTA Button Enabled -->
<button class="h-[48px] px-xl bg-[#f2f2f2] text-[#141414] font-bold rounded-lg flex items-center gap-sm hover:bg-white active:scale-[0.98] transition-all group">
                            Analyze requirements
                            <span class="material-symbols-outlined transition-transform group-hover:translate-x-1" data-icon="arrow_forward">arrow_forward</span>
</button>
</div>
</div>
<!-- Secondary Info Grid (Bento Style) -->
<div class="grid grid-cols-12 gap-lg">
<div class="col-span-8 bg-[#222222] border border-[#333333] p-lg rounded-lg flex flex-col gap-base">
<div class="flex items-center justify-between">
<h3 class="font-headline-md text-primary">System Resources</h3>
<span class="text-[10px] text-on-surface-variant bg-surface-container px-sm py-[2px] rounded uppercase">Live</span>
</div>
<div class="flex items-center gap-xl h-12">
<div class="flex-grow bg-[#1a1a1a] h-1.5 rounded-full overflow-hidden border border-[#333333]">
<div class="bg-primary h-full w-1/4 transition-all duration-500"></div>
</div>
<div class="text-right whitespace-nowrap">
<span class="font-code-md text-primary">2.4 / 10 GB</span>
<span class="font-label-md text-on-surface-variant block">Memory Allocation</span>
</div>
</div>
</div>
<div class="col-span-4 bg-[#222222] border border-[#333333] p-lg rounded-lg flex flex-col items-center justify-center gap-base group cursor-pointer hover:border-[#444444] transition-colors">
<span class="material-symbols-outlined text-on-surface-variant group-hover:text-primary transition-colors text-[32px]" data-icon="account_tree">account_tree</span>
<div class="text-center">
<span class="font-label-md block text-primary">Graph View</span>
<span class="font-label-md text-on-surface-variant text-[10px]">Visualize Logic</span>
</div>
</div>
</div>
</div>
</div>
</main>
<!-- Visual Polish: Ambient Noise / Grain -->
<div class="fixed inset-0 pointer-events-none opacity-[0.03] z-[100]" style="background-image: url('https://www.transparenttextures.com/patterns/stardust.png');"></div>
<script>
        // Micro-interactions for button press and subtle hover feedback
        document.querySelectorAll('button, a').forEach(el => {
            el.addEventListener('mousedown', () => {
                el.style.transform = 'scale(0.98)';
            });
            el.addEventListener('mouseup', () => {
                el.style.transform = 'scale(1)';
            });
            el.addEventListener('mouseleave', () => {
                el.style.transform = 'scale(1)';
            });
        });

        // Simple text area focus animation
        const textarea = document.querySelector('textarea');
        const container = textarea?.closest('div.bg-\\[\\#272727\\]');
        
        if(textarea && container) {
            textarea.addEventListener('focus', () => {
                container.style.borderColor = '#444444';
            });
            textarea.addEventListener('blur', () => {
                container.style.borderColor = '#333333';
            });
        }
    </script>
</body></html>

<!-- SpecForge - Uploading -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>SpecForge — Processing File</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=DM+Mono:wght@400;500&amp;family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@100..900&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          "colors": {
                  "primary": "#ffffff",
                  "surface-dim": "#141313",
                  "on-secondary-fixed": "#1b1c1c",
                  "tertiary-fixed-dim": "#cec5c1",
                  "inverse-primary": "#5d5f5f",
                  "secondary": "#c7c6c6",
                  "inverse-on-surface": "#313030",
                  "surface": "#141313",
                  "background": "#141313",
                  "on-primary-fixed-variant": "#454747",
                  "primary-fixed": "#e2e2e2",
                  "on-surface-variant": "#c4c7c8",
                  "on-error-container": "#ffdad6",
                  "surface-container-high": "#2a2a2a",
                  "secondary-fixed": "#e3e2e2",
                  "surface-container-highest": "#353434",
                  "on-primary-fixed": "#1a1c1c",
                  "on-primary-container": "#636565",
                  "outline-variant": "#444748",
                  "on-tertiary": "#342f2d",
                  "error": "#ffb4ab",
                  "on-error": "#690005",
                  "secondary-container": "#464747",
                  "on-surface": "#e5e2e1",
                  "on-primary": "#2f3131",
                  "surface-bright": "#3a3939",
                  "tertiary-container": "#eae1dd",
                  "surface-tint": "#c6c6c7",
                  "surface-container": "#201f1f",
                  "tertiary-fixed": "#eae1dd",
                  "surface-variant": "#353434",
                  "error-container": "#93000a",
                  "on-secondary": "#303031",
                  "on-tertiary-container": "#696360",
                  "primary-fixed-dim": "#c6c6c7",
                  "secondary-fixed-dim": "#c7c6c6",
                  "on-background": "#e5e2e1",
                  "on-secondary-container": "#b5b5b5",
                  "on-tertiary-fixed": "#1f1b19",
                  "primary-container": "#e2e2e2",
                  "on-secondary-fixed-variant": "#464747",
                  "surface-container-lowest": "#0e0e0e",
                  "on-tertiary-fixed-variant": "#4b4643",
                  "outline": "#8e9192",
                  "surface-container-low": "#1c1b1b",
                  "inverse-surface": "#e5e2e1",
                  "tertiary": "#ffffff"
          },
          "borderRadius": {
                  "DEFAULT": "0.25rem",
                  "lg": "0.5rem",
                  "xl": "0.75rem",
                  "full": "9999px"
          },
          "spacing": {
                  "nav_height": "48px",
                  "xs": "4px",
                  "gutter": "24px",
                  "lg": "24px",
                  "md": "16px",
                  "base": "8px",
                  "sm": "8px",
                  "xl": "32px",
                  "margin_desktop": "40px",
                  "margin_mobile": "16px"
          },
          "fontFamily": {
                  "headline-lg-mobile": ["DM Sans"],
                  "code-md": ["DM Mono"],
                  "display": ["DM Sans"],
                  "headline-lg": ["DM Sans"],
                  "label-md": ["DM Sans"],
                  "body-lg": ["DM Sans"],
                  "headline-md": ["DM Sans"],
                  "body-md": ["DM Sans"]
          },
          "fontSize": {
                  "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                  "code-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                  "display": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                  "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
                  "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "500"}],
                  "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                  "headline-md": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
                  "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}]
          }
        },
      },
    }
  </script>
<style>
    .material-symbols-outlined {
      font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 24;
    }
    
    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    .animate-spin-slow {
      animation: spin 2s linear infinite;
    }
    
    body {
      background-color: #141313;
      color: #e5e2e1;
    }

    /* Refined Minimalism Elevation */
    .level-1 { background-color: #1c1b1b; border: 1px solid #333333; }
    .level-2 { background-color: #201f1f; border: 1px solid #333333; }
    
    /* Progress Bar */
    .progress-track { background-color: #2a2a2a; border-radius: 0; }
    .progress-fill { background-color: #f2f2f2; }
  </style>
</head>
<body class="font-body-md text-body-md overflow-hidden">
<!-- TopNavBar (Shell Visibility Suppression Applied: Centered Logo Lockup Only) -->
<header class="fixed top-0 w-full h-[48px] bg-surface-container flex items-center justify-center z-50 border-b border-outline-variant">
<div class="flex items-center gap-2">
<span class="font-headline-md text-headline-md font-bold text-primary tracking-tight">SpecForge</span>
</div>
</header>
<!-- Main Canvas -->
<main class="flex flex-col items-center pt-[100px] px-margin_desktop min-h-screen max-w-[1280px] mx-auto">
<div class="w-full max-w-2xl flex flex-col items-center text-center">
<!-- Heading & Subheading -->
<h1 class="text-[26px] font-headline-lg text-primary mb-2">Reading your file…</h1>
<p class="font-body-lg text-on-surface-variant mb-xl">Hang on while we parse the contents</p>
<!-- File Chip (Immutable Styling) -->
<div class="mb-xl flex items-center gap-2 px-md py-xs bg-surface-container-low border border-outline-variant rounded-sm">
<span class="material-symbols-outlined text-on-surface-variant text-[18px]">description</span>
<span class="font-label-md text-label-md text-on-surface-variant">technical_specification_v2.pdf</span>
</div>
<!-- Progress Section -->
<div class="w-full mb-lg">
<div class="flex justify-between items-center mb-base">
<span class="font-code-md text-code-md text-on-surface-variant">Parsing file contents — 60%</span>
</div>
<div class="progress-track w-full h-[5px] overflow-hidden">
<div class="progress-fill h-full w-[60%] transition-all duration-700 ease-out"></div>
</div>
</div>
<!-- Spinner Row (DM Mono 12px) -->
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-primary animate-spin-slow text-[20px]" style="font-variation-settings: 'wght' 200;">progress_activity</span>
<span class="font-code-md text-[12px] text-on-surface-variant uppercase tracking-widest">Extracting requirements…</span>
</div>
<!-- Atmospheric Background Element -->
<div class="absolute inset-0 -z-10 pointer-events-none opacity-20">
<div class="absolute top-[20%] left-[10%] w-[400px] h-[400px] bg-primary/5 rounded-full blur-[120px]"></div>
<div class="absolute bottom-[20%] right-[10%] w-[300px] h-[300px] bg-primary/5 rounded-full blur-[100px]"></div>
</div>
</div>
</main>
<!-- Subtle Script for Simulation -->
<script>
    // Micro-interaction for progress bar feel
    window.addEventListener('DOMContentLoaded', () => {
      const fill = document.querySelector('.progress-fill');
      const label = document.querySelector('.font-code-md.text-on-surface-variant');
      let progress = 60;

      // Subtle pulse to indicate life
      setInterval(() => {
        if (progress < 68) {
          progress += 0.2;
          fill.style.width = `${progress}%`;
          // Note: In a real app we'd update the label text too
        }
      }, 3000);
    });
  </script>
</body></html>

<!-- SpecForge - Home (Empty) -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>SpecForge — Requirements Analysis</title>
<!-- Material Symbols -->
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&amp;family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "primary": "#ffffff",
                        "surface-dim": "#141313",
                        "on-secondary-fixed": "#1b1c1c",
                        "tertiary-fixed-dim": "#cec5c1",
                        "inverse-primary": "#5d5f5f",
                        "secondary": "#c7c6c6",
                        "inverse-on-surface": "#313030",
                        "surface": "#141313",
                        "background": "#141313",
                        "on-primary-fixed-variant": "#454747",
                        "primary-fixed": "#e2e2e2",
                        "on-surface-variant": "#c4c7c8",
                        "on-error-container": "#ffdad6",
                        "surface-container-high": "#2a2a2a",
                        "secondary-fixed": "#e3e2e2",
                        "surface-container-highest": "#353434",
                        "on-primary-fixed": "#1a1c1c",
                        "on-primary-container": "#636565",
                        "outline-variant": "#444748",
                        "on-tertiary": "#342f2d",
                        "error": "#ffb4ab",
                        "on-error": "#690005",
                        "secondary-container": "#464747",
                        "on-surface": "#e5e2e1",
                        "on-primary": "#2f3131",
                        "surface-bright": "#3a3939",
                        "tertiary-container": "#eae1dd",
                        "surface-tint": "#c6c6c7",
                        "surface-container": "#201f1f",
                        "tertiary-fixed": "#eae1dd",
                        "surface-variant": "#353434",
                        "error-container": "#93000a",
                        "on-secondary": "#303031",
                        "on-tertiary-container": "#696360",
                        "primary-fixed-dim": "#c6c6c7",
                        "secondary-fixed-dim": "#c7c6c6",
                        "on-background": "#e5e2e1",
                        "on-secondary-container": "#b5b5b5",
                        "on-tertiary-fixed": "#1f1b19",
                        "primary-container": "#e2e2e2",
                        "on-secondary-fixed-variant": "#464747",
                        "surface-container-lowest": "#0e0e0e",
                        "on-tertiary-fixed-variant": "#4b4643",
                        "outline": "#8e9192",
                        "surface-container-low": "#1c1b1b",
                        "inverse-surface": "#e5e2e1",
                        "tertiary": "#ffffff"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.25rem",
                        "lg": "0.5rem",
                        "xl": "0.75rem",
                        "full": "9999px"
                    },
                    "spacing": {
                        "nav_height": "48px",
                        "xs": "4px",
                        "gutter": "24px",
                        "lg": "24px",
                        "md": "16px",
                        "base": "8px",
                        "sm": "8px",
                        "xl": "32px",
                        "margin_desktop": "40px",
                        "margin_mobile": "16px"
                    },
                    "fontFamily": {
                        "headline-lg-mobile": ["DM Sans"],
                        "code-md": ["DM Mono"],
                        "display": ["DM Sans"],
                        "headline-lg": ["DM Sans"],
                        "label-md": ["DM Sans"],
                        "body-lg": ["DM Sans"],
                        "headline-md": ["DM Sans"],
                        "body-md": ["DM Sans"]
                    },
                    "fontSize": {
                        "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                        "code-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                        "display": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                        "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
                        "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "500"}],
                        "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                        "headline-md": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
                        "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}]
                    }
                },
            },
        }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            display: inline-block;
            vertical-align: middle;
            line-height: 1;
        }
        body {
            background-color: #1a1a1a;
            color: #f2f2f2;
            -webkit-font-smoothing: antialiased;
        }
        .tonal-bg-0 { background-color: #1a1a1a; }
        .tonal-bg-1 { background-color: #222222; }
        .tonal-bg-2 { background-color: #272727; }
        .border-base { border: 1px solid #333333; }
        .border-active { border: 1px solid #444444; }
        .text-hint { color: #888888; }
        .text-placeholder { color: #555555; }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #1a1a1a; }
        ::-webkit-scrollbar-thumb { background: #333333; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #444444; }
    </style>
</head>
<body class="font-body-md text-body-md selection:bg-primary-container selection:text-on-primary-container">
<!-- TopNavBar -->
<header class="fixed top-0 w-full h-[48px] bg-surface-container border-b border-outline-variant flex justify-between items-center px-margin_desktop z-50">
<div class="flex items-center gap-base">
<img alt="SpecForge Logo" class="w-[28px] h-[28px] rounded-sm" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAA4CAYAAACohjseAAAENUlEQVR4AexazUtUURR/8ywKtFo5BQqCmwlHJXftJGhX+REIEVS7CMpciZsgpZW4Kdy1KrcKfRnarv/A/IBmXLWYAXEhJOMi0Jl+v4f38bzz3n1fd2Z8g3KP9557z73n/Obc37vvvRnTUPx1d3df6e/vf9zX1/cZkoPsQ680UhgD5DfkU29v7yPGqIBguALExKsA8a61tXUHkz+mUqlhSAZyCXpDC2OAXIeMmKa5wBgR61vG7BZYFUAY3sHkbRi/RH0R9akuxzFOoN4G0CE5WCfAFAymYfgNclk2PO06Y65UKqTSK8SagljFBog9/RA9r2FoD0JPVGHskDfA8kQEbgHMZrO3MPBBdCa9Bpb3AHmbOCyAIOsElHOQZinnAeQFxDDBuzQaVeREX9LLUE9PzzWzXC7fR0oTyzuvLBATduaIicYDL6Ok9wuAN5IORBH/TRNnx6k/zBUAlEPExi16QWmV4EHQ74J1TCQYg2/osQCm02ljYGAglrS3t/sGGccgMsC2tjZjcXHRmJ+fjyVLS0sG14oDQjU3MsDOzk6jpaVFtXagMa7R0dERyDaKUWSATmezs7PG3Nyc3UV9fHzcUInTHlc7e67uRjiAHt7z+bxBEcNsr62tGSqhjbDPZDKePI7LUS0AcTkWsVq1rFudin9TU1OePI7LUS0AFbHHHorLUS0AZQ7Juh9KN87q4qgWgF4AVOckeec2r1AoWNx1ctTNLmifFoAy56jzbFOdk5OTk3aMTg66cY7r2cYhG1oAhvTpax52i6sW1AJQDoh6qVQyxsbGlGeh2zk5OjpqHBwcnIiZ653oCKFoARjCn68pr5q+RiEMtACUOULdj4Ne97BnHAyRPZpqyaDMEepnHOTH6yJnHHT5UFRdWraoykGUMW7xKPPc5mgBKAdEvak5yPtMvqsJ8qQu7j357FgsFrW8JXBmUksGee45F3XeW3qdd6JfnHvi3BS6cz15feeYX1sLQDphJo6OjtgUErjmlhbveHgVDZL5oItrAcgAa8k5rh8UkGynBWAYzskBdHV1We9juIYYY5si9Di1FoBhOCe4J9fy86FTbwgH43AuTEbIa/oKM8dpGzmDUTnn9gyo6nN7PnQC8GtHBsiFd3d3rfcnPMNqJXt7e3QVWWIBjOy1jhP5Bei/Ovqrt6u//AKUv0ert+O6+MP5ucMM/qqLt8Y4yTGDPxvju/ZekcFVZnC19q4a4+Hw8HDV3NzczMH9D0hTFWTvSy6X+yOOiQl0NM3VlFhM03zOjFkANzY28lCeQZqi4N716fr6epFgLIBsYKvy55QzbCdcZpCwBYHBBsgODEyjHkaK91EnqjDmcrl89xiDHfsJgOyFwVekOIv2MqR+JZ6nZca8tbX1XV6mCiANALIAuYdPZRD6NOoVSB5Sgt7QchzDNuoVBDKDepCxQgrQq8p/AAAA//9WwbwMAAAABklEQVQDAPjV/3y0ZWKYAAAAAElFTkSuQmCC"/>
<span class="font-headline-md text-headline-md font-bold text-primary tracking-tight">SpecForge</span>
</div>
<nav class="hidden md:flex items-center gap-xl h-full">
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors duration-200" href="#">Projects</a>
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors duration-200" href="#">Pipeline</a>
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors duration-200" href="#">Assets</a>
<a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors duration-200" href="#">Documentation</a>
</nav>
<div class="flex items-center gap-md">
<button class="p-xs text-on-surface-variant hover:text-primary transition-all cursor-pointer">
<span class="material-symbols-outlined">settings</span>
</button>
<button class="p-xs text-on-surface-variant hover:text-primary transition-all cursor-pointer">
<span class="material-symbols-outlined">help</span>
</button>
<button class="flex items-center gap-xs p-xs text-on-surface-variant hover:text-primary transition-all cursor-pointer">
<span class="material-symbols-outlined">account_circle</span>
</button>
</div>
</header>
<!-- Main Content -->
<main class="min-h-screen flex flex-col items-center justify-center pt-[48px] px-margin_mobile md:px-margin_desktop">
<div class="w-full max-w-[520px] flex flex-col items-center">
<!-- Hero Header -->
<div class="flex flex-col items-center text-center mb-xl">
<div class="mb-lg opacity-90">
<img alt="SpecForge Logo" class="w-[48px] h-[48px] rounded-sm mb-md mx-auto shadow-xl" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAA4CAYAAACohjseAAAENUlEQVR4AexazUtUURR/8ywKtFo5BQqCmwlHJXftJGhX+REIEVS7CMpciZsgpZW4Kdy1KrcKfRnarv/A/IBmXLWYAXEhJOMi0Jl+v4f38bzz3n1fd2Z8g3KP9557z73n/Obc37vvvRnTUPx1d3df6e/vf9zX1/cZkoPsQ680UhgD5DfkU29v7yPGqIBguALExKsA8a61tXUHkz+mUqlhSAZyCXpDC2OAXIeMmKa5wBgR61vG7BZYFUAY3sHkbRi/RH0R9akuxzFOoN4G0CE5WCfAFAymYfgNclk2PO06Y65UKqTSK8SagljFBog9/RA9r2FoD0JPVGHskDfA8kQEbgHMZrO3MPBBdCa9Bpb3AHmbOCyAIOsElHOQZinnAeQFxDDBuzQaVeREX9LLUE9PzzWzXC7fR0oTyzuvLBATduaIicYDL6Ok9wuAN5IORBH/TRNnx6k/zBUAlEPExi16QWmV4EHQ74J1TCQYg2/osQCm02ljYGAglrS3t/sGGccgMsC2tjZjcXHRmJ+fjyVLS0sG14oDQjU3MsDOzk6jpaVFtXagMa7R0dERyDaKUWSATmezs7PG3Nyc3UV9fHzcUInTHlc7e67uRjiAHt7z+bxBEcNsr62tGSqhjbDPZDKePI7LUS0AcTkWsVq1rFudin9TU1OePI7LUS0AFbHHHorLUS0AZQ7Juh9KN87q4qgWgF4AVOckeec2r1AoWNx1ctTNLmifFoAy56jzbFOdk5OTk3aMTg66cY7r2cYhG1oAhvTpax52i6sW1AJQDoh6qVQyxsbGlGeh2zk5OjpqHBwcnIiZ653oCKFoARjCn68pr5q+RiEMtACUOULdj4Ne97BnHAyRPZpqyaDMEepnHOTH6yJnHHT5UFRdWraoykGUMW7xKPPc5mgBKAdEvak5yPtMvqsJ8qQu7j357FgsFrW8JXBmUksGee45F3XeW3qdd6JfnHvi3BS6cz15feeYX1sLQDphJo6OjtgUErjmlhbveHgVDZL5oItrAcgAa8k5rh8UkGynBWAYzskBdHV1We9juIYYY5si9Di1FoBhOCe4J9fy86FTbwgH43AuTEbIa/oKM8dpGzmDUTnn9gyo6nN7PnQC8GtHBsiFd3d3rfcnPMNqJXt7e3QVWWIBjOy1jhP5Bei/Ovqrt6u//AKUv0ert+O6+MP5ucMM/qqLt8Y4yTGDPxvju/ZekcFVZnC19q4a4+Hw8HDV3NzczMH9D0hTFWTvSy6X+yOOiQl0NM3VlFhM03zOjFkANzY28lCeQZqi4N716fr6epFgLIBsYKvy55QzbCdcZpCwBYHBBsgODEyjHkaK91EnqjDmcrl89xiDHfsJgOyFwVekOIv2MqR+JZ6nZca8tbX1XV6mCiANALIAuYdPZRD6NOoVSB5Sgt7QchzDNuoVBDKDepCxQgrQq8p/AAAA//9WwbwMAAAABklEQVQDAPjV/3y0ZWKYAAAAAElFTkSuQmCC"/>
</div>
<h1 class="font-headline-lg text-headline-lg text-primary mb-sm" style="font-size: 26px;">
                    Turn a brief into a full spec
                </h1>
<p class="font-body-lg text-body-lg text-hint">
                    Paste your requirements or upload a file to get started
                </p>
</div>
<!-- Interaction Canvas -->
<div class="w-full space-y-md">
<!-- Textarea Section -->
<div class="w-full relative group">
<textarea class="w-full h-[120px] tonal-bg-1 border-base rounded-lg p-md text-primary placeholder-[#555555] focus:outline-none focus:border-[#444444] transition-all resize-none font-body-md text-body-md" id="requirements-input" placeholder="Describe your app idea…"></textarea>
</div>
<!-- Drop Zone -->
<div class="w-full h-[100px] border-base border-dashed rounded-lg tonal-bg-0 flex flex-col items-center justify-center cursor-pointer hover:bg-surface-container-low transition-colors group">
<div class="flex flex-col items-center gap-xs">
<span class="material-symbols-outlined text-[#888888] group-hover:text-primary transition-colors">upload</span>
<p class="text-hint font-label-md text-label-md">
                            Drop a .txt or .md file, or <span class="text-primary underline cursor-pointer">click to browse</span>
</p>
</div>
<input accept=".txt,.md" class="hidden" type="file"/>
</div>
<!-- CTA -->
<button class="w-full py-md rounded-lg tonal-bg-2 text-[#444444] font-bold flex items-center justify-center gap-sm cursor-not-allowed transition-all active:scale-[0.98]" disabled="" id="submit-btn">
                    Analyze requirements
                    <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
</button>
</div>
<!-- Atmospheric Hint -->
<div class="mt-xl flex items-center gap-base">
<div class="w-2 h-2 rounded-full bg-[#333333]"></div>
<p class="text-hint font-label-md text-label-md tracking-widest uppercase opacity-40">Ready for processing</p>
</div>
</div>
</main>
<!-- Micro-interaction Script -->
<script>
        const textarea = document.getElementById('requirements-input');
        const submitBtn = document.getElementById('submit-btn');

        textarea.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            if (val.length > 5) {
                submitBtn.disabled = false;
                submitBtn.classList.remove('tonal-bg-2', 'text-[#444444]', 'cursor-not-allowed');
                submitBtn.classList.add('bg-primary', 'text-background', 'cursor-pointer', 'hover:opacity-90');
            } else {
                submitBtn.disabled = true;
                submitBtn.classList.add('tonal-bg-2', 'text-[#444444]', 'cursor-not-allowed');
                submitBtn.classList.remove('bg-primary', 'text-background', 'cursor-pointer', 'hover:opacity-90');
            }
        });

        // Add some subtle background particles
        const canvas = document.createElement('canvas');
        canvas.className = 'fixed inset-0 pointer-events-none z-[-1] opacity-20';
        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        let width, height;

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }

        window.addEventListener('resize', resize);
        resize();

        const dots = Array.from({ length: 40 }, () => ({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.2,
            vy: (Math.random() - 0.5) * 0.2
        }));

        function animate() {
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = '#444444';
            dots.forEach(dot => {
                dot.x += dot.vx;
                dot.y += dot.vy;
                if (dot.x < 0 || dot.x > width) dot.vx *= -1;
                if (dot.y < 0 || dot.y > height) dot.vy *= -1;
                ctx.beginPath();
                ctx.arc(dot.x, dot.y, 1, 0, Math.PI * 2);
                ctx.fill();
            });
            requestAnimationFrame(animate);
        }
        animate();
    </script>
</body></html>