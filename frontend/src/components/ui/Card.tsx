import type { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  highlight?: boolean;
  className?: string;
}

export function Card({ children, highlight = false, className = '' }: CardProps) {
  const border = highlight ? 'border-primary' : 'border-line';
  return (
    <section className={`flex flex-col gap-5 rounded-2xl border-2 bg-surface p-6 sm:p-7 ${border} ${className}`}>
      {children}
    </section>
  );
}

interface StepHeadingProps {
  step: number;
  title: string;
  hint?: string;
}

export function StepHeading({ step, title, hint }: StepHeadingProps) {
  return (
    <div className="flex items-baseline gap-3.5">
      <span className="text-sm font-extrabold text-accent-text">{String(step).padStart(2, '0')}</span>
      <h2 className="text-2xl font-extrabold tracking-tight">
        {title}
        {hint && <span className="ml-2 text-sm font-medium text-muted">{hint}</span>}
      </h2>
    </div>
  );
}
