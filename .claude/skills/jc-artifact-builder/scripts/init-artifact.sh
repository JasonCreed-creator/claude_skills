#!/bin/bash

# Exit on error
set -e

# Detect Node version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)

echo "🔍 Detected Node.js version: $NODE_VERSION"

if [ "$NODE_VERSION" -lt 18 ]; then
  echo "❌ Error: Node.js 18 or higher is required"
  echo "   Current version: $(node -v)"
  exit 1
fi

# Set Vite version based on Node version
if [ "$NODE_VERSION" -ge 20 ]; then
  VITE_VERSION="latest"
  echo "✅ Using Vite latest (Node 20+)"
else
  VITE_VERSION="5.4.11"
  echo "✅ Using Vite $VITE_VERSION (Node 18 compatible)"
fi

# Detect OS and set sed syntax
if [[ "$OSTYPE" == "darwin"* ]]; then
  SED_INPLACE="sed -i ''"
else
  SED_INPLACE="sed -i"
fi

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
  echo "📦 pnpm not found. Installing pnpm..."
  npm install -g pnpm
fi

# Check if project name is provided
if [ -z "$1" ]; then
  echo "❌ Usage: ./init-artifact.sh <project-name>"
  exit 1
fi

PROJECT_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPONENTS_TARBALL="$SCRIPT_DIR/shadcn-components.tar.gz"

# Check if components tarball exists
if [ ! -f "$COMPONENTS_TARBALL" ]; then
  echo "❌ Error: shadcn-components.tar.gz not found in script directory"
  echo "   Expected location: $COMPONENTS_TARBALL"
  exit 1
fi

echo "🚀 Creating new React + Vite project: $PROJECT_NAME"

# Create new Vite project (always use latest create-vite, pin vite version later)
pnpm create vite "$PROJECT_NAME" --template react-ts

# Navigate into project directory
cd "$PROJECT_NAME"

echo "🧹 Cleaning up Vite template..."
$SED_INPLACE '/<link rel="icon".*vite\.svg/d' index.html
$SED_INPLACE 's/<title>.*<\/title>/<title>'"$PROJECT_NAME"'<\/title>/' index.html

# jc: Pretendard 폰트(한국어 우선) CDN 주입 — 미로드 시 system 한글 폰트로 폴백
echo "🔤 Injecting Pretendard font (jc-design-system)..."
$SED_INPLACE 's#</head>#  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />\n  </head>#' index.html

echo "📦 Installing base dependencies..."
pnpm install

# Pin Vite version for Node 18
if [ "$NODE_VERSION" -lt 20 ]; then
  echo "📌 Pinning Vite to $VITE_VERSION for Node 18 compatibility..."
  pnpm add -D vite@$VITE_VERSION
fi

echo "📦 Installing Tailwind CSS and dependencies..."
pnpm install -D tailwindcss@3.4.1 postcss autoprefixer @types/node tailwindcss-animate
pnpm install class-variance-authority clsx tailwind-merge lucide-react next-themes

echo "⚙️  Creating Tailwind and PostCSS configuration..."
cat > postcss.config.js << 'EOF'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF

echo "📝 Configuring Tailwind with jc-design-system theme..."
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // --- jc-design-system 시그니처 확장 ---
        navy: "#0A2540",            // --jc-primary (헤더·표지·로고)
        success: "#00C853",         // --jc-success
        warning: "#FFA000",         // --jc-warning
        info: "#2962FF",            // --jc-info (accent 재사용)
        chart: {
          1: "hsl(var(--chart-1))", 2: "hsl(var(--chart-2))", 3: "hsl(var(--chart-3))",
          4: "hsl(var(--chart-4))", 5: "hsl(var(--chart-5))", 6: "hsl(var(--chart-6))",
        },
        // 인포그래픽 스케일 (jc signature-tokens §1.8) — bg-scaleBlue-3 등
        scaleBlue:  { 1: "#0A2540", 2: "#1E4DCC", 3: "#2962FF", 4: "#5B9BD5", 5: "#E8EFFF" },
        scaleGreen: { 1: "#00733B", 2: "#00C853", 3: "#4CDE8A", 4: "#9CEBC4", 5: "#E6F8EE" },
        scaleRed:   { 1: "#8E1F1F", 2: "#D32F2F", 3: "#E57373", 4: "#F2B8B8", 5: "#FBEAEA" },
        scaleAmber: { 1: "#8A5200", 2: "#C77F00", 3: "#FFA000", 4: "#FFC24D", 5: "#FFF3E0" },
      },
      fontFamily: {
        sans: ["Pretendard", "Pretendard Variable", "-apple-system", "BlinkMacSystemFont", "system-ui", "Roboto", "Helvetica Neue", "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", "sans-serif"],
        mono: ["JetBrains Mono", "D2Coding", "Consolas", "monospace"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
EOF

# Add Tailwind directives and CSS variables to index.css (jc-design-system tokens)
echo "🎨 Adding Tailwind directives and jc-design-system CSS variables..."
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

/* jc-design-system 토큰 매핑 (값 정본: signature-tokens.md §6 / mode-mapping.md §3·§3.2) */
@layer base {
  :root {
    --background: 220 27% 98%;          /* #F8F9FB jc-bg */
    --foreground: 222 16% 12%;          /* #1A1D24 jc-text */
    --card: 0 0% 100%;                  /* #FFFFFF jc-surface */
    --card-foreground: 222 16% 12%;
    --popover: 0 0% 100%;
    --popover-foreground: 222 16% 12%;
    --primary: 224 100% 58%;            /* #2962FF jc-accent (CTA/버튼) */
    --primary-foreground: 0 0% 100%;
    --secondary: 220 27% 96%;           /* #F1F3F7 jc-surface-alt */
    --secondary-foreground: 222 16% 12%;
    --muted: 220 27% 96%;
    --muted-foreground: 218 11% 40%;    /* #5A6270 jc-text-muted */
    --accent: 222 100% 95%;             /* #E8EFFF jc-accent-soft */
    --accent-foreground: 224 74% 46%;   /* #1E4DCC jc-accent-strong */
    --destructive: 0 65% 51%;           /* #D32F2F jc-danger */
    --destructive-foreground: 0 0% 100%;
    --border: 218 18% 91%;              /* #E5E8ED jc-border */
    --input: 218 18% 91%;
    --ring: 224 100% 58%;               /* #2962FF jc-accent */
    --radius: 0.5rem;                   /* jc radius md = 8px */
    /* 차트 데이터 시리즈 (jc §1.4) */
    --chart-1: 224 100% 58%;            /* #2962FF */
    --chart-2: 340 82% 52%;             /* #E91E63 */
    --chart-3: 14 100% 57%;             /* #FF5722 */
    --chart-4: 151 100% 45%;            /* #00E676 */
    --chart-5: 210 73% 15%;             /* #0A2540 */
    --chart-6: 262 83% 58%;             /* #7C3AED */
  }

  .dark {
    --background: 218 52% 8%;           /* #0A1220 jc-bg(dark) */
    --foreground: 216 28% 93%;          /* #E8ECF2 */
    --card: 217 42% 14%;                /* #152134 jc-surface(dark) */
    --card-foreground: 216 28% 93%;
    --popover: 217 42% 14%;
    --popover-foreground: 216 28% 93%;
    --primary: 220 82% 65%;             /* #5B8DEF jc-accent(dark) */
    --primary-foreground: 218 52% 8%;
    --secondary: 218 36% 19%;           /* #1F2C42 jc-surface-alt(dark) */
    --secondary-foreground: 216 28% 93%;
    --muted: 218 36% 19%;
    --muted-foreground: 216 12% 67%;    /* #A0A8B4 jc-text-muted(dark) */
    --accent: 218 36% 19%;
    --accent-foreground: 216 28% 93%;
    --destructive: 4 90% 58%;           /* #F44336 jc DARK_DANGER §8 */
    --destructive-foreground: 218 52% 8%;
    --border: 221 31% 24%;              /* #2A3650 jc-border(dark) */
    --input: 221 31% 24%;
    --ring: 220 82% 65%;                /* #5B8DEF */
    /* 차트 다크 보정 (jc §3.2) */
    --chart-1: 220 82% 65%;             /* #5B8DEF */
    --chart-2: 339 84% 62%;             /* #F04D85 */
    --chart-3: 15 100% 64%;             /* #FF7649 */
    --chart-4: 150 85% 57%;             /* #33EE92 */
    --chart-5: 216 16% 82%;             /* #C9CFD8 */
    --chart-6: 255 92% 76%;             /* #A78BFA */
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground font-sans antialiased;
  }
}
EOF

# Add path aliases to tsconfig.json
echo "🔧 Adding path aliases to tsconfig.json..."
node -e "
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('tsconfig.json', 'utf8'));
config.compilerOptions = config.compilerOptions || {};
config.compilerOptions.baseUrl = '.';
config.compilerOptions.paths = { '@/*': ['./src/*'] };
fs.writeFileSync('tsconfig.json', JSON.stringify(config, null, 2));
"

# Add path aliases to tsconfig.app.json
echo "🔧 Adding path aliases to tsconfig.app.json..."
node -e "
const fs = require('fs');
const path = 'tsconfig.app.json';
const content = fs.readFileSync(path, 'utf8');
// Remove comments manually
const lines = content.split('\n').filter(line => !line.trim().startsWith('//'));
const jsonContent = lines.join('\n');
const config = JSON.parse(jsonContent.replace(/\/\*[\s\S]*?\*\//g, '').replace(/,(\s*[}\]])/g, '\$1'));
config.compilerOptions = config.compilerOptions || {};
config.compilerOptions.baseUrl = '.';
config.compilerOptions.paths = { '@/*': ['./src/*'] };
fs.writeFileSync(path, JSON.stringify(config, null, 2));
"

# Update vite.config.ts
echo "⚙️  Updating Vite configuration..."
cat > vite.config.ts << 'EOF'
import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
EOF

# Install all shadcn/ui dependencies
echo "📦 Installing shadcn/ui dependencies..."
pnpm install @radix-ui/react-accordion @radix-ui/react-aspect-ratio @radix-ui/react-avatar @radix-ui/react-checkbox @radix-ui/react-collapsible @radix-ui/react-context-menu @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-hover-card @radix-ui/react-label @radix-ui/react-menubar @radix-ui/react-navigation-menu @radix-ui/react-popover @radix-ui/react-progress @radix-ui/react-radio-group @radix-ui/react-scroll-area @radix-ui/react-select @radix-ui/react-separator @radix-ui/react-slider @radix-ui/react-slot @radix-ui/react-switch @radix-ui/react-tabs @radix-ui/react-toast @radix-ui/react-toggle @radix-ui/react-toggle-group @radix-ui/react-tooltip
pnpm install sonner cmdk vaul embla-carousel-react react-day-picker react-resizable-panels date-fns react-hook-form @hookform/resolvers zod

# Extract shadcn components from tarball
echo "📦 Extracting shadcn/ui components..."
tar -xzf "$COMPONENTS_TARBALL" -C src/

# Create components.json for reference
echo "📝 Creating components.json config..."
cat > components.json << 'EOF'
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
EOF

echo "✅ Setup complete! Tailwind + shadcn/ui + jc-design-system theme ready."
echo ""
echo "🎨 jc-design-system 테마 적용됨:"
echo "  - 폰트: Pretendard(한국어 우선) + JetBrains Mono"
echo "  - primary=#2962FF(Electric Blue), navy=#0A2540, 다크모드 #0A1220 계열"
echo "  - 차트: bg-chart-1..6 (라이트/다크 자동), 스케일: bg-scaleBlue-1..5 등"
echo "  - 다크 토글: <html class=\"dark\"> 또는 next-themes"
echo "  - 자세한 매핑/사용법: references/jc-theme.md"
echo ""
echo "📦 Included components (40+): accordion, alert, badge, button, card, chart-friendly"
echo "  dialog, dropdown-menu, form, input, select, table, tabs, toast, tooltip, ..."
echo ""
echo "To start developing:"
echo "  cd $PROJECT_NAME"
echo "  pnpm dev"
echo ""
echo "📚 Import components like:"
echo "  import { Button } from '@/components/ui/button'"
echo "  import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'"
