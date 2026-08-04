// Cozy pixel-art scene: a cabin wall with a fireplace (campfire vibe),
// a bookshelf (library vibe) and a dumbbell (gym vibe), all in browns.
const C = {
  wall: '#A8773F',
  wallLight: '#B4824A',
  wallDark: '#9C6B38',
  beam: '#7A4F28',
  floor: '#8A5A2E',
  floorDark: '#7A4E26',
  stone: '#6E4523',
  stoneLight: '#7E5230',
  fireDark: '#1C1309',
  flameA: '#E8924A',
  flameB: '#C75B22',
  glow: '#C75B22',
  ember: '#F2B65C',
  shelf: '#6E4523',
  book: ['#A63D2F', '#4E7A44', '#C89A63', '#33527A', '#7A4E26'],
  rug: '#B4502E',
  rugEdge: '#8A3A22',
  wood: '#9C6B38',
  woodDark: '#6E4523',
}

export default function Scene({ children }) {
  const floorY = 34
  const floorH = 22
  return (
    <div className="scene">
      <svg className="scene-svg" viewBox="0 0 96 56" preserveAspectRatio="xMidYMid slice">
        <defs>
          <linearGradient id="wallGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={C.wallLight} />
            <stop offset="100%" stopColor={C.wall} />
          </linearGradient>
        </defs>

        {/* wall */}
        <rect x="0" y="0" width="96" height={floorY} fill="url(#wallGrad)" />
        {[24, 48, 72].map((x) => (
          <rect key={x} x={x} y="0" width="1" height={floorY} fill={C.beam} />
        ))}

        {/* window with starry night */}
        <rect x="6" y="6" width="14" height="12" fill="#2A1E33" />
        <rect x="12" y="6" width="1" height="12" fill={C.beam} />
        <rect x="6" y="11" width="14" height="1" fill={C.beam} />
        <rect x="9" y="8" width="2" height="2" fill="#F2E4C4" />
        <rect x="15" y="13" width="2" height="2" fill="#F2E4C4" />

        {/* bookshelf */}
        <rect x="78" y="6" width="14" height="24" fill={C.shelf} />
        <rect x="80" y="8" width="10" height="5" fill={C.wood} />
        <rect x="80" y="15" width="10" height="5" fill={C.wood} />
        <rect x="80" y="22" width="10" height="5" fill={C.wood} />
        {C.book.map((b, i) => (
          <rect key={`b1-${i}`} x={81 + i * 2} y="9" width="1.5" height="3" fill={b} />
        ))}
        {C.book.map((b, i) => (
          <rect key={`b2-${i}`} x={81 + i * 2} y="16" width="1.5" height="3" fill={b} />
        ))}
        <rect x="81" y="23" width="8" height="3" fill={C.book[1]} />

        {/* fireplace */}
        <rect x="38" y="12" width="20" height="22" fill={C.stone} />
        <rect x="42" y="16" width="12" height="16" fill={C.fireDark} />
        <rect x="38" y="11" width="20" height="1" fill={C.stoneLight} />
        {/* fire */}
        <g className="scene-fire">
          <rect x="45" y="27" width="6" height="4" fill={C.flameB} />
          <rect x="47" y="23" width="2" height="4" fill={C.flameA} />
          <rect x="47" y="20" width="1" height="3" fill={C.flameA} />
          <rect x="43" y="29" width="10" height="2" fill={C.flameB} />
        </g>
        <rect x="43" y="30" width="10" height="1" fill={C.ember} />
        <g className="scene-ember">
          <rect x="48" y="14" width="1" height="1" fill={C.ember} />
          <rect x="52" y="11" width="1" height="1" fill={C.ember} />
        </g>

        {/* dumbbell */}
        <rect x="10" y="28" width="16" height="2" fill={C.woodDark} />
        <rect x="12" y="26" width="3" height="6" fill={C.wood} />
        <rect x="21" y="26" width="3" height="6" fill={C.wood} />
        <rect x="17" y="27" width="2" height="4" fill={C.wood} />

        {/* hanging lantern */}
        <rect x="69" y="4" width="1" height="4" fill={C.beam} />
        <rect x="66" y="8" width="7" height="1" fill={C.beam} />
        <rect x="67" y="9" width="5" height="7" fill={C.flameA} />
        <rect x="68" y="10" width="3" height="5" fill={C.glow} />
        <rect x="67" y="16" width="5" height="1" fill={C.beam} />

        {/* floor */}
        <rect x="0" y={floorY} width="96" height={floorH} fill={C.floor} />
        {[16, 32, 48, 64, 80].map((x) => (
          <rect key={x} x={x} y={floorY} width="1" height={floorH} fill={C.floorDark} />
        ))}

        {/* rug */}
        <rect x="36" y="38" width="24" height="12" fill={C.rug} />
        <rect x="38" y="40" width="20" height="8" fill={C.rugEdge} />

        {/* pet shadow */}
        <rect x="42" y="51" width="12" height="2" fill="#5A3A1E" />
        <rect x="44" y="53" width="8" height="1" fill="#5A3A1E" />
      </svg>
      <div className="scene-pet">{children}</div>
    </div>
  )
}
