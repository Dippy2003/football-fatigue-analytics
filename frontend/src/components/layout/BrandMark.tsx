export function BrandMark() {
  return (
    <svg
      aria-hidden="true"
      className="brand-mark"
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="brand-gradient" x1="4" y1="3" x2="36" y2="38">
          <stop stopColor="#2dd4bf" />
          <stop offset="1" stopColor="#0f766e" />
        </linearGradient>
      </defs>
      <rect width="40" height="40" rx="12" fill="url(#brand-gradient)" />
      <path
        d="M8 11.5h24v17H8zM20 11.5v17M8 20h7l2.25-5 4.5 10 2.5-5H32"
        stroke="white"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="20" cy="20" r="3.5" stroke="white" strokeWidth="1.5" />
    </svg>
  )
}
