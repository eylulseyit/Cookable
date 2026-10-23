import ThemeToggle from '@/components/ThemeToggle';

/** The same compact bar on every screen, pinned to the top of the page. */
export default function Header() {
  return (
    <header className="sticky top-0 z-10 border-b-2 border-line bg-bg/95 px-4 py-3 backdrop-blur sm:px-6">
      <div className="mx-auto flex max-w-3xl items-center justify-between gap-4">
        <span className="text-3xl leading-none font-extrabold tracking-tighter">
          Cook<span className="text-accent">able</span>
        </span>
        <ThemeToggle />
      </div>
    </header>
  );
}
