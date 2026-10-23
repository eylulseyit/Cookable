import type { ButtonHTMLAttributes } from 'react';

type Variant = 'primary' | 'strong' | 'outline';

const variants: Record<Variant, string> = {
  primary: 'bg-primary text-on-primary',
  strong: 'bg-strong text-on-strong',
  outline: 'border-2 border-field-line text-fg hover:bg-surface',
};

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

export function Button({ variant = 'strong', className = '', type = 'button', ...props }: ButtonProps) {
  return (
    <button
      type={type}
      className={`rounded-xl font-extrabold transition hover:brightness-95 disabled:cursor-not-allowed disabled:opacity-50 ${variants[variant]} ${className}`}
      {...props}
    />
  );
}
