# Design System: Editorial Investigativo Sóbrio

## 1. Definição do Estilo

- **Nome:** Editorial Investigativo Sóbrio
- **Tipo:** Serious, Informative, Authoritative
- **Keywords:** investigative journalism, news, analysis, authoritative, informative, serious, clean, structured, deep, trustworthy
- **Era:** 2026+ Informação Crítica
- **Light/Dark:** ✓ Full / ✗ No

## 2. Paleta de Cores

- **Primárias:** Cinza Escuro #2C3E50, Branco #FFFFFF, Vermelho Escuro #8B0000, Preto #000000
- **Secundárias:** Azul Marinho #001F3F, Verde Oliva #6B8E23, Amarelo Ocre #CC7722, Cinza Claro #E0E0E0

## 3. Efeitos Visuais

Tipografia serifada clássica para títulos e sans-serif para corpo, layouts de coluna de jornal, imagens em preto e branco ou com tons sépios, elementos gráficos de infográficos e dados, micro-interações de destaque de texto importante, transições de seção diretas e sem distrações.

## 4. AI Prompt Keywords

Design a serious and informative editorial landing page for an investigative journalism platform. Use: classic serif typography for headlines, sans-serif for body, newspaper-like column layouts, black and white/sepia images, infographic and data graphic elements, important text highlight micro-interactions, direct distraction-free section transitions, dark grey and deep red accents, authoritative and trustworthy feel.

## 5. CSS Technical

```css
background: #FFFFFF, color: #2C3E50, border-bottom: 1px solid #C0C0C0, font-family: "Merriweather, serif", line-height: 1.8, transition: all 0.3s ease-in-out, .report-column, .infographic-element, .text-highlight-subtle.
```

## 6. Design System Variables

```css
--dark-grey-bg: #2C3E50, --white-text: #FFFFFF, --dark-red: #8B0000, --black-text: #000000, --font-serif-news: "Merriweather, serif", --font-sans-body: "Roboto, sans-serif", --line-height-body: 1.8, --border-subtle: 1px solid #C0C0C0.
```

## 7. Checklist de Implementação

- ☐ Tipografia serifada/sans-serif
- ☐ Layouts de coluna de jornal
- ☐ Imagens P&B/sépia
- ☐ Infográficos/dados
- ☐ Micro-interações de destaque de texto
- ☐ Transições diretas.

## 8. Visual Theme & Atmosphere

Editorial Investigativo Sóbrio — Design editorialstyle com investigative journalism, news, analysis. Template e prompt pronto para IA. Estilo Editorial Investigativo Sóbrio representa uma tendência moderna em design UI/UX web com foco em editorialstyle.

- Density: 3/10 — Airy
- Variance: 2/10 — Structured
- Motion: 4/10 — Subtle

## 9. Color Palette & Roles

- **Cinza Escuro** (#2C3E50) — Dark surface, primary background
- **Branco** (#FFFFFF) — Light surface, card backgrounds
- **Vermelho Escuro** (#8B0000) — Dark surface, primary background
- **Preto** (#000000) — Dark surface, primary background
- **Azul Marinho** (#001F3F) — Secondary accent
- **Verde Oliva** (#6B8E23) — Success states, positive indicators
- **Amarelo Ocre** (#CC7722) — Warning states, attention indicators
- **Cinza Claro** (#E0E0E0) — Secondary text, borders, muted elements

## 10. Typography Rules

- **Display / Hero:** Merriweather — Weight 700, tight tracking, used for headline impact
- **Body:** Merriweather — Weight 400, 16px/1.6 line-height, max 72ch per line
- **UI Labels / Captions:** Merriweather — 0.875rem, weight 500, slight letter-spacing
- **Monospace:** JetBrains Mono — Used for code, metadata, and technical values

Scale:
- Hero: clamp(2.5rem, 5vw, 4rem)
- H1: 2.25rem
- H2: 1.5rem
- Body: 1rem / 1.6
- Small: 0.875rem

## 11. Component Stylings

- **Primary Button:** Subtly rounded (0.5rem) shape. Accent color fill. Hover: 8% darken + subtle lift shadow. Active: -1px translate tactile press. Font weight 600. No outer glows.
- **Secondary / Ghost Button:** Outline variant. 1.5px border in muted color. Text in primary color. Hover: subtle background fill.
- **Cards:** Subtly rounded (0.5rem) corners. Surface background. Subtle shadow (0 2px 12px rgba(0,0,0,0.06)). 1px border stroke.
- **Inputs:** Label above input. 1px border stroke. Focus ring: 2px accent color offset 2px. Error text below in semantic red. No floating labels.
- **Navigation:** Primary surface background. Active item: accent color indicator. Font weight 500 when active.
- **Skeletons:** Shimmer animation matching component dimensions. No circular spinners.
- **Empty States:** Icon-based composition with descriptive text and action button.

## 12. Layout Principles

- **Grid:** CSS Grid primary. Max-width containment: 1280px centered with 1.5rem side padding.
- **Spacing rhythm:** Balanced. Base unit: 0.5rem (8px).
- **Section vertical gaps:** clamp(4rem, 8vw, 8rem).
- **Hero layout:** Split-screen (text left, visual right).
- **Feature sections:** Zig-zag alternating text+image rows. No 3-equal-columns.
- **Mobile collapse:** All multi-column layouts collapse below 768px. No horizontal overflow.
- **z-index contract:** base (0) / sticky-nav (100) / overlay (200) / modal (300) / toast (500).

## 13. Motion & Interaction

- **Physics:** Ease-out curves, 200-300ms duration. Smooth and predictable.
- **Entry animations:** Fade + translate-Y (16px → 0) over 420ms ease-out. Staggered cascades for lists: 80ms between items.
- **Hover states:** Subtle color shift + shadow adjustment over 200ms.
- **Page transitions:** Fade only (200ms).
- **Performance:** Only transform and opacity animated. No layout-triggering properties.

## 14. Anti-Patterns (Banned)

- No emojis in UI — use icon system only (Lucide, Heroicons)
- No pure black (#000000) — use off-black or charcoal variants
- No oversaturated accent colors (saturation cap: 80%)
- No 3-column equal-width feature layouts — use zig-zag or asymmetric grid
- No `h-screen` — use `min-h-[100dvh]`
- No AI copywriting clichés: "Elevate", "Seamless", "Unleash", "Next-Gen"
- No broken external image links — use picsum.photos or inline SVG
- No generic lorem ipsum in demos

## Contexto Histórico

Estilo Editorial Investigativo Sóbrio representa uma tendência moderna em design UI/UX web com foco em editorialstyle.

## Caso de Uso

Landing pages, Websites modernas
