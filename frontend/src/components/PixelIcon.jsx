import PixelSprite from './PixelSprite'

const PALETTE = {
  o: '#2B1E12', // outline
  a: '#C75B22', // accent
  b: '#4E7A44', // blue-ish green
  w: '#FFF6E4', // white
  d: '#7A4E26', // dark
  g: '#B4824A', // gold
  r: '#A63D2F', // red
}

const ICONS = {
  fire: [
    '.oo.',
    'ooo.',
    'ooo.',
    '.oo.',
    '..o.',
  ],
  meat: [
    '.....',
    'orr..',
    'orrrr',
    'orrrr',
    'orr..',
    '.....',
  ],
  moon: [
    '...o..',
    '.oooo.',
    'ooooo.',
    'ooooo.',
    'oooo..',
    '......',
  ],
  paw: [
    '...o.',
    '.ooo.',
    '.ooo.',
    '.ooo.',
    'ooooo',
    '.o.o.',
  ],
  water: [
    '..b..',
    '.bwb.',
    '.bwb.',
    '.bwb.',
    '..b..',
  ],
  target: [
    '..ggg..',
    '.gwgwg.',
    'gwwgwwg',
    'gwwwwg.',
    '.gwwg..',
    '..gg...',
  ],
  home: [
    '...oo...',
    '..owwo..',
    '.owwwwo.',
    'owwwwww',
    'owwwwwwo',
    'owwwwwo.',
    'owwwwo..',
    'owoowo..',
  ],
  plus: [
    '..o..',
    '..o..',
    'ooooo',
    '..o..',
    '..o..',
  ],
  x: [
    'o...o',
    '.o.o.',
    '..o..',
    '.o.o.',
    'o...o',
  ],
  profile: [
    '..ooo..',
    '.owwwo.',
    '.owwwo.',
    '..ooo..',
    'ooooooo',
    'owwwwwo',
    '.ooooo.',
  ],
  logout: [
    'owwww.',
    'owwoo.',
    'oww.oo',
    'oww.oo',
    'owwoo.',
    'owwww.',
  ],
  dumbbell: [
    '..d..d.',
    '..d..d.',
    '..d..d.',
    'ddddddd',
    '..d..d.',
    '..d..d.',
  ],
  star: [
    '..o..',
    'oooo.',
    'ooooo',
    '.oooo',
    '..o..',
  ],
  leaf: [
    '..o...',
    '.ogo..',
    'oggoo.',
    '.ogooo',
    '..oo..',
  ],
  bed: [
    '......',
    '.wwww.',
    'owwww.',
    'owwww.',
    'ooooo.',
  ],
  fork: [
    'o.o.',
    'o.o.',
    'o.o.',
    '.o..',
    '.d..',
    '..d.',
  ],
}

export default function PixelIcon({ name, size = 18, className }) {
  const rows = ICONS[name] || ICONS.home
  return <PixelSprite rows={rows} palette={PALETTE} className={className} size={size} />
}
