// Simple slider logic + dots + autoplay
document.addEventListener('DOMContentLoaded', function(){
  const slides = Array.from(document.querySelectorAll('.slide'));
  const dotsWrap = document.getElementById('sliderDots');
  const prevBtn = document.getElementById('prevSlide');
  const nextBtn = document.getElementById('nextSlide');
  let idx = slides.findIndex(s => s.classList.contains('active'));
  if(idx < 0) idx = 0;
  let autoplay = true;
  let timeout = null;

  function goTo(i){
    slides.forEach((s, j) => {
      s.classList.toggle('active', j===i);
    });
    Array.from(dotsWrap.children).forEach((d,j)=> d.classList.toggle('active', j===i));
    idx = i;
  }

  function next(){
    goTo((idx+1) % slides.length);
  }
  function prev(){
    goTo((idx-1 + slides.length) % slides.length);
  }

  // build dots
  slides.forEach((s,i)=>{
    const b = document.createElement('button');
    b.addEventListener('click', ()=>{ goTo(i); resetTimer(); });
    if(i===idx) b.classList.add('active');
    dotsWrap.appendChild(b);
  });

  nextBtn.addEventListener('click', ()=>{ next(); resetTimer(); });
  prevBtn.addEventListener('click', ()=>{ prev(); resetTimer(); });

  function resetTimer(){
    if(timeout) clearInterval(timeout);
    if(autoplay) timeout = setInterval(next, 5000);
  }

  // autoplay
  timeout = setInterval(next, 5000);

  // mobile menu toggle (basic)
  const mobileBtn = document.querySelector('.mobile-menu-btn');
  mobileBtn && mobileBtn.addEventListener('click', ()=>{
    const nav = document.querySelector('.main-nav');
    if(nav) nav.style.display = (nav.style.display === 'flex') ? 'none' : 'flex';
  });

  // make news row draggable horizontally on touch
  const newsRow = document.getElementById('newsRow');
  if(newsRow){
    let pos = null;
    newsRow.addEventListener('touchstart', (e)=> pos = e.touches[0].clientX);
    newsRow.addEventListener('touchmove', (e)=>{
      if(pos === null) return;
      const delta = e.touches[0].clientX - pos;
      newsRow.scrollLeft -= delta;
      pos = e.touches[0].clientX;
    });
    newsRow.addEventListener('touchend', ()=> pos = null);
  }
});