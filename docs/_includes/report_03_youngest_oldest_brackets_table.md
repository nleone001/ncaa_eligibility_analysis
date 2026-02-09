<table class="youngest-oldest-brackets-table eligibility-combo-table"><thead><tr><th>Rank</th><th>Bracket</th><th>Average Age</th><th>Wrestlers</th></tr></thead><tbody><tr data-wrestlers="2014 125lbs" data-wrestlers-places="1. Jesse Delgado (Jr) | 2. Nahshon Garrett (So) | 3. Nico Megaludis (Jr) | 4. Joey Dance (Fr) | 5. Cory Clark (Fr) | 6. Dylan Peters (Fr) | 7. Darian Cruz (Fr) | 8. Earl Hall (Fr)" data-count="1"><td><strong>1</strong></td><td>2014 125lbs</td><td>1.62</td><td>Hover/Click for details</td></tr><tr data-wrestlers="2021 197lbs" data-wrestlers-places="1. AJ Ferrari (Fr) | 2. Nino Bonaccorsi (So) | 3. Myles Amine (Sr) | 4. Jacob Warner (Jr) | 5. Rocky Elam (Fr) | 6. Jake Woodley (Jr) | 7. Michael Beard (Fr) | 8. Stephen Buchanan (Fr)" data-count="1"><td><strong>2</strong></td><td>2021 197lbs</td><td>2.00</td><td>Hover/Click for details</td></tr><tr data-wrestlers="2007 149lbs" data-wrestlers-places="1. Gregor Gillespie (So) | 2. Josh Churella (Jr) | 3. Dustin Schlatter (So) | 4. Lance Palmer (Fr) | 5. J.P. O&#x27;Connor (Fr) | 6. Tyler Turner (Sr) | 7. Matt Coughlin (Fr) | 8. Jordan Leen (So)" data-count="1"><td><strong>3</strong></td><td>2007 149lbs</td><td>2.00</td><td>Hover/Click for details</td></tr><tr><td colspan="4" style="background-color: #f0f0f0; padding: 0.5rem; font-weight: 600; text-align: center;">Oldest Brackets</td></tr><tr data-wrestlers="2025 285lbs" data-wrestlers-places="1. Wyatt Hendrickson (SSr) | 2. Gable Steveson (SSr) | 3. Cohlton Schultz (SSr) | 4. Isaac Trumble (Jr) | 5. Owen Trephan (SSr) | 6. Greg Kerkvliet (SSr) | 7. Joshua Heindselman (SSr) | 8. Ben Kueter (Fr)" data-count="1"><td><strong>1</strong></td><td>2025 285lbs</td><td>4.25</td><td>Hover/Click for details</td></tr><tr data-wrestlers="2025 184lbs" data-wrestlers-places="1. Carter Starocci (SSr) | 2. Parker Keckeisen (SSr) | 3. Max McEnelly (Fr) | 4. Dustin Plott (SSr) | 5. Chris Foca (Sr) | 6. Jaxon Smith (Jr) | 7. Silas Allred (Jr) | 8. Donnell Washington (SSr)" data-count="1"><td><strong>2</strong></td><td>2025 184lbs</td><td>3.88</td><td>Hover/Click for details</td></tr><tr data-wrestlers="2014 165lbs" data-wrestlers-places="1. David Taylor (Sr) | 2. Tyler Caldwell (Sr) | 3. Steve Monk (Sr) | 4. Nick Sulzer (Jr) | 5. Michael Moreno (Sr) | 6. Turtogtokh Luvsandorj (Sr) | 7. Daniel Zilverberg (Sr) | 8. Pierce Harger (Jr)" data-count="1"><td><strong>3</strong></td><td>2014 165lbs</td><td>3.75</td><td>Hover/Click for details</td></tr></tbody></table>
<script>
(function() {
  var tip = null;
  var expandContainer = null;
  var allRows = null;

  function ensureTooltipStyles() {
    if (document.getElementById('wrestler-tooltip-styles')) return;
    var style = document.createElement('style');
    style.id = 'wrestler-tooltip-styles';
    style.textContent = '.wrestler-tooltip{position:fixed;background:#fff;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.12);padding:12px;font-size:0.85rem;line-height:1.5;max-height:400px;max-width:500px;overflow-y:auto;overflow-x:hidden;z-index:1000;pointer-events:none;border:1px solid #e2e8f0;white-space:normal}.wrestler-tooltip .wrestler-tooltip-title{font-weight:600;margin-bottom:6px;color:#1a1a1a}.wrestler-tooltip .wrestler-tooltip-list{margin:0;padding-left:1.2em}';
    document.head.appendChild(style);
  }

  var WRESTLER_DELIM = ' | ';
  
  function showTip(el, x, y) {
    var detailsStr = el.getAttribute('data-wrestlers-places');
    if (!detailsStr || !tip) return;
    
    var title = tip.querySelector('.wrestler-tooltip-title');
    var list = tip.querySelector('.wrestler-tooltip-list');
    title.textContent = el.getAttribute('data-wrestlers');
    
    var items = detailsStr.split(WRESTLER_DELIM);
    list.innerHTML = items.map(function(item){ return '<li>' + item + '</li>'; }).join('');
    tip.style.left = (x + 16) + 'px';
    tip.style.top = (y - 10) + 'px';
    tip.style.display = 'block';
  }
  
  function hideTip() { if (tip) tip.style.display = 'none'; }

  function showExpand(tr) {
    var detailsStr = tr.getAttribute('data-wrestlers-places');
    if (!detailsStr || !expandContainer) return;
    
    allRows.forEach(function(r) { r.classList.remove('combo-row-selected'); });
    tr.classList.add('combo-row-selected');
    
    var title = expandContainer.querySelector('.combo-expand-title');
    var list = expandContainer.querySelector('.combo-expand-list');
    title.textContent = tr.getAttribute('data-wrestlers');
    
    var items = detailsStr.split(WRESTLER_DELIM);
    list.innerHTML = items.map(function(item){ return '<li>' + item + '</li>'; }).join('');
    
    var table = tr.closest('table');
    if (table.nextSibling !== expandContainer) {
      if (expandContainer.parentNode) expandContainer.parentNode.removeChild(expandContainer);
      table.parentNode.insertBefore(expandContainer, table.nextSibling);
    }
    expandContainer.classList.add('is-visible');
  }
  
  function hideExpand() {
    if (expandContainer) expandContainer.classList.remove('is-visible');
    if (allRows) allRows.forEach(function(r) { r.classList.remove('combo-row-selected'); });
  }

  document.addEventListener('DOMContentLoaded', function() {
    ensureTooltipStyles();
    tip = document.createElement('div');
    tip.className = 'wrestler-tooltip';
    tip.innerHTML = '<div class="wrestler-tooltip-title"></div><ul class="wrestler-tooltip-list"></ul>';
    tip.style.display = 'none';
    document.body.appendChild(tip);

    expandContainer = document.createElement('div');
    expandContainer.id = 'youngest-oldest-expand-container';
    expandContainer.className = 'combo-expand-container';
    expandContainer.innerHTML = '<div class="combo-expand-title"></div><ul class="combo-expand-list" style="list-style: none; padding: 0;"></ul>';

    allRows = document.querySelectorAll('.youngest-oldest-brackets-table tbody tr[data-wrestlers-places]');
    allRows.forEach(function(tr) {
      tr.style.cursor = 'pointer';
      tr.addEventListener('mouseenter', function(e) { showTip(tr, e.clientX, e.clientY); });
      tr.addEventListener('mousemove', function(e) { showTip(tr, e.clientX, e.clientY); });
      tr.addEventListener('mouseleave', hideTip);
      tr.addEventListener('click', function() {
        if (tr.classList.contains('combo-row-selected')) {
          hideExpand();
        } else {
          showExpand(tr);
        }
      });
    });
  });
})();
</script>
