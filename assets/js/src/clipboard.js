$(document).ready(function () {
  function fallbackCopy(text) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(textarea);
  }

  function showCopied($btn) {
    $btn.html('<i class="fa fa-check"></i>');
    $btn.addClass('copied');
    setTimeout(function () {
      $btn.html('<i class="fa fa-clipboard"></i>');
      $btn.removeClass('copied');
    }, 2000);
  }

  $('.highlight').each(function () {
    var $highlight = $(this);
    $highlight.css('position', 'relative');

    var $btn = $('<button class="code-copy-btn" title="Copy"><i class="fa fa-clipboard"></i></button>');
    $highlight.prepend($btn);

    $btn.on('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      var codeEl = $highlight.find('td.code pre, pre.highlight, > pre').first();
      var text = codeEl.length ? codeEl.text() : $highlight.text();

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () { showCopied($btn); },
          function () { fallbackCopy(text); showCopied($btn); }
        );
      } else {
        fallbackCopy(text);
        showCopied($btn);
      }
    });
  });
});
