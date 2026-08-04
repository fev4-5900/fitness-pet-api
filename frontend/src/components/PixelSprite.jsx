// Generic pixel-art renderer: an array of strings (one per row),
// each character maps to a color. '.' is transparent.
// Rows shorter than the widest row are centered automatically.
export default function PixelSprite({ rows, palette, className, size }) {
  const width = Math.max(...rows.map((r) => r.length))
  const height = rows.length

  const rects = []
  rows.forEach((row, y) => {
    const pad = Math.floor((width - row.length) / 2)
    for (let x = 0; x < row.length; x++) {
      const color = palette[row[x]]
      if (color) rects.push(<rect key={`${x}-${y}`} x={x + pad} y={y} width="1" height="1" fill={color} />)
    }
  })

  return (
    <svg
      className={className}
      viewBox={`0 0 ${width} ${height}`}
      width={size}
      height={size ? size * (height / width) : undefined}
      shapeRendering="crispEdges"
      aria-hidden="true"
    >
      {rects}
    </svg>
  )
}
