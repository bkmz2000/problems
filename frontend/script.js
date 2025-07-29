let codeMirrorEditor = CodeMirror(document.getElementById('code-editor'), {
  value: '# Write your code here\n',
  mode: 'python',
  theme: 'material',
  lineNumbers: true,
  indentUnit: 4,
  tabSize: 4,
  autofocus: true,
  lineWrapping: true,
});

document.getElementById('file-upload').addEventListener('change', function (e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function (event) {
    codeMirrorEditor.setValue(event.target.result);
  };
  reader.readAsText(file);
});

document.getElementById('submit-btn').addEventListener('click', async function () {
  const code = codeMirrorEditor.getValue();
  document.getElementById('result').textContent = 'Submitting...';
  try {
    const response = await fetch('/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code: code,
        language_id: 71 // Python 3
      })
    });
    const result = await response.json();
    if (result.stdout !== undefined) {
      document.getElementById('result').textContent = 'Output: ' + result.stdout.trim();
    } else if (result.stderr) {
      document.getElementById('result').textContent = 'Error: ' + result.stderr;
    } else if (result.error) {
      document.getElementById('result').textContent = 'Server error: ' + result.error;
    } else {
      document.getElementById('result').textContent = 'Unknown response';
    }
  } catch (err) {
    document.getElementById('result').textContent = 'Network error: ' + err;
  }
});
