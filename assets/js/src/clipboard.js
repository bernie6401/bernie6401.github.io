$(document).ready(function () {
  var CMD_PATTERNS = [
    // $ command
    { regex: /^\$\s+(.+)/, strip: function (m) { return m[1]; } },
    // user@host:path$ command  or  user@host:path# command
    { regex: /^.*?@.*?[:][^\$#]*[\$#]\s+(.+)/, strip: function (m) { return m[1]; } },
    // kali@kali:~$ (already covered above)
    // *Evil-WinRM* PS C:\path> command
    { regex: /^\*Evil-WinRM\*\s+PS\s+.*?>\s+(.+)/, strip: function (m) { return m[1]; } },
    // PS C:\path> command
    { regex: /^PS\s+[A-Za-z]:\\.*?>\s+(.+)/, strip: function (m) { return m[1]; } },
    // SQL (context)> command
    { regex: /^SQL\s+\(.*?\)>\s+(.+)/, strip: function (m) { return m[1]; } },
    // smb: \path\> command
    { regex: /^smb:\s+\\.*?>\s+(.+)/, strip: function (m) { return m[1]; } },
    // dz> command
    { regex: /^dz>\s+(.+)/, strip: function (m) { return m[1]; } },
    // meterpreter > command
    { regex: /^meterpreter\s*>\s+(.+)/, strip: function (m) { return m[1]; } },
    // msf6/msf > command
    { regex: /^msf\d*[\s(>].*?>\s+(.+)/, strip: function (m) { return m[1]; } }
  ];

  function matchCommand(line) {
    var trimmed = line.replace(/^\s+/, '');
    for (var i = 0; i < CMD_PATTERNS.length; i++) {
      var m = trimmed.match(CMD_PATTERNS[i].regex);
      if (m) return CMD_PATTERNS[i].strip(m);
    }
    return null;
  }

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

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(function () {
        fallbackCopy(text);
      });
    }
    fallbackCopy(text);
    return $.Deferred().resolve().promise();
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
    var codeEl = $highlight.find('td.code pre, pre.highlight, > pre').first();
    if (!codeEl.length) return;

    var text = codeEl.text();
    var lines = text.split('\n');
    var lineHeight = parseFloat(getComputedStyle(codeEl[0]).lineHeight);
    var paddingTop = parseFloat(getComputedStyle(codeEl[0]).paddingTop) || 0;

    var $overlay = $('<div class="cmd-copy-overlay"></div>');
    $highlight.css('position', 'relative');
    $highlight.append($overlay);

    var i = 0;
    while (i < lines.length) {
      var cmd = matchCommand(lines[i]);
      if (cmd !== null) {
        var startLine = i;
        var fullCmd = cmd;

        // Handle multi-line commands with \ continuation
        while (fullCmd.match(/\\\s*$/) && i + 1 < lines.length) {
          i++;
          fullCmd += '\n' + lines[i];
        }

        var topPos = paddingTop + startLine * lineHeight;

        (function (command, top) {
          var $btn = $('<button class="cmd-copy-btn" title="Copy command"><i class="fa fa-clipboard"></i></button>');
          $btn.css('top', top + 'px');
          $overlay.append($btn);

          $btn.on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            $.when(copyText(command)).then(function () {
              showCopied($btn);
            });
          });
        })(fullCmd, topPos);
      }
      i++;
    }
  });
});
