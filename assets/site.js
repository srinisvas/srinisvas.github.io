const toggle = document.querySelector('.nav-toggle');
const navigation = document.getElementById('navigation-links');

if (toggle && navigation) {
  document.documentElement.classList.add('js');
  const setOpen = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  };
  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      toggle.focus();
    }
  });
  window.matchMedia('(max-width: 760px)').addEventListener('change', () => setOpen(false));
}

const printButton = document.querySelector('[data-print-resume]');
if (printButton) {
  printButton.hidden = false;
  printButton.addEventListener('click', () => window.print());
}
