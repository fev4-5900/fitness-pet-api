import PixelSprite from './PixelSprite'

const PALETTE = {
  B: '#2B1E12', // outline
  d: '#6E4523', // dark fur
  f: '#A8763E', // mid fur
  F: '#C89A63', // light fur
  w: '#FFF6E4', // cream belly
  E: '#1C1309', // eye
  e: '#FFFFFF', // eye highlight
  n: '#4A2C14', // nose
  p: '#D9A08B', // inner ear
  s: '#C75B22', // scarf
  t: '#E8924A', // scarf highlight
}

// Ears are 30 wide, head is 30 wide -> everything stays aligned
const TOP = [
  '......BB..............BB......',
  '.....B..B............B..B.....',
  '.....b.pp............pp.b.....',
  '.....bdd..............ddb.....',
  '......bb..............bb......',
  '...' + 'b'.repeat(24) + '...',
  '..bF' + 'f'.repeat(22) + 'Fb..',
  '..bF' + 'f'.repeat(22) + 'Fb..',
  '..bff' + 'w'.repeat(20) + 'ffb..',
  '..bff' + 'w'.repeat(20) + 'ffb..',
]

// Face rows share the exact same 30-wide layout so eyes/nose/mouth line up.
const FACE = {
  happy: [
    '..bff' + 'w'.repeat(20) + 'ffb..',
    '..bffwww' + 'Be' + 'w'.repeat(9) + 'Be' + 'wwwwffb..',
    '..bff' + 'w'.repeat(20) + 'ffb..',
    '..bff' + 'w'.repeat(9) + 'nn' + 'w'.repeat(9) + 'ffb..',
    '..bff' + 'w'.repeat(8) + 'nnn' + 'w'.repeat(9) + 'ffb..',
    '..bff' + 'w'.repeat(20) + 'ffb..',
  ],
  ok: [
    '..bff' + 'w'.repeat(20) + 'ffb..',
    '..bffwww' + 'BE' + 'w'.repeat(11) + 'BE' + 'wwffb..',
    '..bff' + 'w'.repeat(20) + 'ffb..',
    '..bff' + 'w'.repeat(9) + 'nn' + 'w'.repeat(9) + 'ffb..',
    '..bff' + 'w'.repeat(9) + 'nn' + 'w'.repeat(9) + 'ffb..',
    '..bff' + 'w'.repeat(20) + 'ffb..',
  ],
  sad: [
    '..bff' + 'w'.repeat(20) + 'ffb..',
    '..bffwww' + 'B' + 'w'.repeat(13) + 'B' + 'wwffb..',
    '..bff' + 'w'.repeat(20) + 'ffb..',
    '..bff' + 'w'.repeat(9) + 'nn' + 'w'.repeat(9) + 'ffb..',
    '..bff' + 'w'.repeat(8) + 'nn' + 'w'.repeat(10) + 'ffb..',
    '..bff' + 'w'.repeat(20) + 'ffb..',
  ],
}

const SCARF = [
  '..b' + 's'.repeat(24) + 'b..',
  '..bt' + 's'.repeat(22) + 'tb..',
]

const BODY = [
  '...b' + 'f'.repeat(22) + 'b...',
  '..bF' + 'w'.repeat(22) + 'Fb..',
  '..bF' + 'w'.repeat(22) + 'Fb..',
  '...b' + 'f'.repeat(22) + 'b...',
  '....' + 'b'.repeat(22) + '....',
  '......bbb......bbb......',
  '......Fbb......bbF......',
]

export default function Chinchilla({ mood = 'ok', level = 1, size = 200, className }) {
  const rows = [...TOP, ...(FACE[mood] || FACE.ok), ...(level >= 5 ? SCARF : []), ...BODY]
  return <PixelSprite rows={rows} palette={PALETTE} className={className} size={size} />
}
