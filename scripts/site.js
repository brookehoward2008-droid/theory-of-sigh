const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('#nav-links');

if (navToggle && navLinks) {
  navToggle.onclick = () => {
    const open = navLinks.classList.toggle('is-open');
    navToggle.classList.toggle('is-open', open);
    navToggle.setAttribute('aria-expanded', String(open));
  };
}

const pages = [...document.querySelectorAll('.issue-page')];
const prev = document.querySelector('.page-prev');
const next = document.querySelector('.page-next');
const current = document.querySelector('#current-page');
const total = document.querySelector('#total-pages');
let page = 0;

function turnTo(n) {
  page = Math.max(0, Math.min(n, pages.length - 1));
  pages.forEach((el, i) => {
    el.classList.toggle('is-active', i === page);
    el.classList.toggle('is-before', i < page);
    el.classList.toggle('is-after', i > page);
  });
  if (current) current.textContent = page + 1;
  if (total) total.textContent = pages.length;
}

if (pages.length) {
  turnTo(0);
  if (prev) prev.onclick = () => turnTo(page - 1);
  if (next) next.onclick = () => turnTo(page + 1);
  document.onkeydown = (event) => {
    if (event.key === 'ArrowRight') turnTo(page + 1);
    if (event.key === 'ArrowLeft') turnTo(page - 1);
  };
}
