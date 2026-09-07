// Shared quiz widget. Markup:
// <div class="quiz" data-answer="b">
//   <div class="q">Question?</div>
//   <label><input type="radio" name="q1" value="a">option a</label> ...
//   <div class="fb ok">Right because...</div><div class="fb no">Not quite: ...</div>
// </div>
// Options should be the same length so formatting gives no hints.
document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.quiz').forEach((qz,i)=>{
    const ans=qz.dataset.answer;
    qz.querySelectorAll('input[type=radio]').forEach(inp=>{
      if(!inp.name)inp.name='quiz'+i;
      inp.addEventListener('change',()=>{
        qz.classList.remove('correct','wrong');
        qz.querySelectorAll('label').forEach(l=>l.classList.remove('chosen','right'));
        inp.closest('label').classList.add('chosen');
        if(inp.value===ans){qz.classList.add('correct');inp.closest('label').classList.add('right');}
        else qz.classList.add('wrong');
        try{localStorage.setItem(location.pathname+'#'+inp.name,inp.value===ans?'1':'0');}catch(e){}
      });
    });
  });
  // Score summary if a #score element exists
  const s=document.getElementById('score');
  if(s){const upd=()=>{const all=[...document.querySelectorAll('.quiz')];const ok=all.filter(q=>q.classList.contains('correct')).length;s.textContent=ok+' / '+all.length+' correct';};document.addEventListener('change',upd);upd();}
});
