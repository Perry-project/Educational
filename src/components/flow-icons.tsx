import type { ReactNode } from "react";

function Icon({ children }: { children: ReactNode }) {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {children}
    </svg>
  );
}

// Science stream — flask
export function IconScience() {
  return (
    <Icon>
      <path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3" />
      <path d="M7.5 15h9" />
    </Icon>
  );
}

// Commerce stream — briefcase
export function IconCommerce() {
  return (
    <Icon>
      <rect x="3" y="7" width="18" height="13" rx="2" />
      <path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
      <path d="M3 12h18" />
    </Icon>
  );
}

// Humanities stream — open book
export function IconHumanities() {
  return (
    <Icon>
      <path d="M12 6.5c-1.5-1.3-3.6-2-6-2v13c2.4 0 4.5.7 6 2 1.5-1.3 3.6-2 6-2V4.5c-2.4 0-4.5.7-6 2Z" />
      <path d="M12 6.5v13" />
    </Icon>
  );
}

// Vocational stream — wrench
export function IconVocational() {
  return (
    <Icon>
      <path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2-2 2.6-2.6Z" />
    </Icon>
  );
}

// Entrance exam — document with pencil
export function IconExam() {
  return (
    <Icon>
      <path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8Z" />
      <path d="M14 3v5h5" />
      <path d="M9 13.5 13.5 9l1.5 1.5L10.5 15H9v-1.5Z" />
    </Icon>
  );
}

// Course — graduation cap
export function IconCourse() {
  return (
    <Icon>
      <path d="M12 3 2 8l10 5 10-5-10-5Z" />
      <path d="M6 10.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-5.5" />
    </Icon>
  );
}

// Career outcome — flag on a pole
export function IconCareer() {
  return (
    <Icon>
      <path d="M6 21V4" />
      <path d="M6 4h12l-3 4 3 4H6" />
    </Icon>
  );
}

// Start of the flow
export function IconStart() {
  return (
    <Icon>
      <path d="M6 4v16" />
      <path d="M6 5h10l-2.5 3.5L16 12H6" />
    </Icon>
  );
}
